const searchArea = $("#search-area");
const licenseRows = $(".lic-group-item");

const btnExpand = $("#expand-all");
const btnCollapse = $("#collapse-all");
const groupBtn = $(".lic-type-button");

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

searchArea.on("input", function () {
  const currentSearch = $(this).val();

  licenseRows.each(function () {
    const currentRow = $(this);

    if (rowHasText($(this), currentSearch)) {
      currentRow.show()
    } else {
      currentRow.hide()
    }
  })
});

btnExpand.click(function () {
  groupBtn.each(function () {
    if ($(this).hasClass("collapsed")) {
      $(this).click()
    }
  })
});

btnCollapse.click(function () {
  groupBtn.each(function () {
    if (!($(this).hasClass("collapsed"))) {
      $(this).click()
    }
  })
});

