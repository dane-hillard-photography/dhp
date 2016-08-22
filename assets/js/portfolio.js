$(function(){
    lightbox.option({
      'resizeDuration': 300,
      'wrapAround': true
    });
});

$(window).load(function(){
    $('.grid').masonry({
      itemSelector: '.grid-item',
      columnWidth: 150
    });
});
