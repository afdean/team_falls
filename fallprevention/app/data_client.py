# import json
# from collections import namedtuple
# import urllib.request as ur
# from .constants import *

# def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
# def json2obj(data): return json.load(data, object_hook=_json_object_hook)

# class Singleton(type):
#     def __init__(self, *args, **kwargs):
#         self.__instance = None
#         super().__init__(*args, **kwargs)

#     def __call__(self, *args, **kwargs):
#         if self.__instance is None:
#             self.__instance = super().__call__(*args, **kwargs)
#             return self.__instance
#         else:
#             return self.__instance

# class DataClient(metaclass=Singleton):
#     def __init__(self):
#         with ur.urlopen(QUESTIONS_URL) as url_questions:
#             self.questions = json2obj(url_questions)
#         with ur.urlopen(FAT_URL) as url_fat:
#             self.func_test = json2obj(url_fat)
#         with ur.urlopen(MEDICATION_URL) as url_medication:
#             self.medication = json2obj(url_medication)
#         with ur.urlopen(PHYEXAM_URL) as url_phyexam:
#             self.physical_exam = json2obj(url_phyexam)
#         with ur.urlopen(INTERVENTION_URL) as url_intervention:
#             self.intervention_list = json2obj(url_intervention)
#         with ur.urlopen(RISK_URL) as url_risk:
#             self.risk_list = json2obj(url_risk)
