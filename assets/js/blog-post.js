/* global ga */

import $ from 'jquery';


$(function () {
    'use strict';
    $('.external-site a').on('click', function(){
        ga('send', {
            'hitType': 'event',
            'eventCategory': 'button',
            'eventAction': 'click',
            'eventLabel': $(this).attr('title'),
            'eventValue': 1
        });
    });

    var readEventSentAlready = false;

    $(window).on('scroll', function() {
        var elementPosition = $('.external-site-list').offset().top;
        var scrollPosition = $(window).height() + $(window).scrollTop();
        if (elementPosition < scrollPosition) {
            if (!readEventSentAlready) {
                ga('send', {
                    'hitType': 'event',
                    'eventCategory': 'post',
                    'eventAction': 'read',
                    'eventLabel': 'post read',
                    'eventValue': 1
                });
            }

            readEventSentAlready = true;
        }
    });
});
