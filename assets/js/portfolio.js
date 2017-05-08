/* global lightbox */

$(function(){
    "use strict";
    lightbox.option({
      'resizeDuration': 300,
      'wrapAround': true
    });
});

$(window).load(function(){
    "use strict";
    $('.grid').masonry({
      itemSelector: '.grid-item',
      columnWidth: 400
    });
});
