// This function is to load the podcast player from the media portal of the university of freiburg

(function ($) {
  $(document).ready(function() {
    /* Podcast-Embed */
    $("div[class^='wp-block-unifreiburg-blocks-podcastportal-block']").find("p.podcastiframe").each(function() {
        $(this).hide();
        var podcastkeyitem = $(this).html();
        $( '<!--  Podcast - Referenzierung --><div class="podcast aspect-ratio"> <iframe aria-label="Podcast from the media portal of the University of Freiburg" src="https://video.uni-freiburg.de/media/embed?key='+podcastkeyitem+'&height=300&autoplay=false&autolightsoff=false&loop=false&chapters=false&related=false&responsive=true&audioembed=true&t=0" frameborder="0" allowfullscreen="allowfullscreen" allowtransparency="true" scrolling="no"></iframe></div>' ).insertAfter($(this))   ;
    });
  });
})(jQuery);