$(document).ready(function() {
  $('.photo').fancybox({
    beforeShow: function() {
      $.fancybox.wrap.bind("contextmenu", function(e) {
        return false;
      });
    },
    openEffect  : 'elastic',
    closeEffect : 'elastic',
    nextEffect  : 'fade',
    prevEffect  : 'fade',
    padding     : 0,
    closeBtn    : false,
    arrows      : false,
    nextClick   : true,
    helpers : {
      overlay : {
        css : {
          'background' : 'rgba(0, 0, 0, .8)'
        }
      },
      title: {
        type: 'float',
        position: 'top'
      }
    }
  });
});