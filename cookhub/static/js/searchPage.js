function search(csrf_token, authenticated, recipePages, recipe_pagination, categoriesSTR) {
    // load initial recipes for search
    $("button.previous").attr("disabled", true);
    $("button.first").attr("disabled", true);
    let recipesPerPage = "6";
    let author = "#"; // TODO: add dynamic authors
    let which = "search";
    let nextPageNum = 1; // load the page on the first page
    let single = "0";
    let element = "div.row#search";
    let url = recipe_pagination;
    let buttons = "";
    let categories = categoriesSTR;

    console.log(categories);

    // if the user is authenticated, then he can save the recipes, so we need buttons
    if (authenticated == "True") {
        buttons = "yes";
    }

    // if we are on the only page, there is no next
    if (nextPageNum == recipePages || recipePages == 0) {
        $("button.first#search").attr("disabled", true);
        $("button.previous#search").attr("disabled", true);
        $("button.next#search").attr("disabled", true);
        $("button.last#search").attr("disabled", true);
    }

    // set page counter
    $("em#SearchRecipePage").text("   " + nextPageNum.toString() + "   ");
    RecipeGetter(csrf_token, recipesPerPage, author, which, nextPageNum.toString(), single, element, url, buttons, null, categories);


    // retrieve last "Search Recipes" page
    $("button.last#search").click(function () {
        let nextPageNumber = recipePages;
        let page = nextPageNumber.toString();
        let single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
        let element = "div.row#search";
        $("button.first#search").attr("disabled", false); // we could click on "last",
        $("button.previous#search").attr("disabled", false); // so there is a "previous" and "first"
        $("button.next#search").attr("disabled", true); // we are on the last page,
        $(this).attr("disabled", true);                 // so there is no next or last anymore
        $("em#SearchRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
        RecipeGetter(csrf_token, recipesPerPage, author, which, page, single, element, url, buttons, null, categories);
    });

    // retrieve next "Search Recipes" page
    $("button.next#search").click(function () {
        let nextPageNumber = parseInt($("em#SearchRecipePage").html().replace(/ /g, ''), 10) + 1;
        let page = nextPageNumber.toString();
        let single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
        let element = "div.row#search";
        $("button.previous#search").attr("disabled", false); // we could click on "next",
        $("button.first#search").attr("disabled", false); // so there is a "previous" and "first"
        if (nextPageNumber == recipePages) { // "next" and "first" disabled if we reach the last page
            $("button.next#search").attr("disabled", true);
            $("button.last#search").attr("disabled", true);
        }
        $("em#SearchRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
        RecipeGetter(csrf_token, recipesPerPage, author, which, page, single, element, url, buttons, null, categories);
    });

    // retrieve previous "Search Recipes" page
    $("button.previous#search").click(function () {
        let nextPageNumber = parseInt($("em#SearchRecipePage").html().replace(/ /g, ''), 10) - 1;
        let page = nextPageNumber.toString();
        let single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
        let element = "div.row#search";
        $("button.last#search").attr("disabled", false);
        $("button.next#search").attr("disabled", false);
        if (nextPageNumber == 1) { // if we are on the first page again
            $("button.previous#search").attr("disabled", true);
            $("button.first#search").attr("disabled", true);
        }
        $("em#SearchRecipePage").text("   " + page + "   "); // update the page counter as long as there are previous pages
        RecipeGetter(csrf_token, recipesPerPage, author, which, page, single, element, url, buttons, null, categories);
    });

    // retrieve first "Search Recipes" page
    $("button.first#search").click(function () {
        let nextPageNumber = 1; // go to the first page
        let page = "1";
        let single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
        let element = "div.row#search";
        $(this).attr("disabled", true); // we are already on the first page
        $("button.previous#search").attr("disabled", true); // disable "previous", we are already on the first page
        $("button.next#search").attr("disabled", false);     // we could click on "first", so there is a next
        $("button.last#search").attr("disabled", false);    // and a last, too
        $("em#SearchRecipePage").text("   " + page + "   "); // update the page counter as long as there are previous pages
        RecipeGetter(csrf_token, recipesPerPage, author, which, page, single, element, url, buttons, null, categories);
    });
}