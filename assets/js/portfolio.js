$(function(){
    lightbox.option({
      'resizeDuration': 300,
      'wrapAround': true
    });

    $('.grid').masonry({
      itemSelector: '.grid-item',
    });
});
