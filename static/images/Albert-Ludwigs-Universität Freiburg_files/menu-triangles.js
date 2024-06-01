(function ($) {
    var $menu = $(".main-menu");
    $(document).ready(function () {
        $(".main-menu").menuAim({
            // Function to call when a row is purposefully activated. Use this
            // to show a submenu's content for the activated row.
            activate: activateSubmenu,

            // Function to call when a row is deactivated.
            deactivate: deactivateSubmenu,

            // Function to call when mouse exits the entire menu. If this returns
            // true, the current row's deactivation event and callback function
            // will be fired. Otherwise, if this isn't supplied or it returns
            // false, the currently activated row will stay activated when the
            // mouse leaves the menu entirely.
            exitMenu: deactivateSubmenu,

            // Selector for identifying which elements in the menu are rows
            // that can trigger the above events. Defaults to "> li".
            rowSelector: "> li",

            // You may have some menu rows that aren't submenus and therefore
            // shouldn't ever need to "activate." If so, filter submenu rows w/
            // this selector. Defaults to "*" (all elements).
            submenuSelector: ".menu-item-has-children",

            // Direction the submenu opens relative to the main menu. This
            // controls which direction is "forgiving" as the user moves their
            // cursor from the main menu into the submenu. Can be one of "right",
            // "left", "above", or "below". Defaults to "right".
            submenuDirection: "below"
        });
    });


    function activateSubmenu(row) {
        $(row).addClass("selected");
    }

    function deactivateSubmenu(row) {
        $('.main-menu > li').removeClass("selected");
    }
})(jQuery);

