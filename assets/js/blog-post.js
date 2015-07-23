$('#feedlyFollow').on('click', function(){
    ga('send', {
        'hitType': 'event',
        'eventCategory': 'button',
        'eventAction': 'click',
        'eventLabel': 'feedly follow',
        'eventValue': 1
    });
});

$('#pinterest-pin').on('click', function(){
    ga('send', {
        'hitType': 'event',          
        'eventCategory': 'button',   
        'eventAction': 'click',      
        'eventLabel': 'pinterest pin',
        'eventValue': 1
    });
});
