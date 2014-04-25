"use strict";
var cardList;
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
          var newHtml = '<input type="radio" name="chosen_location" id="cb' + json.location_id + '">';
          newHtml += '<label for="cb' + json.location_id + '">' + json.location_name + '</label>'
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
      $table = $('#edit-card-list'),
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

$('.autocomplete').autocomplete({
   serviceUrl: '/suggestions/',
   //lookup: cardList,
   onSelect: function(suggestion) {
     alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
   }
});

$(document).ready(function() {
    $.ajax({
       url: '/json/',
       method: 'post',
       async: false,
       dataType: 'json',
       success: function(json) {
         cardList = json;
       }
    });
});
