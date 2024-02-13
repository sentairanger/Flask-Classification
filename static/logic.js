function classifier() {
  $.get('/classify', function(data) {
    $('#image').html(data);  // update page with new data
  });
};
