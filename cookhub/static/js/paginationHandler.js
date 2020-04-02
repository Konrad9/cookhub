function RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes, categories, rating) {
    $.post(url, {"RecipesPerPage":RecipesPerPage, "author":author, "which":which, "page":page, "single":single, "buttons":buttons, "attributes":attributes, "csrfmiddlewaretoken": csrf_token, "categories": categories, "rating": rating},
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
                         recipeInformation.creator = recipe[4];
                         if (buttons=="yes") {
                                recipeInformation.button = recipe[5];
                         }

                         if (buttons=="remove") {
                                recipeInformation.button = "remove";
                         }
                         recipesArray[i] = recipeInformation;       // add the dictionary to the array of recipe dictionaries
                 }
                 displayRecipes(element, recipesArray, buttons, which);
             }
    });
}

// now to the representation
function displayRecipes(element, recipesArray, buttons, which) {
    var part1 = "<div class='col-md-4'><div class='card mb-4 box-shadow'><img class='card-img-top' alt='Thumbnail [100%x225]' style='height: 225px; width: 100%; display: block;' src='";
    var part2 = "' data-holder-rendered='true'><div class='card-body'><a class='card-text-title p-0 m-0 text-truncate' style='max-width: 300px' href='/recipe/";
    var part3 = "'>";
    var part4 = "</a><div class='d-flex justify-content-between align-items-center m-0 p-0'>";
    var part4Creator = "";
    var part4Rating = "<p class='card-text-rating m-0 t-0'>Rating: ";
    var part5 = "</p>";
    var part6 = "</div></div></div></div>";
    var recipeHTMLpiece = "";
    for (i=0; i<recipesArray.length; i++) {
        var buttonPart = "";
        if (recipesArray[i].button=="remove") {
            buttonPart = "<div class='btn-group'><button type='button' id='" + recipesArray[i].id + "' class='btn btn-sm btn-outline-warning removeRecipeButton' data-recipeid='" + recipesArray[i].id + "' >Remove</button></div>";
        }
        else if (recipesArray[i].button=="save") {
            buttonPart = "<div class='btn-group'><button type='button' id='" + recipesArray[i].id + "' class='btn btn-sm btn-outline-warning addRecipeButton' data-recipeid='" + recipesArray[i].id + "' >Save</button></div>";
        }
        else if (recipesArray[i].button=="saved") {
            buttonPart = "<div class='btn-group'><button type='button' id='" + recipesArray[i].id + "' class='btn btn-sm btn-outline-warning addRecipeButton' data-recipeid='" + recipesArray[i].id + "' disabled='true' >Saved</button></div>";
        }
        if (which!="my") {
            part4Creator  = "<p class='card-text-author mt-0 mb-0'>Creator:<a class='card-text-creator m-0 p-0 pl-2' href='/profile/" + recipesArray[i].creator + "/'>" + recipesArray[i].creator + "</a></p></div><div class='d-flex justify-content-between align-items-center'>";
        }
        recipeHTMLpiece += part1 + recipesArray[i].photoSource + part2 + recipesArray[i].id + part3 + recipesArray[i].title + part4 + part4Creator + part4Rating + recipesArray[i].averageRating + part5 + buttonPart + part6;
    }
    $(element).html(recipeHTMLpiece);
    
/*
Element displayed by the function "displayRecipes", with some minor changes depending on the context:

<div class="card mb-4 box-shadow">
<img class="card-img-top" alt="Thumbnail [100%x225]" style="height: 225px; width: 100%; display: block;" src="/media/{{ recipe.photo }}" data-holder-rendered="true">
	<div class="card-body">
		<a class="card-text-title p-0 m-0" href="/recipe/{{ recipe id }}">{{ recipe.title }}</a>
		<div class="d-flex justify-content-between align-items-center">
			<p class="card-text-author mt-2 mb-2">Creator:<a href="/profile/{{ username }}/">{{ username }}</a></p>
			<p class="card-text-rating mt-2 mb-2">Rating: {{ recipe.rating }}</p>
			<div class="btn-group">
				<button type="button" id="{{ recipe.id }}" class="btn btn-sm btn-outline-warning addRecipeButton" data-recipeid="{{ recipe.id }}">
				Save
				</button>
			</div>
		</div>
	</div>
</div>

*/
}