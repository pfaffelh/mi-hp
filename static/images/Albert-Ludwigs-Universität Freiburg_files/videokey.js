// This function is to load the video player from the media portal of the university of freiburg

(function ($) {
  $(document).ready(function() {
    $("div[class^='wp-block-unifreiburg-blocks-videoportal-block']").find("p.videoiframe").each(function() {
         $(this).hide();
         var videokeyitem = $(this).html();
         $( '<!--  Video - Referenzierung --><div class="video aspect-ratio"> <iframe aria-label="Video from the media portal of the University of Freiburg" src="https://videoportal.uni-freiburg.de/media/embed?key='+videokeyitem+'&autoplay=false&autolightsoff=false&loop=false&chapters=false&responsive=true&loadonclick=true&thumb=true" data-src="https://videoportal.uni-freiburg.de/media/embed?key='+videokeyitem+'&autoplay=false&autolightsoff=false&loop=false&chapters=false&responsive=true&loadonclick=true" frameborder="0" allowfullscreen="allowfullscreen" allowtransparency="true" scrolling="no"></iframe></div>' ).insertAfter($(this))   ;
     });
  });
})(jQuery);