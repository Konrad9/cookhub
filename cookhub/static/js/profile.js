function start(authenticated, MyRecipePages, SavedRecipePages, recipe_pagination, selected_user, save_recipe, csrf_token) {
        // set up of the initial look
        $("button.previous").attr("disabled", true);
        var RecipesPerPage = "3"; // set globally for the whole page and all requests
        var author = selected_user; // also global; we are on "selected_user"'s profile
        var which = "my";
        var nextPageNumber = 1; // this is on load up obviously the first page
        var page = nextPageNumber.toString();
        var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
        var element = "div.row#my";
        var url = recipe_pagination;
        if (nextPageNumber== MyRecipePages || MyRecipePages==0) { // if we are on the only page, there is no next
            $("button.next#my").attr("disabled", true);
        }
        $("em#MyRecipePage").text("   "+page+"   "); // set the page counter
        RecipeGetter(RecipesPerPage, author, which, page, single, element, url);
        
        if (authenticated=="True") { // if the user is authenticated, then he can remove the saved recipes, so we need buttons
            which = "saved";
            element = "div.row#saved";
            var buttons = "remove";
            if (nextPageNumber== SavedRecipePages || SavedRecipePages==0) {
                $("button.next#saved").attr("disabled", true);
            }
            $("em#SavedRecipePage").text("   "+page+"   "); // set the page counter
            RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
        }
        
        
        // remove the recipe from saved
        $("body").on("click", "button.removeRecipeButton", function() {
            if (authenticated=="True") {
                var recipeID = $(this).attr("data-recipeid");
                $.post(save_recipe,
                        {"recipeID": recipeID, "csrfmiddlewaretoken": csrf_token}, 
                        function(data) { // update the displayed recipes if one has been removed
                            if (data.startsWith("correct")) {
                                var recipesLeft = parseInt(data.substring(7), 10);
                                var which = "saved";
                                var nextPageNumber = parseInt($("em#SavedRecipePage").html().replace(/ /g,''), 10);
                                if (recipesLeft%RecipesPerPage==0 && nextPageNumber>1) {
                                    nextPageNumber -= 1;
                                }
                                var page = nextPageNumber.toString();
                                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                                if (recipesLeft==1) { // if there is only one left, get only one
                                    single = "1";
                                }
                                var element = "div.row#saved";
                                if (recipesLeft==0) { // if there are no saved recipes left, leave it empty
                                    $(element).html("");
                                    return;
                                }
                                var url = recipe_pagination;
                                var buttons = "remove";
                                if (recipesLeft<=parseInt(RecipesPerPage, 10)) { // if there are no more recipes left than there are recipes per page,
                                                                                 // deactivate both buttons
                                    $("button.next#saved").attr("disabled", true);
                                    $("button.previous#saved").attr("disabled", true);
                                }
                                else if (nextPageNumber== SavedRecipePages || SavedRecipePages==0) {
                                    $("button.next#saved").attr("disabled", true);
                                }                            
                                if (nextPageNumber>0) { // update the page counter as long as there are next pages
                                    $("em#SavedRecipePage").text("   "+page+"   ");
                                }
                                RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
                            }
                        });
                }
                
        });
        
        // retrieve next "My Recipes" page
        $("button.next#my").click(function () {
            var which = "my";
            var nextPageNumber = parseInt($("em#MyRecipePage").html().replace(/ /g,''), 10) + 1;
            var page = nextPageNumber.toString();
            var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
            var element = "div.row#my";
            var url = recipe_pagination;
            $("button.previous#my").attr("disabled", false);
            if (nextPageNumber== MyRecipePages || MyRecipePage==0) { // next disabled if we reach the last page
                $("button.next#my").attr("disabled", true);
            }
            $("em#MyRecipePage").text("   "+page+"   ");
            RecipeGetter(RecipesPerPage, author, which, page, single, element, url);   
        });
        
        // retrieve previous "My Recipes" page
        $("button.previous#my").click(function () {
            var which = "my";
            var nextPageNumber = parseInt($("em#MyRecipePage").html().replace(/ /g,''), 10) - 1;
            var page = nextPageNumber.toString();
            var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
            var element = "div.row#my";
            var url = recipe_pagination;
            $("button.next#my").attr("disabled", false);
            if (nextPageNumber==1) { // if we are on the first page again
                $("button.previous#my").attr("disabled", true);
            }
            $("em#MyRecipePage").text("   "+page+"   ");
            RecipeGetter(RecipesPerPage, author, which, page, single, element, url);
        });
        
        // retrieve next "Saved Recipes" page
        $("button.next#saved").click(function () {
            if (authenticated=="True") {
                var which = "saved";
                var nextPageNumber = parseInt($("em#SavedRecipePage").html().replace(/ /g,''), 10) + 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#saved";
                var url = recipe_pagination;
                var buttons = "remove"; // you can only remove a saved recipe
                $("button.previous#saved").attr("disabled", false);
                if (nextPageNumber== SavedRecipePages || SavedRecipePages==0) { // next disabled if we reach the last page
                    $("button.next#saved").attr("disabled", true);
                }
                $("em#SavedRecipePage").text("   "+page+"   ");
                RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
            }
        });
        
        // retrieve previous "Saved Recipes" page
        $("button.previous#saved").click(function () {
            if (authenticated=="True") {
                var which = "saved";
                var nextPageNumber = parseInt($("em#SavedRecipePage").html().replace(/ /g,''), 10) - 1;
                var page = nextPageNumber.toString();
                var single = "0"; // 1-based counting; if only one recipe from the page: 0 is NOT a single one
                var element = "div.row#saved";
                var url = recipe_pagination;
                var buttons = "remove";
                $("button.next#saved").attr("disabled", false);
                if (nextPageNumber==1) { // if we are on the first page again
                    $("button.previous#saved").attr("disabled", true);
                }
                $("em#SavedRecipePage").text("   "+page+"   ");
                RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons);
            }
        });
}