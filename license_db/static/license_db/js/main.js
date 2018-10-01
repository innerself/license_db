const searchArea = $("#search-area");
const licenseRows = $(".lic-group-item");

const btnExpand = $("#expand-all");
const btnCollapse = $("#collapse-all");
// const categoryBtn = $(".lic-category-button");
// const locationBtn = $(".lic-location-button");
const categoryContainer = $(".view-category-container");
const licenseGroup = $(".license-group");

function rowHasText(row, text) {
  let hasText = false;
  const searchText = text.toLowerCase();

  row.children().each(function () {
    const childText = $(this).text().toLowerCase();

    if (childText.indexOf(searchText) > -1) {
      hasText = true;
      return false  // this is for 'break'
    }
  });

  return hasText
}

function locationIsVisible(location) {
  return location.children('.lic-group-item').is(':visible');
}

function hideLocation(location) {
  const locationId = location.attr('id');
  const locationBtn = $('[data-target="#' + locationId + '"]');
  const locationGroup = $('#' + locationId);

  locationGroup.hide();
  locationBtn.hide();

  return null
}

function showLocation(location) {
  const locationId = location.attr('id');
  const locationBtn = $('[data-target="#' + locationId + '"]');
  const locationGroup = $('#' + locationId);

  // locationGroup.show();
  // locationBtn.show();

  locationGroup.removeAttr('style');
  locationBtn.removeAttr('style');

  return null
}

// $(document).ready(function () {
//   licenseRows.hide();
// });

searchArea.on("input", function () {
  const currentSearch = $(this).val();

  licenseRows.each(function () {
    const currentRow = $(this);
    const currentLocation = currentRow.parent();

    if (rowHasText(currentRow, currentSearch)) {
        // currentRow.show();
      currentRow.removeAttr('style');
      showLocation(currentLocation);
      // }

      // TODO Highlight found text in the row (make red)
    } else {
      currentRow.hide();
      // currentRow.addClass('collapsed');

      if (!locationIsVisible(currentLocation)) {
        hideLocation(currentLocation);
      }
    }
  })
});

btnExpand.click(function () {
  categoryContainer.each(function () {
    if (!($(this).is(':visible'))) {
      const categoryId = $(this).attr('id');
      const categoryBtn = $('[data-target="#' + categoryId + '"]');

      categoryBtn.click();
    }
  });

  setTimeout(function () {
    licenseGroup.each(function () {
      if (!($(this).is(':visible'))) {
        const locationId = $(this).attr('id');
        const locationBtn = $('[data-target="#' + locationId + '"]');

        locationBtn.click();
      }
    });
  }, 350)
});

btnCollapse.click(function () {
  licenseGroup.each(function () {
    if ($(this).is(':visible')) {
      const locationId = $(this).attr('id');
      const locationBtn = $('[data-target="#' + locationId + '"]');

      locationBtn.click();
    }
  });

  setTimeout(function () {
    categoryContainer.each(function () {
      if ($(this).is(':visible')) {
        const categoryId = $(this).attr('id');
        const categoryBtn = $('[data-target="#' + categoryId + '"]');

        categoryBtn.click();
      }
    });
  }, 350)
});

