// var completed_image = $()
  var questions_submit_button = $('#questions_submit_button');
    // var question_submit_button = $('#question_submit_button');
    var risks_submit_button = $('#risks_submit_button');
    var assessment_submit_button = $('#assessment_submit_button');
    var exam_submit_button = $('#exam_submit_button');
// Main function that is called throughout sessions
var main = function () {
    "use strict";

  

  

    submitButtonClick();
}
$(document).ready(main);

function submitButtonClick() {
    questions_submit_button.click(function () {
        $('#questions_li').prepend('<img src="/img/completed.svg" style="width: 10px height: 10px;"/>');
        console.log()
        
    });
}