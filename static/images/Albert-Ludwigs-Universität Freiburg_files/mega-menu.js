// This function is a fix for mega menus, where the mega-item is higher than the mega-menu itself

(function ($) {
    $(document).ready(function () {
        $(".mega-menu-with-mega-item").one('mouseenter', function () {
            var totalHeight = 0;
            $(this).find("> ul .mega-item").children().each(function () {
                totalHeight = totalHeight + $(this).outerHeight(true);
            });
            $(this).find("> ul").css("min-height", totalHeight + 16);
        });
        $(".mega-menu-with-mega-item > button").one('click', function () {
            var totalHeight = 0;
            $(this).parent().find("> ul .mega-item").children().each(function () {
                totalHeight = totalHeight + $(this).outerHeight(true);
            });
            $(this).parent().find("> ul").css("min-height", totalHeight + 16);
        });
    });
})(jQuery);