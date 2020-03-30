function start(authenticated, NewestRecipePages, PopularRecipePages, recipe_pagination) {   
            // set up of the initial look
            $("button.previous").attr("disabled", true);
            var RecipesPerPage = "3"; // set globally
            var author = "#"; // also global; we are on the homepage, so profile author is not specified
            var which = "newest";
            var nextPageNumber = 1; // this is on load up obviously the first page
            var page = nextPageNumber.toString();
            var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
            var element = "div.row#newest";
            var url = recipe_pagination;
            if (authenticated=="True") { // if the user is authenticated, then he can save the recipes, so we need buttons
                var buttons = "yes";
            }
            else {
                var buttons = "";
            }
            if (nextPageNumber == NewestRecipePages || NewestRecipePages==0) { // if we are on the only page, there is no next
                $("button.next#newest").attr("disabled", true);
            }
            $("em#NewestRecipePage").text("   " + page + "   "); // set the page counter
            RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);

            which = "popular";
            element = "div.row#popular";
            if (nextPageNumber == PopularRecipePages || PopularRecipePages==0) { // if we are on the only page, there is no next
                $("button.next#popular").attr("disabled", true);
            }
            $("em#PopularRecipePage").text("   " + page + "   "); // set the page counter
            RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);


            // retrieve next "Newest Recipes" page
            $("button.next#newest").click(function () {
                var which = "newest";
                var nextPageNumber = parseInt($("em#NewestRecipePage").html().replace(/ /g, ''), 10) + 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#newest";
                var url = recipe_pagination;
                var buttons = "yes";
                $("button.previous#newest").attr("disabled", false);
                if (nextPageNumber == NewestRecipePages) { // next disabled if we reach the last page
                    $("button.next#newest").attr("disabled", true);
                }
                $("em#NewestRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
                RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
            });

            // retrieve previous "Newest Recipes" page
            $("button.previous#newest").click(function () {
                var which = "newest";
                var nextPageNumber = parseInt($("em#NewestRecipePage").html().replace(/ /g, ''), 10) - 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#newest";
                var url = recipe_pagination;
                var buttons = "yes";
                $("button.next#newest").attr("disabled", false);
                if (nextPageNumber == 1) { // if we are on the first page again
                    $("button.previous#newest").attr("disabled", true);
                }
                $("em#NewestRecipePage").text("   " + page + "   "); // update the page counter as long as there are previous pages
                RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
            });

            // retrieve next "Popular Recipes" page
            $("button.next#popular").click(function () {
                var which = "popular";
                var nextPageNumber = parseInt($("em#PopularRecipePage").html().replace(/ /g, ''), 10) + 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#popular";
                var url = recipe_pagination;
                var buttons = "yes";
                $("button.previous#popular").attr("disabled", false);
                if (nextPageNumber == PopularRecipePages) { // next disabled if we reach the last page
                    $("button.next#popular").attr("disabled", true);
                }
                $("em#PopularRecipePage").text("   " + page + "   "); // update the page counter
                RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
            });

            // retrieve previous "Popular Recipes" page
            $("button.previous#popular").click(function () {
                var which = "popular";
                var nextPageNumber = parseInt($("em#PopularRecipePage").html().replace(/ /g, ''), 10) - 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#popular";
                var url = recipe_pagination;
                var buttons = "yes";
                $("button.next#popular").attr("disabled", false);
                if (nextPageNumber == 1) {  // if we are on the first page again
                    $("button.previous#popular").attr("disabled", true);
                }
                $("em#PopularRecipePage").text("   " + page + "   ");  // update the page counter as long as there are previous pages
                RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
            });
}