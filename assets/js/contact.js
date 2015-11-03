$(function(){
    $('.send-button').on('click', function(){
        ga('send', {
            'hitType': 'event',
            'eventCategory': 'button',
            'eventAction': 'click',
            'eventLabel': 'send message',
            'eventValue': 1
        });
    });
});
