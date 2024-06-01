/*************************************************
 * 
 *                 THE FUNCTIONS
 * 
 ************************************************/

// Translation
const { __, _x, _n, _nx } = wp.i18n;

// Count first-level-items in menu
var itemsInMenuInit = jQuery('.main-menu > li').length;

// Helper function to write less code by calculating the right edge of an item
function itemRightEdge(item, withMargin) {
  return jQuery(item).offset().left + jQuery(item).outerWidth(withMargin);
}

function itemLeftEdge(item) {
  return jQuery(item).offset().left;
}

// Show menu and put stuff inside
function addToMoreMenu() { // the final push + re-run
  (function ($) {
    let itemsInMainMenu = $('.main-menu > li').length - 1;

    if (itemsInMainMenu > 0) {
      let itemsInMoreMenu = $('.main-menu-more > ul > li').length;
      let menuRightEdge = itemLeftEdge('.site-nav-and-search > .language-button-wrapper') - 40;

      // here the whole thing starts work
      if (itemsInMoreMenu > 0) {
        let moreButtonRightEdge = itemRightEdge('.main-menu-more', true);
        if (menuRightEdge < moreButtonRightEdge) {
          theAddActions(itemsInMainMenu, itemsInMoreMenu);
        }
      } else {
        let lastMenuItemRightEdge = itemRightEdge('.main-menu > li:nth-last-of-type(2)', true);
        if (menuRightEdge < lastMenuItemRightEdge) {
          theAddActions(itemsInMainMenu, itemsInMoreMenu);
          $('.main-menu-more').removeClass('hidden'); // show the "more"-item; only needed at first run
        }
      };
    };
  })(jQuery);
}

/* This is where the magic happens */

function theAddActions(itemsInMainMenu, itemsInMoreMenu) {
  (function ($) {

    /* this is the important push */

    let lastMenuItem = $('.main-menu > li:nth-last-of-type(2)');
    lastMenuItem.attr('data-size', lastMenuItem.outerWidth(true)); // store size of item as attribute; needed for removeFromMenu
    $('.main-menu-more > ul').prepend(lastMenuItem); // add item to more-menu
    addToMoreMenu(); // re-run the function to check the next item

    /* this checks for creation of hamburger */
    if (itemsInMainMenu < 3) { // this is the status before the item is being pushed!
      if ((itemsInMenuInit > 1) || (itemsInMoreMenu > 0)) {
        $('.main-menu').addClass('menu-hamburger');
        $('.site-branding-inner-container').addClass('is-menu-hamburger');
        let firstMenuItem = $('.main-menu > li:first-of-type');
        firstMenuItem.attr('data-size', firstMenuItem.outerWidth(true)); // store size of item as attribute; needed for removeFromMenu
        $('.main-menu-more > ul').prepend($('.main-menu').find(' > li:not(.main-menu-more)'));
      };
    };

  })(jQuery);
}


function removeFromMoreMenu() {
  (function ($) {
    let itemsInMoreMenu = $('.main-menu-more > ul > li').length;
    if (itemsInMoreMenu > 0) {
      let menuRightEdge = itemLeftEdge('.site-nav-and-search > .language-button-wrapper') - 40;
      let firstMoreMenuItemWidth = $('.main-menu-more > ul > li:first-child').data('size');
      var secondMoreMenuItemWidth = 0; // this is backup if the menu has only one single item
      let itemsInMainMenu = $('.main-menu > li').length - 1;

      if ($('.main-menu-more > ul > li').length > 1) { // nicht-Letztes Item rausholen
        let moreButtonRightEdge = itemRightEdge('.main-menu-more', true);
        if (itemsInMainMenu > 0) { // if it's not a "hamburger"-menu
          if (menuRightEdge > moreButtonRightEdge + firstMoreMenuItemWidth) {
            theRemoveActions();
            removeFromMoreMenu();
          }
        } else { // if it's a "hamburger"-menu -> two items have to be pushed
          var secondMoreMenuItemWidth = $('.main-menu-more > ul > li:nth-child(0n+2)').data('size');

          if ((menuRightEdge > moreButtonRightEdge + firstMoreMenuItemWidth + secondMoreMenuItemWidth)) {
            theRemoveActions();
            removeFromMoreMenu();
            /* Hamburger-Menü zurückwandeln */
            $('.main-menu').removeClass('menu-hamburger');
            $('.site-branding-inner-container').removeClass('is-menu-hamburger');
          }

        }
      } else { // letztes Item rausholen
        let lastMenuItemRightEdge = itemRightEdge('.main-menu > li:nth-last-of-type(2)', true);
        if (menuRightEdge > lastMenuItemRightEdge + firstMoreMenuItemWidth) {
          theRemoveActions();
          $('.main-menu-more').addClass('hidden');
        }
      }
    };
  })(jQuery);
}

/* This is where the remove-magic happens */

function theRemoveActions() {
  (function ($) {
    /* push the thing! */
    $('.main-menu-more > ul > li:first-child').insertBefore('.main-menu-more');

    /* close everything in main menu */
    $('.main-menu > li.menu-item-has-children').find('button').next().attr('aria-hidden', true);
    $('.main-menu > li.menu-item-has-children').find('button').attr('aria-expanded', false);
    $('.main-menu > li').removeClass('faded');
  })(jQuery);
};

/*************************************************
 * 
 *                    INIT
 * 
 ************************************************/

// More-button
// jQuery(".main-menu").append("<li id='main-menu-more' class='main-menu-more menu-item-has-children hidden'><button class='sub-menu-expand' aria-expanded='false'><span class='text-more'>Mehr</span> <span class='text-menu'>Menü</span> <i class='fas fa-plus fa-80'></i></button><ul class='sub-menu'></ul></li>");
jQuery(".main-menu").append("<li id='main-menu-more' class='main-menu-more menu-item-has-children hidden'><button class='sub-menu-expand' aria-expanded='false'><span class='text-more'>"+__('More','unifreiburg-theme')+"</span> <span class='text-menu screen-reader-text'>"+__('Menu','unifreiburg-theme')+"</span> <i class='fas fa-plus fa-80'></i></button><ul class='sub-menu'></ul></li>");

addToMoreMenu();

(function ($) {
  $(document).ready(function () {
    addToMoreMenu();
  });
})(jQuery);

// Debouncing – needed for resizing : https://davidwalsh.name/javascript-debounce-function
// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
  var timeout;
  return function () {
    var context = this,
      args = arguments;
    var later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

var addMenuMoreOnResize = debounce(function () {
  removeFromMoreMenu();
  addToMoreMenu();
}, 100);

window.onorientationchange = function () {
  removeFromMoreMenu();
  addToMoreMenu();
};

// Resize effect muss für iOS-Devices angepasst werden, da sich das Menü beim Scrollen verändert oder gar eingeklappt hat.
// https://stackoverflow.com/questions/9361968/javascript-resize-event-on-scroll-mobile/24312082#24312082

var cachedWidth = jQuery(window).width();
jQuery(window).resize(function () {
  var newWidth = jQuery(window).width();
  if (newWidth !== cachedWidth) {
    jQuery(window).on('resize', addMenuMoreOnResize); // this is the important line to trigger the priority menu
    cachedWidth = newWidth;
  }
});