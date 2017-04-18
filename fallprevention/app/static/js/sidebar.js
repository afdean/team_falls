
// Main function that is called throughout sessions
var main = function () {
  "use strict";
  $(".nav a").on("click", function () {

    $("#userMenu").find(".active").removeClass("active");
    $(this).parent().addClass("active");
    console.log($(this))
  });
}
$(document).ready(main);

function completedTask(tasks) {
  $("#pic1").click(function () {
    $("#items p").wrap("<del>");
    $("#pic1").fadeOut("slow");
  });
}