window.addEventListener("DOMContentLoaded", function() {
    var subMenuButtons = document.querySelectorAll("#site-navigation .sub-menu-expand");
    if (subMenuButtons.length === 0) {
        // No sub menus, so we can exit here.
        return;
    }

    initSubMenuButtons(subMenuButtons);
    setInitialAttributes(subMenuButtons);
    registerCloseActions();
});

/**
 * Polyfill for element.closest().
 * 
 * @łink https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
 */
if (!Element.prototype.matches) {
    Element.prototype.matches =
        Element.prototype.msMatchesSelector ||
        Element.prototype.webkitMatchesSelector;
}

if (!Element.prototype.closest) {
    Element.prototype.closest = function (s) {
        var el = this;

        do {
            if (Element.prototype.matches.call(el, s)) return el;
            el = el.parentElement || el.parentNode;
        } while (el !== null && el.nodeType === 1);
        return null;
    };
}

/**
 * Init the submenu buttons.
 * @param {NodeList} subMenuButtons 
 */
function initSubMenuButtons(subMenuButtons) {
    for (var i = 0; i < subMenuButtons.length; i++) {
        var button = subMenuButtons[i];
        button.addEventListener("click", function(e) {
            toggleSubMenu(this);
        });
    }
}

/**
 * Set initial attributes.
 * @param {NodeList} subMenuButtons 
 */
function setInitialAttributes(subMenuButtons) {
    for (var i = 0; i < subMenuButtons.length; i++) {
        var button = subMenuButtons[i],
            subMenu = button.closest("li").querySelector(".sub-menu");

        subMenu.setAttribute("aria-hidden", "true");
    }
}

/**
 * Actions that trigger closing of open sub menus.
 */
function registerCloseActions() {
    // Close sub menus on escape key.
    document.addEventListener("keydown", function(e) {
        var key = e.which || e.keyCode;
        if (key !== 27) {
            return;
        }

        closeSubMenus();
    });

    // Close sub menus when the user clicked something outside the #site-navigation container.
    document.addEventListener("click", function(e) {
        if (e.target.closest("#site-navigation")) {
            // Click event was inside #main-navigation.
            return;
        }

        closeSubMenus();
    });

    // Close sub menus when the user switches to mouse and hovers over another top menu entry.
    var menuItemsWithSubmenu = document.querySelectorAll("#site-navigation .main-menu > .menu-item-has-children");
    for (var i = 0; i < menuItemsWithSubmenu.length; i++) {
        var menuItem = menuItemsWithSubmenu[i];
        menuItem.addEventListener("mouseenter", function() {
            var hoveredItem = this;
            closeOtherSubMenus(hoveredItem);
        });
    }

    // Close submenus when focus is not inside submenu.
    document.addEventListener("focusin", function(e) {
        if (e.target.closest(".sub-menu")) {
            return;
        }

        closeSubMenus();
    });
}

/**
 * Toggle a submenu.
 * @param {Node} button The menu button.
 */
function toggleSubMenu(button) {
    var menuListItem = button.closest("li"),
        menuLink = menuListItem.querySelector("a[aria-haspopup='true']"),
        subMenu = menuListItem.querySelector(".sub-menu");

    menuListItem.classList.toggle("opened");
    toggleAriaExpanded(menuLink);
    toggleAriaExpanded(button);
    toggleAriaHidden(subMenu);
    if (menuLink.getAttribute("aria-expanded") === "true") {
        closeOtherSubMenus(menuListItem);
        return;
    }

    // We close a sub menu, we need to make sure the `selected` class is also removed.
    menuListItem.classList.remove("selected");
}

/**
 * Toggle aria-expanded attribute.
 * @param {Node} node 
 */
function toggleAriaExpanded(node) {
    if (node === null) {
        // Happens for »more« menu item.
        return;
    }
    if (node.getAttribute("aria-expanded") === "false") {
        node.setAttribute("aria-expanded", "true");
        return;
    }

    node.setAttribute("aria-expanded", "false");
}

/**
 * Toggle aria-hidden attribute.
 * @param {Node} node 
 */
function toggleAriaHidden(node) {
    if (node.getAttribute("aria-hidden") === "false") {
        node.setAttribute("aria-hidden", "true");
        return;
    }

    node.setAttribute("aria-hidden", "false");
}

/**
 * @param {Node} menuListItem The menu list item of the submenu button that was clicked.
 */
function closeOtherSubMenus(menuListItem) {
    var openMenus;
    // Check if the given menu item is inside a sub menu.
    if (menuListItem.closest(".sub-menu")) {
        // Get open sub menus on same level.
        openMenus = menuListItem.closest(".sub-menu").querySelectorAll(".menu-item-has-children.opened")
    }

    if (openMenus === undefined) {
        // Get open sub menus of first level.
        openMenus = document.querySelectorAll("#site-navigation .menu-item-has-children.opened");
    }

    if (openMenus.length === 0) {
        return;
    }

    for (var i = 0; i < openMenus.length; i++) {
        openMenu = openMenus[i];
        if (openMenu === menuListItem) {
            continue;
        }

        toggleSubMenu(openMenu.querySelector(".sub-menu-expand"));
    }
}

/**
 * Close open sub menus.
 */
function closeSubMenus() {
    var openSubMenus = document.querySelectorAll("#site-navigation .menu-item-has-children.opened");
    if (openSubMenus.length === 0) {
        return;
    }

    for (var i = 0; i < openSubMenus.length; i++) {
        openMenu = openSubMenus[i];

        toggleSubMenu(openMenu.querySelector(".sub-menu-expand"));
    }
}