function addIng(url, btn, recipeID) {
    $.post(url,{"name": $(btn).closest("#ingredient_form").children("input#id_name").val(),
    			 "quantity": $("input#id_quantity").val(),
    			 "unit": $("input#id_unit").val(),
    			 "recipeID": recipeID,
    			 "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val()}, 
                function(json) {
                    var unitPart = "";
                    if (json.unit.length>0) {
                        unitPart = json.unit + " of ";
                    }
                    $("ul#ingredientList").append("<li id='ingredient" +
                    json.id + "'>" + json.quantity + " " + unitPart + json.name + 
                    "  <button class='removeIngredient' data-ingredientid='" + 
                    json.id + "' >Remove</button></li>");
                document.getElementById("ingredient_form").reset();
            });
}