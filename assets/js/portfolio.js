/* global lightbox */

$(function(){
    "use strict";
    lightbox.option({
      "resizeDuration": 300,
      "wrapAround": true
    });

    var $grid = $(".grid").masonry({
      itemSelector: ".grid-item",
      columnWidth: 300
    });

    $(".grid").imagesLoaded().progress(function(imageLoad, image) {
        var $theImage = $(image.img).parents(".grid-item");
        $theImage.removeClass("hidden");
        $grid.masonry("appended", $theImage);
    });
});
