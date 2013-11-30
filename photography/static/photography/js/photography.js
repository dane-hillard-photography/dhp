$(document).ready(function() {
  $('.photo').fancybox({
    beforeShow: function() {
      $.fancybox.wrap.bind("contextmenu", function(e) {
        return false;
      });
    },
    beforeLoad: function() {
      var element, id = $(this.element).data('title-id');

      if (id) {
        element = $('#' + id);

        if (element.length) {
          this.title = element.html();
        }
      }
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
      },
      thumbs: {
        width: 50,
        height: 50
      }
    }
  });
});
