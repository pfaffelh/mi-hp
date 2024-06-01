/* global unifreiburgPrintString */
window.addEventListener("DOMContentLoaded", function() {
    var breadcrumb = document.querySelector(".site-breadcrumb"),
        printFooterWrapper = document.querySelector(".print-view-footer");
    if (!breadcrumb) {
        return;
    }

    addPrintActionButtons();

    createLinkList(printFooterWrapper);
});

/**
 * Adds print button and cancel button to page.
 */
function addPrintActionButtons() {
    // Add button before #primary.
    var printButtonContainer = document.createElement("div"),
        printButton = document.createElement("button"),
        cancelButton = document.createElement("button"),
        primaryContainer = document.getElementById("primary"),
        screenReaderSpan = document.createElement("span"),
        iconSpan = document.createElement("span");

    if (!primaryContainer) {
        return;
    }

    printButtonContainer.classList.add("print-button-wrapper");

    printButton.classList.add("print-button", "raised");

    screenReaderSpan.textContent = unifreiburgPrintString.print;
    screenReaderSpan.classList.add("screen-reader-text");

    printButton.appendChild(screenReaderSpan);

    iconSpan.classList.add("fa-print");

    printButton.appendChild(iconSpan);

    printButtonContainer.appendChild(printButton);
    
    primaryContainer.parentNode.insertBefore(printButtonContainer, primaryContainer);

    cancelButton.classList.add("cancel-print-button");
    cancelButton.textContent = unifreiburgPrintString.cancel;
    primaryContainer.parentNode.insertBefore(cancelButton, primaryContainer);

    printButton.addEventListener("click", function() {
        var html = document.querySelector("html");

        // Check if we are already in the print template view.
        if (html.classList.contains("print-template")) {
            window.print();
            return;
        }
        document.querySelector("html").classList.add("print-template");

        toggleLinkHrefAttribute();
        addHideImageButtons();
    });

    cancelButton.addEventListener("click", exitPrintTemplate);
}

/**
 * Add link list after content.
 * 
 * @param {Node} footerWrapper 
 */
function createLinkList(footerWrapper) {
    var links = document.querySelectorAll("#primary a, #secondary a");
    if (links.length === 0) {
        return;
    }

    // Add links list to #primary.
    var linkListHeading = document.createElement("h2"),
        linkList = document.createElement("ol"),
        linkItemTmpl = document.createElement("li"),
        sourceParagraph = footerWrapper.querySelector("p");

    linkListHeading.classList.add("print-view-link-list-heading");
    linkListHeading.textContent = unifreiburgPrintString.linkListLabel;

    linkList.classList.add("print-view-link-list");

    footerWrapper.insertBefore(linkListHeading, sourceParagraph);
    footerWrapper.insertBefore(linkList, sourceParagraph);

    for (var i = 0; i < links.length; i++) {
        var link = links[i]
            listItem = linkItemTmpl.cloneNode(true);

        listItem.textContent = link.getAttribute("href");
        linkList.appendChild(listItem);
    }
}

/**
 * Exit the print template again.
 */
function exitPrintTemplate() {
    toggleLinkHrefAttribute();

    document.querySelector("html").classList.remove("print-template");

    removeHideImageButtons();
}

/**
 * If we are in the print view, we replace the `href` attr of links with `data-href`,
 * so that the links are not clickable and do not break the hide image buttons.
 */
function toggleLinkHrefAttribute() {
    var links = document.querySelectorAll("#content a, #secondary a");
    
    if (links.length === 0) {
        return;
    }

    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        if (link.getAttribute("data-href")) {
            link.setAttribute("href", link.getAttribute("data-href"));
            link.removeAttribute("data-href");
            continue;
        }

        link.setAttribute("data-href", link.getAttribute("href"));
        link.removeAttribute("href");
    }
}

/**
 * Remove the hide image buttons.
 */
function removeHideImageButtons() {
    var hideImageButtons = document.querySelectorAll(".hide-image-for-print-button");
    if (!hideImageButtons) {
        return;
    }

    for (var i = 0; i < hideImageButtons.length; i++) {
        hideImageButtons[i].remove();
    }
}

/**
 * Adds buttons to images to hide them in print view.
 */
function addHideImageButtons() {
    // Get all images in #primary.
    var images = document.querySelectorAll("#primary img, #secondary img");
    if (images.length === 0) {
        // No images.
        return;
    }

    var hideButtonTmpl = document.createElement("button"),
        hideImageSpan = document.createElement("span"),
        showImageSpan = document.createElement("span"),
        wrapperTmpl = document.createElement("div");

    hideButtonTmpl.classList.add("hide-image-for-print-button", "raised");
    hideImageSpan.textContent = unifreiburgPrintString.hideImage;
    hideImageSpan.classList.add("hide-image-text");
    showImageSpan.textContent = unifreiburgPrintString.showImage;
    showImageSpan.classList.add("show-image-text");
    hideButtonTmpl.appendChild(hideImageSpan);
    hideButtonTmpl.appendChild(showImageSpan);

    wrapperTmpl.classList.add("print-template-img-wrapper");

    for (var i = 0; i < images.length; i++) {
        var image = images[i],
            hideButton = hideButtonTmpl.cloneNode(true);

        // Add button to figure element.
        image.parentNode.insertBefore(hideButton, image);
        addHideButtonEventListener(hideButton);
    }
}

/**
 * Add event listener to hide button.
 * 
 * @param {Node} button The hide button node. 
 */
function addHideButtonEventListener(button) {
    button.addEventListener("click", function(e) {
        e.stopPropagation();
        var button = this,
            image = button.parentNode.querySelector("img"),
            entryHeader = button.closest(".entry-header"),
            cardImageContainer = button.closest(".card__image");

        if (!image) {
            return;
        }

        button.classList.toggle("is-active");
        image.classList.toggle("hide-image-for-print");

        if (entryHeader) {
            entryHeader.classList.toggle("post-thumbnail-is-hidden");
        }

        if (cardImageContainer) {
            cardImageContainer.classList.toggle("card-image-is-hidden");
        }
    })
}