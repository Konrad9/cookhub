function searchquery(csrf_token, authenticated, recipe_pagination, RecipesPerPage, query, NumberOfPages) {
    $("button.previous").attr("disabled", true);
    $("button.first").attr("disabled", true);
    var RecipesPerPage = RecipesPerPage; // set globally
    var author = "#"; // also global;
    var which = "query";
    var nextPageNumber = 1; // this is on load up obviously the first page
    var page = "1";
    var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
    var element = "div.row#results";
    var url = recipe_pagination;
    var NumberOfPages = NumberOfPages;
    if (authenticated=="True") { // if the user is authenticated, then he can save the recipes, so we need buttons
        var buttons = "yes";
    }
    else {
        var buttons = "";
    }
    var attributes = query;
    if (nextPageNumber >= NumberOfPages) { // if we are on the only page, there is no next
        console.log(nextPageNumber, NumberOfPages);
        $("button.first#results").attr("disabled", true);
        $("button.previous#results").attr("disabled", true);
        $("button.next#results").attr("disabled", true);
        $("button.last#results").attr("disabled", true);
    }
    $("em#ResultsRecipePage").text("   " + page + "   "); // set the page counter
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);


            var which = "query"; // setting the variable for the section of "newest" buttons
            // retrieve last page
            $("button.last#results").click(function () {
                var nextPageNumber = NumberOfPages;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#results";
                $("button.first#results").attr("disabled", false); // we could click on "last", 
                $("button.previous#results").attr("disabled", false); // so there is a "previous" and "first"
                $("button.next#results").attr("disabled", true); // we are on the last page,
                $(this).attr("disabled", true);                 // so there is no next or last anymore
                $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
            });
            
            // retrieve next page
            $("button.next#results").click(function () {
                var nextPageNumber = parseInt($("em#ResultsRecipePage").html().replace(/ /g, ''), 10) + 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#results";
                $("button.previous#results").attr("disabled", false); // we could click on "next", 
                $("button.first#results").attr("disabled", false); // so there is a "previous" and "first"
                if (nextPageNumber == NumberOfPages) { // "next" and "first" disabled if we reach the last page
                    $("button.next#results").attr("disabled", true);
                    $("button.last#results").attr("disabled", true);
                }
                $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
            });
            
            // retrieve previous page
            $("button.previous#results").click(function () {
                var nextPageNumber = parseInt($("em#ResultsRecipePage").html().replace(/ /g, ''), 10) - 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#results";
                $("button.last#results").attr("disabled", false);
                $("button.next#results").attr("disabled", false);
                if (nextPageNumber == 1) { // if we are on the first page again
                    $("button.previous#results").attr("disabled", true);
                    $("button.first#results").attr("disabled", true);
                }
                $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are previous pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
            });
            
            // retrieve first page
            $("button.first#results").click(function () {
                var nextPageNumber = 1; // go to the first page
                var page = "1";
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#results";
                $(this).attr("disabled", true); // we are already on the first page
                $("button.previous#results").attr("disabled", true); // disable "previous", we are already on the first page
                $("button.next#results").attr("disabled", false);     // we could click on "first", so there is a next
                $("button.last#results").attr("disabled", false);    // and a last, too
                $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are previous pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
            });
 }
 
 function addIngredient() {
    var text = document.getElementById("ingredientInput").value;
    $("ul#ingredientList").append("<li>"+ text + "</li>");
    document.getElementById("ingredientInput").value = "";
} 

function clearFilters() {
    console.log($("input.catCheckbox"));
    $("input").removeAttr("checked");
    $("input#ratingSlider").val("0");
    $("em#sliderValue").html("0.0");
    $("ul#ingredientList").html("");
}     

 // Update the current slider value (each time you drag the slider handle)
function sliderFunction() {
    var slider = document.getElementById("ratingSlider");
    var output = document.getElementById("sliderValue");
    output.innerHTML = (slider.value/10).toString();
} 

function searchfiltered(csrf_token, authenticated, recipe_pagination, RecipesPerPage, query, NumberOfPages, checkedBoxes, rating, ingredients) {
    console.log(checkedBoxes);
    var author = "#";
    var which = "filtered";
    var nextPageNumber = 1;
    var page = 1;
    var single = "1";
    var element = "div.row#results";
    var url = recipe_pagination;
    if (authenticated=="True") { // if the user is authenticated, then he can save the recipes, so we need buttons
        var buttons = "yes";
    }
    else {
        var buttons = "";
    }
   // RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
    $.ajax({
        url: recipe_pagination, 
        data: {"csrfmiddlewaretoken": csrf_token, "attributes": JSON.stringify({"query": query, "rating": rating,"ingredients": ingredients})},
        type: "post",
        success: function(data) {
            console.log(data);
        }
        });
}