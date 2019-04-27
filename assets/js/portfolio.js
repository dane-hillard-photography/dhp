import { $ } from 'jquery';
import lightbox from 'lightbox2/src/js/lightbox';
import Masonry from 'masonry-layout/masonry';
import ImagesLoaded from 'imagesloaded/imagesloaded';

$(function(){
    'use strict';
    lightbox.option({
        'resizeDuration': 300,
        'wrapAround': true
    });

    var grid = new Masonry('.grid', {
        itemSelector: '.grid-item',
        columnWidth: 300
    });

    var imageWaiter = new ImagesLoaded('.grid');
    imageWaiter.on('progress', function(imageLoad, image) {
        var $theImage = $(image.img).parents('.grid-item');
        $theImage.removeClass('hidden');
        grid.appended($theImage);
    });
});
