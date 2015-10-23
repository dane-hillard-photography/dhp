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

$('.external-site a').on('click', function(){
    ga('send', {
        'hitType': 'event',
        'eventCategory': 'button',
        'eventAction': 'click',
        'eventLabel': $(this).attr('title'),
        'eventValue': 1
    });
});

$(window).on("scroll", function() {
    var scrollHeight = $(document).height();
    var scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
        ga('send', {
            'hitType': 'event',
            'eventCategory': 'post',
            'eventAction': 'read',
            'eventLabel': 'post read',
            'eventValue': 1
        });
    }
});
