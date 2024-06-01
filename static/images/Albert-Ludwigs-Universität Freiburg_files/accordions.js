
'use strict';

/* Instead of searching for every accordion – what creates problems in AJAX, this function waits for clicks on accordion elements */
jQuery(function ($) {
    $(document).on('click', '.accordion-item__button', function () {
        var target = $(this)[0];
        var accordion = $(target).closest('.accordion')[0];

        // Allow for multiple accordion sections to be expanded at the same time
        var allowMultiple = accordion.getAttribute('data-allowmultiple') == 'true';

        // Allow for each toggle to both open and close individually
        var allowToggle = 'true';

        // Check if the current toggle is expanded.
        var isExpanded = target.getAttribute('aria-expanded') == 'true';
        var active = accordion.querySelector('[aria-expanded="true"]');

        // without allowMultiple, close the open accordion
        if (!allowMultiple && active && active !== target) {
            // Set the expanded state on the triggering element
            active.setAttribute('aria-expanded', 'false');
            // Hide the accordion sections, using aria-controls to specify the desired section
            document.getElementById(active.getAttribute('aria-controls')).setAttribute('hidden', '');

            // When toggling is not allowed, clean up disabled state
            if (!allowToggle) {
                active.removeAttribute('aria-disabled');
            }
        }

        if (!isExpanded) {
            // Set the expanded state on the triggering element
            target.setAttribute('aria-expanded', 'true');
            // Hide the accordion sections, using aria-controls to specify the desired section
            document.getElementById(target.getAttribute('aria-controls')).removeAttribute('hidden');

            // If toggling is not allowed, set disabled state on trigger
            if (!allowToggle) {
                target.setAttribute('aria-disabled', 'true');
            }
        } else if (allowToggle && isExpanded) {
            // Set the expanded state on the triggering element
            target.setAttribute('aria-expanded', 'false');
            // Hide the accordion sections, using aria-controls to specify the desired section
            document.getElementById(target.getAttribute('aria-controls')).setAttribute('hidden', '');
        }
    })
});

/* This is the legacy function to optimise a11y */
function optimizeAccordionA11y() {
    Array.prototype.slice.call(document.querySelectorAll('.accordion')).forEach(function (accordion) {

        // Bind keyboard behaviors on the main accordion container
        accordion.addEventListener('keydown', function (event) {
            var target = event.target;
            var key = event.which.toString();

            // 33 = Page Up, 34 = Page Down
            var ctrlModifier = (event.ctrlKey && key.match(/33|34/));

            // Is this coming from an accordion header?
            if (target.classList.contains('accordion-item__button')) {
                // Up/ Down arrow and Control + Page Up/ Page Down keyboard operations
                // 38 = Up, 40 = Down
                if (key.match(/38|40/) || ctrlModifier) {
                    var index = triggers.indexOf(target);
                    var direction = (key.match(/34|40/)) ? 1 : -1;
                    var length = triggers.length;
                    var newIndex = (index + length + direction) % length;

                    triggers[newIndex].focus();

                    event.preventDefault();
                } else if (key.match(/35|36/)) {
                    // 35 = End, 36 = Home keyboard operations
                    switch (key) {
                        // Go to first accordion
                        case '36':
                            triggers[0].focus();
                            break;
                        // Go to last accordion
                        case '35':
                            triggers[triggers.length - 1].focus();
                            break;
                    }
                    event.preventDefault();

                }

            }
        });

        // These are used to style the accordion when one of the buttons has focus
        accordion.querySelectorAll('.accordion-item__button').forEach(function (trigger) {

            trigger.addEventListener('focus', function (event) {
                accordion.classList.add('focus');
            });

            trigger.addEventListener('blur', function (event) {
                accordion.classList.remove('focus');
            });

        });

    });
}

function checkForSearchTerms() {
    var urlParams = new URLSearchParams(window.location.search);
    if (!urlParams.has('search-phrase')) {
        return;
    }

    var accordions = document.querySelectorAll('.entry-content .accordion-item');
    if (accordions.length === 0) {
        return;
    }

    var searchTerms = urlParams.get('search-phrase').trim().toLowerCase().split(' ');
    if (searchTerms.length === 0) {
        return;
    }

    // Filter out stopwords.
    searchTerms = searchTerms.filter(function(word) {
        return !unifreiburgStopwords.includes(word.trim());
    });

    for (var i = 0; i < accordions.length; i++) {
        var accordion = accordions[i],
            accordionContent = accordion.querySelector('.accordion-item__content').innerHTML.toLowerCase(),
            found = false;

        for (var j = 0; j < searchTerms.length; j++) {
            if (accordionContent.indexOf(searchTerms[j].trim()) === -1) {
                continue;
            }
            found = true;
        }

        if (!found) {
            continue;
        }

        var accordionButton = accordion.querySelector('.accordion-item__button');
        if (accordionButton.getAttribute('aria-expanded') == 'true') {
            break;
        }

        // Check for data-allowmultiple="false".
        if (accordion.parentNode.getAttribute('data-allowmultiple') == 'false') {
            accordion.parentNode.setAttribute('data-allowmultiple', 'true');
        }

        accordionButton.click();
    }
}

window.addEventListener('hashchange', openAccordionByUrlHash );
function openAccordionByUrlHash() {
    var hash = location.hash.substring(1);
    if (hash === '') {
        return;
    }
    var elem = document.getElementById(hash);
    if (!elem) {
        return;
    }

    if (!elem.classList.contains('accordion-item')) {
        return;
    }

    var button = elem.querySelector('button');
    if (button.getAttribute('aria-expanded') == 'true') {
        return;
    }

    button.click();
    button.focus();
}

jQuery(document).ready(function () {
    // optimise a11y after page load
    optimizeAccordionA11y();
    openAccordionByUrlHash();
})
jQuery(document).ajaxComplete(function () { optimizeAccordionA11y(); });   // optimise a11y after ajax calls
jQuery(document).ready(function () { checkForSearchTerms() })              // Open accordions with search terms when user comes from search page.