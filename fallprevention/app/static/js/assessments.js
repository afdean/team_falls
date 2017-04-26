var tug_checkbox = $('#tug_checkbox');
var stand_checkbox = $('#30_sec_stand_checkbox');
var stage_checkbox = $('#4_stage_balance_checkbox');

// Main function that is called throughout sessions
var main = function () {
    "use strict";
    // $('#assessments').hide();
    hideButtons();
    showSelectedAssessments();

}
$(document).ready(main);

function hideButtons() {
    $('#tug').hide();
    $('#30_sec_stand').hide();
    $('#4_stage_balance').hide();
    $('#notes').hide();
    $('#assessment_button').hide();
    // $('#myBtn').hide();
}

function showSelectedAssessments() {
    var button = $('#submit-id-submit');
    button.click(function () {
     $('center').hide();
    });
}
