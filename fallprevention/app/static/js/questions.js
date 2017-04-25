// Main function that is called throughout sessions
var main = function () {
    $('.pass').click(function () {
        $("label input[value=False]").prop("checked", true)
         $("label input[value=0]").prop("checked", true)

    })


    $('.fail').click(function () {
        $("label input[value=True]").prop("checked", true)
         $("label input[value=2]").prop("checked", true)
    })


}
$(document).ready(main);