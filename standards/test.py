import json
# from collections import namedtuple
import urllib.request as ur
from constants import *

class DataClient():
    def __init__(self):
        with ur.urlopen(QUESTIONS_URL) as url_questions:
            self.questions = json.loads(url_questions.read().decode('utf8'))
        with ur.urlopen(FAT_URL) as url_fat:
            self.func_test = json.loads(url_fat.read().decode('utf8'))
        with ur.urlopen(MEDICATION_URL) as url_medication:
            self.medication = json.loads(url_medication.read().decode('utf8'))
        with ur.urlopen(PHYEXAM_URL) as url_phyexam:
            self.physical_exam = json.loads(url_phyexam.read().decode('utf8'))
        with ur.urlopen(INTERVENTION_URL) as url_intervention:
            self.intervention_list = json.loads(url_intervention.read().decode('utf8'))
        with ur.urlopen(RISK_URL) as url_risk:
            self.risk_list = json.loads(url_risk.read().decode('utf8'))

def add_question_info(fhir_dict):
    data_client = DataClient()
    questions = data_client.questions
    doc_dict = {}
    doc_dict['content'] = questions['name']
    doc_dict['description'] = questions['description']
    doc_dict['units'] = questions['units']
    fhir_dict[questions['code']] = doc_dict
    for i, question in enumerate(questions['questions']):
        question_dict = {}
        question_dict['content'] = question['content']
        question_dict['description'] = question['description']
        question_dict['units'] = question['units']
        fhir_dict[question['code']] = question_dict
    return fhir_dict

def add_assessment_info(fhir_dict):
    data_client = DataClient()
    tests = data_client.func_test
    for i, test in enumerate(tests):
        test_dict = {}
        test_dict['content'] = test['name']
        test_dict['description'] = test['description']
        test_dict['units'] = test['units']
        fhir_dict[test['code']] = test_dict
        for i, field in enumerate(test['forms']):
            field_dict = {}
            field_dict['content'] = field['content']
            field_dict['description'] = field['description']
            field_dict['units'] = field['units']
            fhir_dict[field['code']] = field_dict
    return fhir_dict

def add_exam_info(fhir_dict):
    data_client = DataClient()
    entities = data_client.physical_exam
    for i, entity in enumerate(entities):
        for i, field in enumerate(entity['forms']):
            field_dict = {}
            field_dict['content'] = field['content']
            field_dict['description'] = field['description']
            field_dict['units'] = field['units']
            fhir_dict[field['code']] = field_dict
    return fhir_dict

def add_intervention_info(fhir_dict):
    data_client = DataClient()
    entities = data_client.intervention_list
    for name, entity in entities.items():
        for i, field in enumerate(entity['forms']):
            field_dict = {}
            field_dict['content'] = field['content']
            field_dict['description'] = field['description']
            field_dict['units'] = field['units']
            fhir_dict[field['code']] = field_dict
    return fhir_dict

if __name__ == "__main__":
    fhir_dict = {}
    fhir_dict = add_question_info(fhir_dict)
    fhir_dict = add_assessment_info(fhir_dict)
    fhir_dict = add_exam_info(fhir_dict)
    fhir_dict = add_intervention_info(fhir_dict)
    with open("output.txt", 'w') as f:
        for key, value in fhir_dict.items():
            f.write('%s:%s\n' % (key, value))
