"use strict";
var autocompleteSettings = {
      serviceUrl: '/suggestions/',
      onSelect: function(suggestion) {
        console.log('selected: ' + suggestion.value + ', ' + suggestion.data);
      }
    };

$('#create-new').on('submit', function(e) {
  e.preventDefault();
  $.ajax({
    url: '/create-location',
    method: 'post',
    data: {
      'new-location' : $('#new-location').val()
    },
    success: function(json) {
      if (json.location_id) {
        if (json.new === true) {
          // add to list
          var newHtml = '<li><input type="radio" name="chosen_location" id="cb' + json.location_id + '">';
          newHtml += '<label for="cb' + json.location_id + '">' + json.location_name + '</label></li>';
          $('#locations').append($(newHtml));
        } 
        $('#locations #cb' + json.location_id).prop('checked', true);

      } else {
        alert('fell over');
      }
    }
  });
});

// clicked radio or made new location
$('#locations input[name=chosen_location]').on('change', function() {
  // load cards
  var locationId = this.id.substr(2), // slice off "cb" prefix
      $table = $('#edit-card-list table'),
      $rowTemplate = $table.find('tr:last-child');
  $.ajax({
    url: '/location-contents/' + locationId,
    method: 'post',
    success: function(cards) {
      for (var i=0; i<cards.length; i++) {
        $table.append($rowTemplate);
      }
    }
  });
});

$('#edit-card-list').on('click', '.addRow',function(e) {
  e.preventDefault();
  addTableRow();
  $(this).remove();
}).on('click', '.deleteRow',function(e) {
  e.preventDefault();
  $(this).closest('tr').remove();
}).on('submit', function(e) {
  e.preventDefault();
  var $form = $(this),
      data = $form.serializeArray(),
      locationId = $('input[name=chosen_location]:checked').val();

  // validate
  if (!locationId) {
    alert('choose a location');
    return;
  }

  $.ajax({
     url: $form.attr('action'),
     method: 'post',
     data: data,
     success: function(response) {
       alert('updated');
     }
  });
});

$('.autocomplete').autocomplete(autocompleteSettings);

function addTableRow() {
  var $table = $('#edit-card-list table'),
      $rows = $table.find('tr:not(:first-child)'), // exclude heading
      $rowTemplate = $table.find('tr:last-child').clone(false),
      $newRow = $table.append($rowTemplate).find('tr:last-child'),
      $inputs = $newRow.find('input');
      $inputs.get(0).name = 'n' + $rows.length;
      $inputs.get(1).name = 'c' + $rows.length;
      
      // attach new Autocomplete() 
      $inputs.eq(1).autocomplete(autocompleteSettings).val('');
}

