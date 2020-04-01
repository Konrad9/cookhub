function openNavbar() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNavbar() {
    document.getElementById("mySidenav").style.width = "0";
}

$(document).ready(function(){
   // resize the search bar on window resize
   function searchbarResize() {
       $("input#query").attr("style", "width:"+($(window).width()/4).toString()+"px; border-radius:10rem; background-color: #252525; color: #f8f9fa; border-color: #252525");
   }
   // show sidebar button and hide the top navigation bar
   function sidebarShow() {
       var imageWidth = $("img#logoImage").width();
       if (imageWidth==0) { // on page load, the width is not available
           imageWidth = 154;
       }
       if (imageWidth/$(window).width() >= 0.18) { // experimentally found ratio when the bar becomes very ugly
           $("div#navbarCollapse").css("display", "none");
           $("a.icon").css({"float": "right", "display": "block"});
        }
        else {
            $("div#navbarCollapse").css("display", "block");
            $("a.icon").css("display", "none");
        } 
   }
   searchbarResize();
   sidebarShow();
   $(window).resize(function(){
       sidebarShow();
       searchbarResize();
    });
});
                    
