/**
 * Search form Metaheader
 */


// Show search
function showSearchField() { // the final push + re-run
  (function ($) {
    $('body:not(.search) .site-search-form').toggleClass('search-visible');
    $('body:not(.search) .site-search-button').toggleClass('search-visible');
    if ($('.site-search-button').hasClass('search-visible')) {
      if ($('body').hasClass('language-selection-visible')) {
        $('body').removeClass('language-selection-visible');
      }
      // this function is for foucssing the input on iOS with keyboard
      // Source: https://stackoverflow.com/a/55652503

      console.log('TEST');

      // create invisible dummy input to receive the focus first
      const fakeInput = document.createElement('input')
      fakeInput.setAttribute('type', 'text')
      fakeInput.style.position = 'absolute'
      fakeInput.style.opacity = 0
      fakeInput.style.height = 0
      fakeInput.style.fontSize = '16px' // disable auto zoom

      // you may need to append to another element depending on the browser's auto 
      // zoom/scroll behavior
      document.body.prepend(fakeInput)

      // focus so that subsequent async focus will work
      fakeInput.focus()

      setTimeout(() => {

        // now we can focus on the target input
        $('.site-search-form .search-field').focus()

        // cleanup
        fakeInput.remove()

      }, 500);
    } else if ($('body').hasClass('search')) {
      $('.site-search-form .search-field').focus()
    } else {
      $('.site-search-button').focus();
    }
  })(jQuery);
}

(function ($) {

  // needed to prevent the search to be displayed directly again
  // if the search field has focus and then the user clicks on the search button again.
  let preventShow = false,
    clickedButton = null;
  $(document).ready(function () {
    const searchButtons = document.querySelectorAll('.site-search-button'),
      searchFormWrapper = document.getElementById('site-search-form');
    if (searchButtons.length === 0 || !searchFormWrapper) {
      return;
    }

    /* Show Search Form when search link is clicked */
    document.querySelector('body').addEventListener('click', function (e) {
      const target = e.target;
      let buttonClicked = false;
      searchButtons.forEach(function(button) {
        if (target !== button && !button.contains(target)) {
          return;
        }

        buttonClicked = true;
        clickedButton = button;
      })

      if (preventShow) {
        preventShow = false;
        return;
      }

      if (searchFormWrapper.contains(target) || searchFormWrapper === target) {
        return;
      }

      if (!buttonClicked && document.querySelector('.site-search-form.search-visible')) {
        $('.site-search-form, .site-search-button.search-visible').toggleClass('search-visible');
        return;
      }

      if (buttonClicked && document.querySelector('.site-search-form.search-visible')) {
        $('.site-search-form, .site-search-button.search-visible').toggleClass('search-visible');
        return;
      }

      if (buttonClicked) {
        showSearchField();
      }
    });

    // Close meta search on escape key
    document.addEventListener('keydown', function (e) {
      if (document.querySelector('body:not(.search) .site-search-form.search-visible')) {
        var key = e.which || e.keyCode;

        if (key === 27) { // 27 is esc
          $('.site-search-form, .site-search-button.search-visible').toggleClass('search-visible');
        }
      }
    }, false);

    // Listen for focus leaving the search form area and move it back to the search button.
    if (searchFormWrapper) {
      searchFormWrapper.addEventListener('focusout', function(e) {
        e.stopPropagation();
        const relatedTarget = e.relatedTarget ? e.relatedTarget : null;
        if (relatedTarget === null) {
          return;
        }

        if (searchFormWrapper.contains(relatedTarget)) {
          return;
        }

        // We need that check, because the focusout event is also fired if the user clicks outside the
        // search field area. If he clicks the button again, the focusout and click event are fired, so
        // we need to prevent that the field is hidden from `focusout` and instantly shown by `click` again.
        if (relatedTarget.classList.contains('site-search-button')) {
          preventShow = true;
          window.setTimeout(function() {
            preventShow = false;
          }, 200);
        }

        clickedButton.focus();

        $('.site-search-form, .site-search-button.search-visible').toggleClass('search-visible');
      })
    }
  });

})(jQuery);