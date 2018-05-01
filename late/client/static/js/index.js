let searchButton = $("#srch-btn");
let searchBar = $("#srch-bar");
let searchBarInput = searchBar.children()[0]
searchButton.click(function() {
	searchBarInput.value = "";
    searchBar.toggleClass("search-bar-hidden");
    searchBarInput.focus();
});

