function start(csrf_token, authenticated, NewestRecipePages, PopularRecipePages, recipe_pagination, RecipesPerPage) {   
            // set up of the initial look
            $("button.previous").attr("disabled", true);
            $("button.first").attr("disabled", true);
            var RecipesPerPage = RecipesPerPage; // set globally
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
                $("button.first#newest").attr("disabled", true);
                $("button.previous#newest").attr("disabled", true);
                $("button.next#newest").attr("disabled", true);
                $("button.last#newest").attr("disabled", true);
            }
            $("em#NewestRecipePage").text("   " + page + "   "); // set the page counter
            RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            

            which = "popular";
            element = "div.row#popular";
            if (nextPageNumber == PopularRecipePages || PopularRecipePages==0) { // if we are on the only page, there is no next
                $("button.first#popular").attr("disabled", true);
                $("button.previous#popular").attr("disabled", true);
                $("button.next#popular").attr("disabled", true);
                $("button.last#popular").attr("disabled", true);
            }
            $("em#PopularRecipePage").text("   " + page + "   "); // set the page counter
            RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            
            setTimeout(function after() {
                console.log("n is now: " + n);
            }, 500)
            
            // retrieve last "Newest Recipes" page
            $("button.last#newest").click(function () {
                var nextPageNumber = NewestRecipePages;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#newest";
                var which = "newest";
                $("button.first#newest").attr("disabled", false); // we could click on "last", 
                $("button.previous#newest").attr("disabled", false); // so there is a "previous" and "first"
                $("button.next#newest").attr("disabled", true); // we are on the last page,
                $(this).attr("disabled", true);                 // so there is no next or last anymore
                $("em#NewestRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });
            
            // retrieve next "Newest Recipes" page
            $("button.next#newest").click(function () {
                var nextPageNumber = parseInt($("em#NewestRecipePage").html().replace(/ /g, ''), 10) + 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#newest";
                var which = "newest";
                $("button.previous#newest").attr("disabled", false); // we could click on "next", 
                $("button.first#newest").attr("disabled", false); // so there is a "previous" and "first"
                if (nextPageNumber == NewestRecipePages) { // "next" and "first" disabled if we reach the last page
                    $("button.next#newest").attr("disabled", true);
                    $("button.last#newest").attr("disabled", true);
                }
                $("em#NewestRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });
            
            // retrieve previous "Newest Recipes" page
            $("button.previous#newest").click(function () {
                var nextPageNumber = parseInt($("em#NewestRecipePage").html().replace(/ /g, ''), 10) - 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#newest";
                var which = "newest";
                $("button.last#newest").attr("disabled", false);
                $("button.next#newest").attr("disabled", false);
                if (nextPageNumber == 1) { // if we are on the first page again
                    $("button.previous#newest").attr("disabled", true);
                    $("button.first#newest").attr("disabled", true);
                }
                $("em#NewestRecipePage").text("   " + page + "   "); // update the page counter as long as there are previous pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });
            
            // retrieve first "Newest Recipes" page
            $("button.first#newest").click(function () {
                var nextPageNumber = 1; // go to the first page
                var page = "1";
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#newest";
                var which = "newest";
                $(this).attr("disabled", true); // we are already on the first page
                $("button.previous#newest").attr("disabled", true); // disable "previous", we are already on the first page
                $("button.next#newest").attr("disabled", false);     // we could click on "first", so there is a next
                $("button.last#newest").attr("disabled", false);    // and a last, too
                $("em#NewestRecipePage").text("   " + page + "   "); // update the page counter as long as there are previous pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });
            
            // retrieve last "Popular Recipes" page
            $("button.last#popular").click(function () {
                var nextPageNumber = PopularRecipePages;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#popular";
                var which = "popular";
                $("button.first#popular").attr("disabled", false);
                $("button.previous#popular").attr("disabled", false);
                $("button.next#popular").attr("disabled", true);
                $(this).attr("disabled", true);
                $("em#PopularRecipePage").text("   " + page + "   "); // update the page counter
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });
            
            // retrieve next "Popular Recipes" page
            $("button.next#popular").click(function () {
                var nextPageNumber = parseInt($("em#PopularRecipePage").html().replace(/ /g, ''), 10) + 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#popular";
                var which = "popular";
                $("button.first#popular").attr("disabled", false);
                $("button.previous#popular").attr("disabled", false);
                if (nextPageNumber == PopularRecipePages) { // next disabled if we reach the last page
                    $("button.next#popular").attr("disabled", true);
                    $("button.last#popular").attr("disabled", true);
                }
                $("em#PopularRecipePage").text("   " + page + "   "); // update the page counter
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });

            // retrieve previous "Popular Recipes" page
            $("button.previous#popular").click(function () {
                var nextPageNumber = parseInt($("em#PopularRecipePage").html().replace(/ /g, ''), 10) - 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#popular";
                var which = "popular";
                $("button.last#popular").attr("disabled", false);
                $("button.next#popular").attr("disabled", false);
                if (nextPageNumber == 1) {  // if we are on the first page again
                    $("button.previous#popular").attr("disabled", true);
                    $("button.first#popular").attr("disabled", true);
                }
                $("em#PopularRecipePage").text("   " + page + "   ");  // update the page counter as long as there are previous pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });
            
            // retrieve first "Popular Recipes" page
            $("button.first#popular").click(function () {
                var nextPageNumber = 1;
                var page = "1";
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#popular";
                var which = "popular";
                $("button.last#popular").attr("disabled", false);
                $("button.next#popular").attr("disabled", false);
                $("button.previous#popular").attr("disabled", true);
                $(this).attr("disabled", true);
                $("em#PopularRecipePage").text("   " + page + "   ");  // update the page counter as long as there are previous pages
                RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons);
            });
}