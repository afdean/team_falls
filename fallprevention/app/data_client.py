import json

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
        question_file = open("../standards/questions.json", "r")
        med_file = open("../standards/medication.json", "r")
        func_ability_file = open("../standards/func_ability_test.json", "r")
        intervention_list_file = open("../standards/intervention_list.json", "r")
        physical_exam_file = open("../standards/physical_exam.json", "r")
        risk_interventions_file = open("../standards/risk_interventions.json", "r")

        self.questions = json.load(question_file)
        self.func_test = json.load(func_ability_file)
        self.intervention_list = json.load(intervention_list_file)
        self.medication = json.load(med_file)
        self.physical_exam = json.load(physical_exam_file)
        self.risk_interventions = json.load(risk_interventions_file)

        print(self.func_test)
