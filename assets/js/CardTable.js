"use strict";
function CardTable(selector) {
  this.selector = selector;
  this.$table = $(this.selector).eq(0);
  this.$form = this.$table.closest('form');
  this.updateRows();
  this.$table.find('.autocomplete').autocomplete(MA.autocompleteSettings);
  
  var that = this;
  this.$table.on('click', '.addRow',function(e) {
      e.preventDefault();
      that.addRow();
      $(this).remove();
    }).on('click', '.deleteRow',function(e) {
      e.preventDefault();
      $(this).closest('tr').remove();
      that.updateRows();
    }).closest('form').on('submit', function(e) {
      e.preventDefault();
      var data,
          locationId = that.$form.find('input[name=chosen_location]:checked').val();
    
      // validate
      if (!locationId) {
        alert('choose a location');
        return;
      }
    
      data = {
        cards: JSON.stringify(that.harvestData()),
        location: locationId
      };
      
      $.ajax({
         url: that.$form.attr('action'),
         method: 'post',
         data: data,
         success: function(response) {
           alert('updated');
         }
      });
    });
}

CardTable.prototype.updateRows = function() {
  this.$rows = this.$table.find('tr:not(:first-child)');
};

CardTable.prototype.addRow = function(data) {
  var $rowTemplate = this.$table.find('tr:last-child').clone(false),
      $newRow = this.$table
        .append($rowTemplate)
        .find('tr:last-child'),
      $oldInputs = this.$rows.eq(0).find('input'),
      $newInputs = $newRow.find('input'),
      that = this;

  $newInputs.each(function(j) {
    var field = $oldInputs.eq(j).fieldName(),
        $input = $(this);

    $input.attr('name', field + '-' + that.$rows.length);
    if (data && data[field]) {
      $input.val(data[field]);
    } else {
      $input.val('');
    }
  });

  // attach new Autocomplete() 
  $newInputs.filter('[name^="name"]').autocomplete(MA.autocompleteSettings)
      .end().filter('[name^="count"]').focus();

  this.updateRows();
};

CardTable.prototype.rebuild = function(cards) {
  this.$table.find('tr:not(:first-child) + tr').remove();
  if (cards.length > 0) {
    for (var i in cards) {
      if (cards.hasOwnProperty(i)) {
        this.addRow(cards[i]);
      }
    }
    this.$table.find('tr:first-child + tr').remove();
  } else {
    this.$table.find('tr:first-child + tr input').val('');
  }
  
  this.updateRows();
};

CardTable.prototype.harvestData = function() {
  var response = {};
  this.$table.find('tr:not(:first-child)').each(function() {
    var obj = {}, name;
    $(this).find('input').each(function() {
      var $this = $(this),
          field = $this.fieldName();
      obj[field] = MA.utils.makeNice($this.val()); // could potentially be empty
    });
    name = obj.name;
    if (name) {
      //delete obj.name; // not strictly needed but let's leave it in for now
      response[name] = obj;
    }
  });
  return response;
};
