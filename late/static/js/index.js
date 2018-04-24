let searchButton = $("#srch-btn");
let searchBar = $("#srch-bar");
searchButton.click(function() {
	console.log("dude")
	searchBar.toggleClass("search-bar-hidden");
});