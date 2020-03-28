function RecipeGetter(RecipesPerPage, author, which, page, single, element, url) {
    $.get(url, {"RecipesPerPage":RecipesPerPage, "author":author, "which":which, "page":page, "single":single},
          function(data) {
              if (data.startsWith("error")) {
                      alert(data);
              }
              else {
                  // firstly extract the information from the response
                  var recipes = data.split("||RCP||");           // each recipe is an array entry
                  var recipesArray = new Array(recipes.length);  // create the array of recipe objects
                  for (i=0; i<recipes.length; i++) {         // loop through each recipe
                         var recipe = recipes[i].split(";;");       // split each recipe into the pieces of information
                         var recipeInformation = new Object();      // create the dictionary for this recipe
                         // extract the pieces of information
                         var photoSource = "/media/"+recipe[0];
                         var id = recipe[1];
                         var title = recipe[2];
                         var averageRating = recipe[3];
                         // and add them to the dictionary
                         recipeInformation.photoSource = photoSource;
                         recipeInformation.id = id;
                         recipeInformation.title = title;
                         recipeInformation.averageRating = averageRating;
                         recipesArray[i] = recipeInformation;       // add the dictionary to the array of recipe dictionaries
                 }
                 displayRecipes(element, recipesArray);
             }
    });
}

// now to the representation
function displayRecipes(element, recipesArray) {
    var part1 = "<div class='col-md-4'><div class='card mb-4 box-shadow'><img class='card-img-top' alt='Thumbnail [100%x225]' style='height: 225px; width: 100%; display: block;'src='";
    var part2 = "' data-holder-rendered='true'><div class='card-body'><a class='card-text' href='/recipe/";
    var part3 = "'>";
    var part4 = "</a><div class='d-flex justify-content-between align-items-center'><a>Rating: ";
    var part5 = "</a></div></div></div></div>";
    var recipeHTMLpiece = "";
    for (i=0; i<recipesArray.length; i++) {
        recipeHTMLpiece += part1 + recipesArray[i].photoSource + part2 + recipesArray[i].id + part3 + recipesArray[i].title + part4 + recipesArray[i].averageRating + part5;
    }
    $(element).html(recipeHTMLpiece);
}