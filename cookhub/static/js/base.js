                    $(document).ready(function(){
                        // resize the search bar on window resize
                        function c() {
                            $("input#query").attr("style", "width:"+($(window).width()/4).toString()+"px; border-radius:10rem; background-color: #252525; color: #f8f9fa; border-color: #252525");
                        }
                        c();
                        $(window).resize(function(){ 
                            c();
                        });
                    });