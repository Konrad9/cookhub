// adds a category to the list of possible categories to add the recipe to when creating a new recipe
function addCat(url) {
    var name = $("input#id_name").val();
    if (name.length==0){
        alert("Empty name, could not add category.");
        return;
    }
    $.post(url, {"name": name,"csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()}, 
            function(json) {
                if (json.alreadyExists=="no") {
                    $("ul#id_categories").append("<li><label for='id_categories_" + 
                    (json.id).toString() + "'><input type='checkbox' name='categories' value='" + 
                    (json.id+1).toString() + "' id='id_categories_" +
                    (json.id).toString() + "'> " +
                    json.name + "</label>");
                }
                else {
                    alert("Category already exists.");
                }
                document.getElementById("category_form").reset();
            });
}