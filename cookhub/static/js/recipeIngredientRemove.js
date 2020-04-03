// removes an ingredient from the list of added ones when creating a new recipe
function remIng(url, csrf_token, btn) {
        			var ingredientID = $(btn).attr("data-ingredientid");
        			$.post(url,
                        {"ingredientID": ingredientID, "csrfmiddlewaretoken": csrf_token }, 
                        function(data) {
                            if (data.startsWith("correct")) {
                                $("li#ingredient"+ingredientID).remove();
                            }
                            else {
                                alert(data);
                            }
                        });
}