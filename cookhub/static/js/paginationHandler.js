function RecipeGetter(RecipesPerPage, author, which, page, single, element, url, buttons, attributes) {
    $.get(url, {"RecipesPerPage":RecipesPerPage, "author":author, "which":which, "page":page, "single":single, "attributes":attributes},
          function(data) {
              if (data.startsWith("error")) {
                      alert(data);
              }
              else if (data=="empty") {
                  $(element).html("");
              }
              else {
                  // firstly extract the information from the response
                  var recipes = data.split("||RCP||");           // each recipe is an array entry
                  var recipesArray = new Array(recipes.length);  // create the array of recipe objects
                  for (i=0; i<recipes.length; i++) {         // loop through each recipe
                         var recipe = recipes[i].split(";;");       // split each recipe into the pieces of information
                         var recipeInformation = new Object();      // create the dictionary for this recipe
                         // extract the pieces of information and add them to the dictionary
                         recipeInformation.photoSource = "/media/"+recipe[0];
                         recipeInformation.id = recipe[1];
                         recipeInformation.title = recipe[2];
                         recipeInformation.averageRating = recipe[3];
                         if (buttons=="yes") {
                             if (which=="newest" || which=="popular") {
                                 recipeInformation.button = recipe[4];
                                 }
                            else if (which=="saved") {
                                recipeInformation.button = "remove";
                            }
                         }
                         recipesArray[i] = recipeInformation;       // add the dictionary to the array of recipe dictionaries
                 }
                 displayRecipes(element, recipesArray, buttons);
             }
    });
}

// now to the representation
function displayRecipes(element, recipesArray, buttons) {
    var part1 = "<div class='col-md-4'><div class='card mb-4 box-shadow'><img class='card-img-top' alt='Thumbnail [100%x225]' style='height: 225px; width: 100%; display: block;' src='";
    var part2 = "' data-holder-rendered='true'><div class='card-body'><a class='card-text' href='/recipe/";
    var part3 = "'>";
    var part4 = "</a><div class='d-flex justify-content-between align-items-center'><a>Rating: ";
    var part5 = "</a></div>";
    var part6 = "</div></div></div>";
    var recipeHTMLpiece = "";
    for (i=0; i<recipesArray.length; i++) {
        var buttonPart = "";
        if (buttons=="yes") {
            if (recipesArray[i].button=="remove") {
                buttonPart = "<div class='btn-group'><button type='button' id='" + recipesArray[i].id + "' class='btn btn-sm btn-outline-secondary removeRecipeButton' data-recipeid='" + recipesArray[i].id + "' >Remove</button></div>";
            }
            else if (recipesArray[i].button=="save") {
                buttonPart = "<div class='btn-group'><button type='button' id='" + recipesArray[i].id + "' class='btn btn-sm btn-outline-secondary addRecipeButton' data-recipeid='" + recipesArray[i].id + "' >Save</button></div>";
            }
            else if (recipesArray[i].button=="saved") {
                buttonPart = "<div class='btn-group'><button type='button' id='" + recipesArray[i].id + "' class='btn btn-sm btn-outline-secondary addRecipeButton' data-recipeid='" + recipesArray[i].id + "' disabled='true' >Saved</button></div>";
            }
        }
        recipeHTMLpiece += part1 + recipesArray[i].photoSource + part2 + recipesArray[i].id + part3 + recipesArray[i].title + part4 + recipesArray[i].averageRating + part5 + buttonPart + part6;
    }
    $(element).html(recipeHTMLpiece);
}