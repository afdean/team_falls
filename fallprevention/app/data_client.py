import json
from collections import namedtuple
import urllib.request as ur
from .constants import *

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
        self.patient = {}
