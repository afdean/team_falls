var tug_checkbox = $('#tug_checkbox');
var stand_checkbox = $('#30_sec_stand_checkbox');
var stage_checkbox = $('#4_stage_balance_checkbox');

// Main function that is called throughout sessions
var main = function () {
    "use strict";
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
}

function showSelectedAssessments() {
    var button = $('#select_assessment_button');
    button.click(function () {

        if (tug_checkbox.is(':checked')) {
            $('#tug').slideToggle('fast');
        }
        if (stand_checkbox.is(':checked')) {
            $('#30_sec_stand').slideToggle('fast');

        }
        if (stage_checkbox.is(':checked')) {
            $('#4_stage_balance').slideToggle('fast');
        }
        $('#notes').show();
        $('#assessment_button').show();
        $('#assessment_select').hide();
    });
}
