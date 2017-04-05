

// Main function that is called throughout sessions
var main = function () {
    "use strict";
    var elements = document.getElementsByTagName('fieldset');
  
    createExamSelectForm();

    $('#id-tugform2').hide();
    showSelectedExams(elements);

}
$(document).ready(main);

function showSelectedExams(elements) {
    var checkboxes = document.getElementById("exam_select").querySelectorAll('.checkbox input');

    
      var exams_class_names = document.getElementById("exam_select").querySelectorAll('.checkbox');


    $('#select_exam_button button').click(function () {
        $('.select_exam').hide();
         $('#id-tugform2').show(); 

         //check which check boxes were selected
         for(var i = 0;i < checkboxes.length;i++){
            if(!checkboxes[i].checked){
              elements[i].style.display = 'none';
            }
         }

    });

 

}

function createNewCheckboxt(name, id) {
    
    var div = document.createElement('div');
    div.className += 'checkbox';
    var label = document.createElement('label');
    var p = document.createElement('p');
    p.append(name);
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = name;
    checkbox.id = id;
    label.append(checkbox);
    label.appendChild(p);
    
    div.append(label);
    return div;
}

function createExamSelectForm() {
    var exam_form = $('#exam_select');
    var exam_button = $('#select_exam_button');
    exam_button.hide();
    var legends = document.getElementsByTagName('legend');
    for (var i = 0; i < legends.length; i++) {
        var exam_title = legends[i].innerText;
        var checkbox = createNewCheckboxt(exam_title, exam_title);
        exam_form.append(checkbox);
    }
   exam_form.append(exam_button.show());
}