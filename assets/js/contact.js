$(function(){
    $('.send-button').on('click', function(e){
        e.preventDefault();
        ga(
            'send',
            {
                'hitType': 'event',
                'eventCategory': 'button',
                'eventAction': 'click',
                'eventLabel': 'send message',
                'eventValue': 1,
                hitCallback: function() {
                    $('.send-button').parents('form:first').submit();
                }
            });
    });
});
