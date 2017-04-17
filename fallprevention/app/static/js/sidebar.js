
// Main function that is called throughout sessions
var main = function () {
  "use strict";
  $(".nav a").on("click", function () {
    
    $(".nav .nav-stacked").find(".active").removeClass("active");
    $(this).parent().addClass("active");
    console.log($(this))
  });
}
$(document).ready(main);