"use strict";
var autocompleteSettings = {
      serviceUrl: '/suggestions/',
      onSelect: function(suggestion) {
        console.log('selected: ' + suggestion.value + ', ' + suggestion.data);
      }
    };

$('#create-new').on('submit', function(e) {
  e.preventDefault();
  var newLocation = $('#new-location').val();
  if (newLocation.toLowerCase() == 'limbo') return; // TODO: error message
  $.ajax({
    url: '/create-location',
    method: 'post',
    data: {
      'new-location' : newLocation
    },
    success: function(json) {
      if (json.location_id) {
        if (json.new === true) {
          // add to list
          var newHtml = '<li><input type="radio" name="chosen_location" id="cb' + json.location_id + '" value="'+json.location_id+'">';
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
  var locationId = this.id.substr(2); // slice off "cb" prefix
  $('#edit-card-list tr:not(:first-child) + tr').remove();
      
  $.ajax({
    url: '/location-contents/' + locationId,
    method: 'post',
    success: function(cards) {
      for (var i in cards) {
        if (cards.hasOwnProperty(i)) {
          addTableRow(cards[i]);
        }
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
      locationId = $('input[name=chosen_location]:checked').val(),
      data;

  // validate
  if (!locationId) {
    alert('choose a location');
    return;
  }

  data = {
    cards: JSON.stringify(harvestData($form)),//$form.serializeArray(),
    location: locationId
  };
  
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

function addTableRow(data) {
  var $table = $('#edit-card-list table'),
      $rows = $table.find('tr:not(:first-child)'), // exclude heading
      $rowTemplate = $table.find('tr:last-child').clone(false),
      $newRow = $table.append($rowTemplate).find('tr:last-child'),
      $oldInputs = $rows.eq(0).find('input'),
      $newInputs = $newRow.find('input');

  $newInputs.each(function(j) {
    var field = $oldInputs.eq(j).fieldName(),
        $input = $(this);

    $input.attr('name', field + '-' + $rows.length);
    if (data && data[field]) {
      $input.val(data[field]);
    } else {
      $input.val('');
    }
  });

  // attach new Autocomplete() 
  $newInputs.filter('[name^="name"]').autocomplete(autocompleteSettings);
 
}

function harvestData($form) {
  // iterate over rows; 
  var response = {};
  $form.find('tr:not(:first-child)').each(function() {
    var obj = {}, name;
    $(this).find('input').each(function() {
      var $this = $(this),
          field = $this.fieldName();
      obj[field] = makeNice($this.val()); // could potentially be empty
    });
    name = obj.name;
    if (name) {
      //delete obj.name; // not strictly needed but let's leave it in for now
      response[name] = obj;
    }
  });
  return response;
}

jQuery.prototype.fieldName = function() {
  var bits = this.get(0).name.split('-');
  return bits[0];
};

function makeNice(n) {
  // convert to number if possible
  if (isNaN(Number(n))) {
    return n;
  }
  n = Number(n);
  if (Math.floor(n) - n == 0) { // integer
    return Math.floor(n);
  }
  return n;
}

