(function(){
  const languageButtons = document.querySelectorAll('.site-header .language-button'),
    languageSelectionArea = document.getElementById('language-selection');
  let preventShow = false;
  if (languageButtons.length === 0 || !languageSelectionArea) {
    return;
  }

  /**
   * Toggles aria-hidden on the selection area and tabindex="-1" on the language links.
   */
  function toggleScreenReaderVisibility() {
    const newAriaHiddenValue = languageSelectionArea.getAttribute('aria-hidden') == 'true' ? 'false' : 'true',
      languageItems = languageSelectionArea.querySelectorAll('.language-switcher > *');

    languageSelectionArea.setAttribute('aria-hidden', newAriaHiddenValue);

    if (!languageItems) {
      return;
    }

    languageItems.forEach(function(item) {
      if (newAriaHiddenValue == 'false') {
        item.setAttribute('tabindex', '0');
      } else {
        item.setAttribute('tabindex', '-1');
      }
    })
  }

  toggleScreenReaderVisibility();

  let clickedSearchButton = null;

  const body = document.querySelector('body'),
    visibleHintClass = 'language-selection-visible';

  body.addEventListener('click', function(e) {
    const target = e.target;
    let buttonClicked = false;
    languageButtons.forEach(function(button) {
      if (target !== button && !button.contains(target)) {
        return;
      }

      buttonClicked = true;

      if (preventShow) {
        preventShow = false;
        return;
      }

      clickedSearchButton = button;
      body.classList.toggle(visibleHintClass);
      toggleScreenReaderVisibility();

      if (body.classList.contains(visibleHintClass)) {
        const searchElems = document.querySelectorAll('#site-search-form.search-visible, .site-search-button.search-visible');
        if (searchElems.length !== 0) {
          searchElems.forEach(function(elem) {
            elem.classList.remove('search-visible');
          })
        }

        // Move focus to first item in language selection.
        languageSelectionArea.querySelector('.language-switcher > :first-child').focus();
      }
    })

    if (buttonClicked) {
      return;
    }

    if (languageSelectionArea.contains(target)) {
      return;
    }

    if (body.classList.contains(visibleHintClass)) {
      body.classList.remove(visibleHintClass);

      clickedSearchButton.focus();

      toggleScreenReaderVisibility();
    }
  })

  // Listen for focus leaving the language selection area and move it back to the search button.
  languageSelectionArea.addEventListener('focusout', function(e) {
    e.stopPropagation();
    const relatedTarget = e.relatedTarget ? e.relatedTarget : null;
    if (relatedTarget === null) {
      return;
    }

    if (languageSelectionArea.contains(relatedTarget)) {
      return;
    }

    // We need that check, because the focusout event is also fired if the user clicks outside the
    // language buttons area. If he clicks the lang button again, the focusout and click event are fired, so
    // we need to prevent that the field is hidden from `focusout` and instantly shown by `click` again.
    if (relatedTarget.classList.contains('language-button')) {
      preventShow = true;
      window.setTimeout(function() {
        preventShow = false;
      }, 200);
    }

    body.classList.remove(visibleHintClass);

    clickedSearchButton.focus();

    toggleScreenReaderVisibility();
  })

  document.addEventListener('keydown', function (e) {
    const key = e.which || e.keyCode;
    if (key !== 27) {
      return;
    }

    if (body.classList.contains(visibleHintClass) && clickedSearchButton) {
      body.classList.remove(visibleHintClass);
      clickedSearchButton.focus()
      toggleScreenReaderVisibility();
    }
  }, false);
}());