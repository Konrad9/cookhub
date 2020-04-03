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
    console.log(nextPageNumber, NumberOfPages);
    if (nextPageNumber >= NumberOfPages) { // if we are on the only page, there is no next
        $("button.first#results").attr("disabled", true);
        $("button.previous#results").attr("disabled", true);
        $("button.next#results").attr("disabled", true);
        $("button.last#results").attr("disabled", true);
    }
    $("em#ResultsRecipePage").text("   " + page + "   "); // set the page counter
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);    
    
    $("button.last#results").bind("click", {"dict": searchdata.query}, lastResultButton);
    $("button.next#results").bind("click", {"dict": searchdata.query}, nextResultButton);
    $("button.previous#results").bind("click", {"dict": searchdata.query}, previousResultButton);
    $("button.first#results").bind("click", {"dict": searchdata.query}, firstResultButton);
               
}

function lastResultButton(e) {
    dicti = e.data.dict;
    var csrf_token = dicti.csrf_token;
    var RecipesPerPage = dicti.RecipesPerPage;
    var author = dicti.author;
    var which = dicti.which;
    var single = dicti.single;
    var element = dicti.element;
    var url = dicti.url;
    var buttons = dicti.buttons;
    var attributes = dicti.attributes;
    var NumberOfPages = dicti.NumberOfPages;
    var nextPageNumber = NumberOfPages;
    var page = nextPageNumber.toString();
    $("button.first#results").attr("disabled", false); // we could click on "last", 
    $("button.previous#results").attr("disabled", false); // so there is a "previous" and "first"
    $("button.next#results").attr("disabled", true); // we are on the last page,
    $(this).attr("disabled", true);                 // so there is no next or last anymore
    $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
}

function nextResultButton(e) {
    dicti = e.data.dict;
    var csrf_token = dicti.csrf_token;
    var RecipesPerPage = dicti.RecipesPerPage;
    var author = dicti.author;
    var which = dicti.which;
    var single = dicti.single;
    var element = dicti.element;
    var url = dicti.url;
    var buttons = dicti.buttons;
    var attributes = dicti.attributes;
    var NumberOfPages = dicti.NumberOfPages;
    var nextPageNumber = parseInt($("em#ResultsRecipePage").html().replace(/ /g, ''), 10) + 1;
    var page = nextPageNumber.toString();
    $("button.previous#results").attr("disabled", false); // we could click on "next", 
    $("button.first#results").attr("disabled", false); // so there is a "previous" and "first"
    if (nextPageNumber == NumberOfPages) { // "next" and "last" disabled if we reach the last page
        $("button.next#results").attr("disabled", true);
        $("button.last#results").attr("disabled", true);
    }
    $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
}

function previousResultButton(e) {
    dicti = e.data.dict;
    var csrf_token = dicti.csrf_token;
    var RecipesPerPage = dicti.RecipesPerPage;
    var author = dicti.author;
    var which = dicti.which;
    var single = dicti.single;
    var element = dicti.element;
    var url = dicti.url;
    var buttons = dicti.buttons;
    var attributes = dicti.attributes;
    var NumberOfPages = dicti.NumberOfPages;
    var nextPageNumber = parseInt($("em#ResultsRecipePage").html().replace(/ /g, ''), 10) - 1;
    var page = nextPageNumber.toString();
    $("button.last#results").attr("disabled", false);
    $("button.next#results").attr("disabled", false);
    if (nextPageNumber == 1) { // if we are on the first page again
        $("button.previous#results").attr("disabled", true);
        $("button.first#results").attr("disabled", true);
    }
    $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
}

function firstResultButton(e) {
    dicti = e.data.dict;
    var csrf_token = dicti.csrf_token;
    var RecipesPerPage = dicti.RecipesPerPage;
    var author = dicti.author;
    var which = dicti.which;
    var single = dicti.single;
    var element = dicti.element;
    var url = dicti.url;
    var buttons = dicti.buttons;
    var attributes = dicti.attributes;
    var NumberOfPages = dicti.NumberOfPages;
    var nextPageNumber = 1;
    var page = "1";
    $(this).attr("disabled", true); // we are already on the first page
    $("button.previous#results").attr("disabled", true); // disable "previous", we are already on the first page
    $("button.next#results").attr("disabled", false);     // we could click on "first", so there is a next
    $("button.last#results").attr("disabled", false);    // and a last, too
    $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
}


 
 // add an ingredient to the list
 function addIngredient() {
    var text = document.getElementById("ingredientInput").value;
    $("ul#ingredientList").append("<li>"+ text + "</li>");
    document.getElementById("ingredientInput").value = "";
} 

// clear all filters
function clearFilters() {
    clearResetup(searchdata.query);
    $("input").removeAttr("checked");
    $("input#ratingSlider").val("0");
    $("em#sliderValue").html("0.0");
    $("ul#ingredientList").empty();
    $("button.last#results").unbind();
    $("button.next#results").unbind();
    $("button.previous#results").unbind();
    $("button.first#results").unbind();
    $("button.last#results").bind("click", {"dict": searchdata.query}, lastResultButton);
    $("button.next#results").bind("click", {"dict": searchdata.query}, nextResultButton);
    $("button.previous#results").bind("click", {"dict": searchdata.query}, previousResultButton);
    $("button.first#results").bind("click", {"dict": searchdata.query}, firstResultButton);
}     

 // Update the current slider value
