// var rellax = new Rellax('.rellax');

(function ($) {
$(document).ready(function () {
     $(window).scroll(function () {
            var maxY = $('body').height() - $(window).height();
            var currY = $(this).scrollTop();
            var scrollPercent = 100 - (currY / maxY) * 100;
            $('.parallax').css('transform', 'translateY(' + scrollPercent + '%)');

        });
    })
    })
(jQuery);
