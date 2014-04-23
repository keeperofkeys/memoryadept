"use strict";

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
  $.ajax({
    url: '/location-contents/' + $(this).val
  });
});