function sliderFunction() {
    var slider = document.getElementById("ratingSlider");
    var output = document.getElementById("sliderValue");
    output.innerHTML = (slider.value/10).toString();
} 

function searchfiltered(dicti) {
    console.log("searching filtered");
    console.log(dicti.attributes);
    var csrf_token = dicti.csrf_token;
    var RecipesPerPage = dicti.RecipesPerPage;
    var author = dicti.author;
    var which = dicti.which;
    var single = dicti.single;
    var element = dicti.element;
    var url = dicti.url;
    var buttons = dicti.buttons;
    var attributes = dicti.attributes;
    var nextPageNumber = 1;
    var page = "1";
    var NumberOfPages = -1;
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes, function (value) {
                console.log("Callback: " + value);
                NumberOfPages = value;
    });
    setTimeout(function () {
        searchdata.filtered.NumberOfPages = NumberOfPages;
        $("button.first#results").attr("disabled", true); // we are already on the first page
        $("button.previous#results").attr("disabled", true); // disable "previous", we are already on the first page
        if (nextPageNumber>=NumberOfPages) {
            $("button.next#results").attr("disabled", true);     
            $("button.last#results").attr("disabled", true);
        }
        else {
            $("button.next#results").attr("disabled", false);     
            $("button.last#results").attr("disabled", false);    
        } 
    }, 200); 
      
    $("em#ResultsRecipePage").text("   " + page + "   "); // update the page counter as long as there are next pages
    
    $("button.last#results").unbind();
    $("button.next#results").unbind();
    $("button.previous#results").unbind();
    $("button.first#results").unbind();
    $("button.last#results").bind("click", {"dict": searchdata.filtered}, lastResultButton);
    $("button.next#results").bind("click", {"dict": searchdata.filtered}, nextResultButton);
    $("button.previous#results").bind("click", {"dict": searchdata.filtered}, previousResultButton);
    $("button.first#results").bind("click", {"dict": searchdata.filtered}, firstResultButton);
    
}


function clearResetup(dicti) {
    $("button.previous").attr("disabled", true);
    $("button.first").attr("disabled", true);
    $("button.next").attr("disabled", false);
    $("button.last").attr("disabled", false);
    var csrf_token = dicti.csrf_token;
    var RecipesPerPage = dicti.RecipesPerPage;
    var author = dicti.author;
    var which = dicti.which;
    var nextPageNumber = 1;
    var page = "1";
    var single = dicti.single;
    var element = dicti.element;
    var url = dicti.url;
    var buttons = dicti.buttons;
    var attributes = dicti.attributes;
    var NumberOfPages = dicti.NumberOfPages;
    if (nextPageNumber >= NumberOfPages) { // if we are on the only page, there is no next
        $("button.first#results").attr("disabled", true);
        $("button.previous#results").attr("disabled", true);
        $("button.next#results").attr("disabled", true);
        $("button.last#results").attr("disabled", true);
    }
    $("em#ResultsRecipePage").text("   " + page + "   "); // set the page counter
    RecipeGetter(csrf_token, RecipesPerPage, author, which, page, single, element, url, buttons, attributes);
}

function applyFilters() {
                // get checked boxes
                var cdBoxes = document.getElementsByName("catBox");
                var checkedBoxes = [];
                for (var i=0; i<cdBoxes.length; i++) {
                    console.log("checking boxes");
                    if (cdBoxes[i].checked) {
                        checkedBoxes.push(cdBoxes[i].value);
                        console.log(cdBoxes[i].value);
                    }
                }
                if (checkedBoxes.length==0) {
                    checkedBoxes = null;
                }
                
                // get rating
                var rating = document.getElementById("sliderValue").innerHTML;
                
                // get ingredients
                var ingredients = [];
                var ul = document.getElementById("ingredientList");
                var items = ul.getElementsByTagName("li");
                console.log(items.length);
                for (var i=0; i<items.length; i++) {
                    ingredients.push(items[i].innerHTML);
                }
                if (ingredients.length==0) {
                    ingredients = null;
                }
                
                // get sorting
                var sortBy = $("button.dropbtn#dropper").text();
                
                // remember the query
                var query = searchdata.query.attributes;
                searchdata.filtered.attributes = JSON.stringify({"query": query, "checkedCategories": checkedBoxes, "rating": rating, "ingredients": ingredients, "sortBy": sortBy});
                console.log(query, checkedBoxes, rating, ingredients);
                searchfiltered(searchdata.filtered);
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function dropper() {
  document.getElementById("myDropdown").classList.toggle("show");
}

$("button.dropbtn.s").click(function () {
    $("button.dropbtn#dropper").text($(this).text());
    closeMenu();
});

// close the menu
function closeMenu() {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
        }
    }
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    closeMenu();
  }
}             