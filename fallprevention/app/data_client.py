import json
from collections import namedtuple
import urllib.request as ur
from .constants import *
from app.fhir_reading import FallsFHIRClient

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

class DataClient(metaclass=Singleton):
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
        with ur.urlopen(MED_FORM_URL) as url_med_form:
            self.med_form = json.loads(url_med_form.read().decode('utf8'))
        self.fhir_client = FallsFHIRClient()
        # Creates self.fhir_dict
        self.create_fhir_dict()
        # print(self.fhir_dict['q000'])
        self.fhir_client.load_standards_document(self.fhir_dict)
        # Use "low", "moderate", and "high"
        self.risk_level = ""
        # Stores resources
        self.patient = {}
        self.encounter = {}
        # Complete dict of observations to be written to FHIR
        self.observations = {}
        # Determines if patient or provider that has logged in
        # Set as care_provider for now just for debugging purposes
        self.identity = "care_provider"
        # Used for displaying asssessments
        self.assessments_chosen = []
        # Used for displaying phyiscal exams
        self.exams_chosen = []
        self.patient_id = ""
        # Keeping these separate because they aren't written to FHIR in any meaninful way. Plus, anybody
        # doing this again can quickly review.
        self.medication_complete = False
        self.risks_complete = False

        # self.fhir_client.load_standards_document(self.fhir_dict)

    def reload_data(self):
        self.risk_level = ""
        self.patient = {}
        self.encounter = {}
        self.observations = {}
        self.identity = "care_provider"
        self.assessments_chosen = []
        self.exams_chosen = []
        self.patient_id = ""
        self.medication_complete = False
        self.risks_complete = False

    def create_fhir_dict(self):
        self.fhir_dict = {}
        self.add_question_info()
        self.add_assessment_info()
        self.add_exam_info()
        self.add_intervention_info()
        self.add_risk_info()
        self.add_med_form_info()
        # with open("output.txt", 'w') as f:
        #     for key, value in self.fhir_dict.items():
        #         f.write('%s:%s\n' % (key, value))

    def add_question_info(self):
        self.doc_dict = {}
        self.doc_dict['content'] = self.questions['name']
        self.doc_dict['description'] = self.questions['description']
        self.doc_dict['units'] = self.questions['units']
        self.fhir_dict[self.questions['code']] = self.doc_dict
        for i, question in enumerate(self.questions['questions']):
            self.question_dict = {}
            self.question_dict['content'] = question['content']
            self.question_dict['description'] = question['description']
            self.question_dict['units'] = question['units']
            self.fhir_dict[question['code']] = self.question_dict

    def add_assessment_info(self):
        for i, test in enumerate(self.func_test):
            self.test_dict = {}
            self.test_dict['content'] = test['name']
            self.test_dict['description'] = test['description']
            self.test_dict['units'] = test['units']
            self.fhir_dict[test['code']] = self.test_dict
            for i, field in enumerate(test['forms']):
                self.field_dict = {}
                self.field_dict['content'] = field['content']
                self.field_dict['description'] = field['description']
                self.field_dict['units'] = field['units']
                self.fhir_dict[field['code']] = self.field_dict

    def add_exam_info(self):
        for i, entity in enumerate(self.physical_exam):
            for i, field in enumerate(entity['forms']):
                self.field_dict = {}
                self.field_dict['content'] = field['content']
                self.field_dict['description'] = field['description']
                self.field_dict['units'] = field['units']
                self.fhir_dict[field['code']] = self.field_dict

    def add_intervention_info(self):
        for name, entity in self.intervention_list.items():
            for i, field in enumerate(entity['forms']):
                self.field_dict = {}
                self.field_dict['content'] = field['content']
                self.field_dict['description'] = field['description']
                self.field_dict['units'] = field['units']
                self.fhir_dict[field['code']] = self.field_dict

    def add_risk_info(self):
        self.fhir_dict[self.risk_list['code']] = {
            'content': self.risk_list['content'],
            'description': self.risk_list['description'],
            'units': self.risk_list['units']
        }

    def add_med_form_info(self):
        for i, field in enumerate(self.med_form['forms']):
            self.field_dict = {}
            self.field_dict['content'] = field['content']
            self.field_dict['description'] = field['description']
            self.field_dict['units'] = field['units']
            self.fhir_dict[field['code']] = self.field_dict
