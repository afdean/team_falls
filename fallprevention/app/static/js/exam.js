

// Main function that is called throughout sessions
var main = function () {
    "use strict";
    $('#exams_select').hide();

    var elements = document.getElementById("id-tugform2").querySelectorAll('.field_set');


    var array = new Array(elements.length);
    examButtonSelect();

}
$(document).ready(main);

function examButtonSelect() {
    $('#select_exam_button').click(function () {
         $('.exams').show();
          var elements = document.getElementById("id-tugform2").querySelectorAll('.field_set');

    console.log(elements);

    });

    var exams = document.getElementById("exam_select").querySelectorAll('.checkbox');

   

    exams.each(function () {
        if ($(this).is(':checked')) {
            $('#tug').slideToggle('fast');
        }
    })

}