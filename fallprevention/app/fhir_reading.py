#!/usr/bin/env python
#
#
# FHIR Client for using smart-on-fhir rest-api to read and write fhir resources, specifically for a
# falls-prevention FHIR app made for Georgia Tech class CS6440. Project was Improving Fall Prevention
# among Older Adults
#
#
# Author: Ari Kapusta (akapusta@gatech.edu)
# Team: Team Falls
# Members: Shujun Bian, Andrew Dean, Ari Kapusta, Lusenii Kromah
#
#

import json
import requests
import copy
import time
from collections import namedtuple
import urllib.request as ur
from .constants import *
# Requires a smart-on-fhir api-server running on localhost. Find code to run that at
# https://github.com/smart-on-fhir/api-server
class FallsFHIRClient(object):
    def __init__(self):
        self.api_base = 'http://localhost:8080/'
        self.patient_id = None
        self.encounter_id = None
        #set diagnostic_report to True as default
        self.diagnostic_report = True
        self.medication_list = None
        self.standards_document_dict = {}
        self.questions_code = []
        self.questions_text = []
        self.questions_answer_description = []
        self.questions_units = []
        #self.load_standards_document('https://raw.githubusercontent.com/akapusta/team_falls/master/standards/questions.json')

    def test_function(self):
        self.select_patient_from_patient_result(self.search_patient('sarah', 'graham'))

    # Loads the latest standards document. Should probably be run occasionally or whenever things are
    # called to make sure questions are being kept up to date.
    # Input: nothing (it loads the document from a known location)
    # Returns: nothing
    # Note: We can change this to take input so you can tell it where the document is.
    def load_standards_document(self, standards_document_dict):
        self.standards_document_dict = standards_document_dict
        self.questions_code = []
        self.questions_text = []
        self.questions_answer_description = []
        self.questions_units = []
        for question in standards_document_dict:
            if question in self.questions_code:
                print('There are repeated question codes in the standards document! That will cause problems')
                return False
            self.questions_code.append(question)
            self.questions_text.append(standards_document_dict[question]['content'])
            self.questions_answer_description.append(standards_document_dict[question]['description'])
            self.questions_units.append(standards_document_dict[question]['units'])
        print('Client has loaded the current standards document')
        return True

    # Search for a patient by name
    # Input: first_name, last_name
    # Returns: list of patients. Each is a dict.
    # Note: Patient_id is found at patient['resource']['identifier'][0]['value']
    # Requires: api-server running
    def search_patient(self, first_name, last_name):
        search_headers = {'Accept': 'application/json'}
        search_params = {'family': last_name, 'given': first_name}
        resp = requests.get(self.api_base + 'Patient/', headers=search_headers, params=search_params)
        if resp.status_code != 200 or resp.json()['total'] < 1:
            # This means something went wrong.
            print('Something went wrong')
            return []
        else:
            # print resp.json()
            patient_list = resp.json()['entry']
            return patient_list

    # Search for a patient by name and date of birth. DoB can be entered by year, year and month, or year, month and
    # date.
    # Input: first_name, last_name, DoB as str(YYYY-MM-DD).
    # Returns: list of patients. Each is a dict.
    # Note: Checks from left to right, needs full amount. So you can enter YYYY or YYYY-MM or
    # YYYY-MM-DD
    # Patient_id is found at patient['resource']['identifier'][0]['value']
    # Requires: api-server running
    def search_patient_dob(self, first_name, last_name, date_of_birth):
        search_headers = {'Accept': 'application/json'}
        search_params = {'birthdate': date_of_birth, 'family': last_name, 'given': first_name}
        resp = requests.get(self.api_base + 'Patient/', headers=search_headers, params=search_params)
        if resp.status_code != 200 or resp.json()['total'] < 1:
            # This means something went wrong.
            print('Something went wrong')
            return []
        else:
            # print resp.json()
            patient_list = resp.json()['entry']
            return patient_list

    # Search for a patient by id
    # Input: patient_id
    # Returns: list of patients. Each is a dict.
    # Note: Patient_id is found at patient['resource']['identifier'][0]['value']
    # Requires: api-server running
    def search_patient_by_id(self, pat=None):
        if pat == None:
            pat = self.patient_id
        if not pat:
            print('I am missing a patient_id to search for relevant encounters')
            return None
        search_headers = {'Accept': 'application/json'}
        search_params = {'identifier': pat}
        resp = requests.get(self.api_base + 'Patient/', headers=search_headers, params=search_params)
        # print(resp)
        if resp.status_code != 200 or resp.json()['total'] < 1:
            # This means something went wrong.
            print('Something went wrong. Probably there is no patient by that id')
            return []
        else:
            # print(resp.json())
            patient = resp.json()['entry']
            return patient

    # Function to select the patient (i.e., set the client's patient_id to the desired patient) based
    # on a returned list from search_patient or search_patient_dob.
    # Input: patient_list, index of desired patient (defaults to first on list)
    # Returns: nothing
    def select_patient_from_patient_result(self, patient_list, list_index=0):
        if len(patient_list) < list_index-1:
            print('The index of the patient selected is higher than the number of patients available.')
            self.patient_id = None
        else:
            self.patient_id = patient_list[list_index]['resource']['identifier'][0]['value']

    # Function to select the patient (i.e., set the client's patient_id to the desired patient) based on
    # the function's input
    # Input: patient_id
    # Returns: nothing
    def select_patient(self, patient_id):
        self.patient_id = str(patient_id)

    # Search for all encounters by patient_id. Lets you set desired status.
    # Input: patient_id (by default uses the client's patient_id, if it has
    # been set), status list of desired statuses of encounters
    # Returns: list of encounters. Each is a dict.
    # Requires: api-server running
    def search_encounter_all(self, pat=None, status=['']):
        if pat == None:
            pat = self.patient_id
        if not pat:
            print('I am missing a patient_id to search for relevant encounters')
            return None
        encounter_list = []
        search_headers = {'Accept': 'application/json'}
        for stat in status:
            search_params = {'patient': pat, 'status': stat}
            resp = requests.get(self.api_base + 'Encounter/', headers=search_headers, params=search_params)
            if resp.json()['total'] > 0:
                for enc in resp.json()['entry']:
                    encounter_list.append(enc)
        if len(encounter_list) == 0:
            print('There were no encounters for that patient')
        return encounter_list


    def create_new_encounter(self, pat=None, date='', set_as_active_encounter=False):
        if pat == None:
            pat = self.patient_id
        if not pat:
            print('I am missing a patient_id to search for relevant encounters')
            return None
        if not date:
            date = (time.strftime("%Y-%m-%d"))
        save_enc = {}
        save_enc['resourceType'] = "Encounter"
        save_enc['status'] = "in-progress"
        save_enc['period'] = {}
        save_enc['period']['start'] = date
        save_enc['patient'] = {}
        save_enc['patient']['reference'] = 'Patient/'+pat
        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        resp = requests.post(self.api_base + 'Encounter/', data=json.dumps(save_enc), headers=write_headers)
        if resp.status_code != 201:
            print('Something went wrong when trying to write to the server')
            return False
        else:
            if set_as_active_encounter:
                print(resp.json())
                self.encounter_id = resp.json()['id']
            return True

        def end_encounter(self, enc_id=None):
            if enc_id == None:
                enc_id = self.encounter_id
            if not enc_id:
                print('I am missing a encounter_id to search for relevant encounters')
                return None
            write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            search_headers = {'Accept': 'application/json'}
            resp = requests.get(self.api_base + 'Encounter/' + enc_id, headers=search_headers)
            if resp.status_code != 200:
                print(
                'Could not find the encounter by that encounter id or something else ' \
                'went wrong.')
                return False
            alter_enc = resp.json()
            alter_enc['status'] = 'finished'
            resp = requests.put(self.api_base + 'Encounter/' + enc_id, data=json.dumps(alter_enc),
                                headers=write_headers)
            if resp.status_code != 200:
                print('Something went wrong in writing the update to close the encounter by setting its status to ' \
                      'finished')
                return False
            else:
                return True

    # Search for encounters on a date and by patient_id. Sets client encounter_id if there is only one
    # matching encounter.
    # Input: Date str(YYYY-MM-DD), patient_id (by default uses the client's patient_id, if it has
    # been set)
    # Returns: list of encounters. Each is a dict.
    # Requires: api-server running
    def search_encounter_date(self, date=None, pat=None):
        if pat == None:
            pat = self.patient_id
        if not pat:
            print('I am missing a patient_id to search for relevant encounters')
            return None
        if not date:
            date = (time.strftime("%Y-%m-%d"))
        encounter_list = []
        search_headers = {'Accept': 'application/json'}
        for stat in ['planned', 'arrived', 'in-progress']:
            search_params = {'patient': 'Patient/'+pat, 'status': stat}
            resp = requests.get(self.api_base + 'Encounter/', headers=search_headers, params=search_params)
            if resp.json()['total']>0:
                for enc in resp.json()['entry']:
                    encounter_list.append(enc)
        if len(encounter_list) == 0:
            print('There were no encounters for that date for that patient')
            return []
        matching_encounters = []
        for enc in encounter_list:
            if enc['resource']['period']['start'] == date:
                matching_encounters.append(enc)
        if len(matching_encounters) > 1:
            print('There is more than one encounter that matches the date. Pick one.')
            print(matching_encounters)
            return matching_encounters
        else:
            self.encounter_id = enc['id']
            print(matching_encounters)
            return matching_encounters

    # Function to select the encounter (i.e., set the client's patient_id to the desired patient) based
    # on a returned list from search_patient or search_patient_dob.
    # Input: patient_list, index of desired patient (defaults to first on list)
    # Returns: nothing
    def select_encounter_from_encounter_result(self, encounter_list, list_index=0):
        if len(encounter_list) == 0:
            print('There were no encounters for that date for that patient')
            self.encounter_id = None
        if len(encounter_list) < list_index - 1:
            print('The index of the encounter selected is higher than the number of encounters available.')
            self.encounter_id = None
        else:
            self.encounter_id = encounter_list[list_index]['resource']['id']

    # Search for medications the patient is currently on by patient_id. First looks up medication orders, which shows
    # the medications the patient is taking. Then looks up the information for each medication and returns that.
    # Input: patient_id (by default uses the client's patient_id, if it has been set)
    # Returns: list of medications the patient is currently taking. Each is a dict.
    # Requires: api-server running
    def search_medication(self, pat=None):
        if pat == None:
            pat = self.patient_id
        if not pat:
            print('I am missing a patient_id to search for relevant medications')
            return None
        medication_code_list = []
        medication_list = []
        search_headers = {'Accept': 'application/json'}

        use_medicationstatement_instead_of_medication_order = False
        if not use_medicationstatement_instead_of_medication_order:
            for stat in ['active', 'intended']:
                search_params = {'patient': pat, 'status': stat}
                # search_params = {}
                resp = requests.get(self.api_base + 'MedicationOrder/', headers=search_headers, params=search_params)
                if resp.json()['total'] > 0:
                    for med_order in resp.json()['entry']:
                        medication_list.append(med_order)
        else:
            for stat in ['active', 'intended']:
                search_params = {'subject': pat, 'status': stat}
                search_params = {}
                resp = requests.get(self.api_base + 'MedicationStatement/', headers=search_headers, params=search_params)
                print(resp)
                if resp.json()['total']>0:
                    for med_statement in resp.json()['entry']:
                        medication_code_list.append(med_statement['resource']['medicationReference']['reference'])

            if len(medication_code_list) == 0:
                print('The patient is not taking any medications')
                return medication_list

            for med in medication_code_list:
                search_params = {'id': med}
                resp = requests.get(self.api_base + 'Medication/', headers=search_headers, params=search_params)
                if resp['total'] > 0:
                    for med_resp in resp.json()['resource']:
                        medication_list.append(med_resp)
        return medication_list

    # Probably something in the care provider's system should make changes to prescriptions, etc, but for fun here is
    # a function to end a medication order ourselves. Simply sets the status of a medication order to completed.
    # Input: medication_order_id (from the searched medication order list), patient_id (defaults to the client's
    # patient id if it has been set).
    # Returns: True if write is successful. False otherwise.
    def end_medication_by_id(self, medication_order_id, pat=None):
        if pat == None:
            pat = self.patient_id
        if not pat:
            print('I am missing a patient_id to search for relevant medications')
            return False
        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        search_headers = {'Accept': 'application/json'}
        search_params = {'patient': pat}
        resp = requests.get(self.api_base + 'MedicationOrder/'+medication_order_id, headers=search_headers, params=search_params)
        if resp.status_code != 200:
            print('Could not find the medication order by that medication order id and patient id or something else ' \
                  'went wrong.')
            return False
        alter_med = resp.json()
        alter_med['status'] = 'completed'
        resp = requests.put(self.api_base + 'MedicationOrder/'+medication_order_id, data=json.dumps(alter_med), headers=write_headers)
        if resp.status_code != 200:
            print('Something went wrong in writing the update to end the medication order by setting its status to ' \
                  'complete')
            return False
        else:
            return True

    # Probably something in the care provider's system should make changes to prescriptions, etc, but for fun here is
    # a function to end a medication order ourselves. Simply sets the status of a medication order to completed.
    # Input: medication_order (from a search)
    # Returns: True if write is successful. False otherwise.
    def end_medication_by_order(self, medication_order):
        pat = medication_order['resource']['patient']['reference'].split('/')[1]
        medication_order_id = medication_order['resource']['id']
        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        search_headers = {'Accept': 'application/json'}
        search_params = {'patient': pat}
        resp = requests.get(self.api_base + 'MedicationOrder/'+medication_order_id, headers=search_headers,
                            params=search_params)
        if resp.status_code != 200:
            print('Could not find the medication order or something else went wrong.')
            return False
        alter_med = resp.json()
        alter_med['status'] = 'completed'
        resp = requests.put(self.api_base + 'MedicationOrder/'+medication_order_id, data=json.dumps(alter_med),
                            headers=write_headers)
        if resp.status_code != 200:
            print('Something went wrong in writing the update to end the medication order by setting its status to ' \
                  'complete')
            return False
        else:
            return True

    # Function to select the encounter (i.e., set the client's encounter_id to the desired patient)
    # based on the function's input
    # Input: encounter_id
    # Returns: nothing
    def select_encounter(self, encounter_id):
        self.encounter_id = str(encounter_id)

    # Function to look up the relevant diagnostic report. If none exists, it will create one. This keeps track
    # of the observations done for an assessment. Not currently particularly working.
    # Input: patient_id, encounter_id (the default uses client values if they have been set)
    # Returns: The first matching procedure,
    # Note: Not particularly working yet.
    def pullup_diagnostic_report(self, pat=None, enc=None):
        if pat == None:
            pat = self.patient_id
        if enc == None:
            enc = self.encounter_id
        if not pat or not enc:
            print('I am missing a patient_id or encounter_id to search for relevant diagnostic_reports')
            return None
        search_headers = {'Accept': 'application/json'}
        search_params = {'subject': pat, 'encounter': enc, 'category': 'fall_prevention'}
        resp = requests.get(self.api_base + 'DiagnosticReport/', headers=search_headers, params=search_params)
        if resp['total'] > 0:
            self.diagnostic_report = resp.json()['entry'][0]
            self.diagnostic_report_previously_existed = True
            return True
        else:
            self.diagnostic_report_previously_existed = False
            self.create_new_procedure()

    # Function to create a new procedure. This is primarily for record keeping, to know when things
    # have been done. Not currently working or.
    # Input: patient_id, encounter_id (the default uses client values if they have been set)
    # Returns: True if succeeds in creating a new procedure or False if fails.
    # Note: Not working.
    def create_new_diagnostic_report(self, pat=None, enc=None):
        if pat == None:
            pat = self.patient_id
        if enc == None:
            enc = self.encounter_id
        if not pat or not enc:
            print('I am missing a patient_id or encounter_id to create a relevant diagnostic report')
            return None
        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        print('I cannot make new procedures quite yet')
        resp = False
        if resp.status_code == '201':
            return True
        else:
            print('Something went wrong when trying to write to the server')
            return False

    # Search for observations that are relevant to the app based on standards document.
    # Input: dict of standards, patient_id, encounter_id (by default uses the client's values, if they
    # have been set)
    # Returns: Dict of observations. The key is the observation code. Each observation is also a dict.
    # Requires: api-server running
    def search_observations(self, standards_dict=None, pat=None, enc=None, return_entire_observation_not_just_value=False):
        output_dict = {}
        if pat == None:
            pat = self.patient_id
        if enc == None:
            enc = self.encounter_id
        if standards_dict == None:
            standards_dict = self.standards_document_dict
        if not pat or not enc or not standards_dict:
            print('I am missing a patient_id, encounter_id, or standards_dict to search for relevant observations')
            return {}
        search_headers = {'Accept': 'application/json'}
        search_params = {'subject': pat, 'encounter': enc, 'category': 'fall_prevention'}
        resp = requests.get(self.api_base + 'Observation/', headers=search_headers, params=search_params)
        if resp.json()['total'] > 0:
            for obs in resp.json()['entry']:
                if obs['resource']['code']['coding'][0]['system'] == 'fall_prevention':
                    for question_code in self.questions_code:
                        # if standards_question['model'] == 'app.Question':
                        # print (standards_question)

                        if obs['resource']['code']['coding'][0]['code'] == question_code:
                            if return_entire_observation_not_just_value:
                                output_dict[str(question_code)] = obs
                            else:
                                if 'valueCodeableConcept' in obs['resource'].keys() and 'code' in obs['resource']['valueCodeableConcept']['coding'][0].keys():
                                    output_dict[str(question_code)] = obs['resource']['valueCodeableConcept']['coding'][0]['code']
                                else:
                                    print('Tried to pull up observation data but the old observation uses old version of standard')
        return output_dict

    # Function write many observations to fhir. Takes in a list of question codes and associated responses.
    # Input: data (a dict where keys are question_codes and contents are the responses to the question), patient_id, encounter_id,
    # diagnostic report (the default uses client values if they have been set)
    # Returns: True if succeeds in creating a new procedure or False if fails.
    def write_list_of_observations_to_fhir(self, data, pat_id=None, enc_id=None, diag_rpt=None):
        if pat_id == None:
            pat_id = self.patient_id
        if enc_id == None:
            enc_id = self.encounter_id
        if diag_rpt == None:
            diag_rpt = self.diagnostic_report
        if not pat_id or not enc_id or not diag_rpt:
            print('I am missing a patient_id, encounter_id, or diagnostic_report to create observations')
            return None
        search_headers = {'Accept': 'application/json'}
        search_params = {'subject': pat_id, 'encounter': enc_id, 'category': 'fall_prevention'}
        resp = requests.get(self.api_base + 'Observation/', headers=search_headers, params=search_params)
        for code in data:
            updated_existing = False
            if resp.json()['total'] > 0:
                for obs in resp.json()['entry']:
                    if obs['resource']['code']['coding'][0]['system'] == 'fall_prevention' and obs['resource']['code']['coding'][0]['code'] == code:
                        print('updating an existing observation')
                        self.update_observation_by_observation(obs, data[code])
                        updated_existing = True
            if updated_existing:
                continue
            print('Creating a new observation')
            self.create_new_observation(code, data[code], pat_id=pat_id, enc_id=enc_id, diag_rpt=diag_rpt)

    # Function write a note observation to fhir. Takes in a list the question code we would like to save it as and
    # the content of the note. Writes a new observation if one did not previously exist. Updates existing one if it
    # existed.
    # Input: question_code list from the standards document, responses list to question, patient_id, encounter_id,
    # diagnostic report (the default uses client values if they have been set)
    # Returns: True if succeeds in creating/updating an observation or False if fails.
    def write_note_to_fhir(self, question_code, note_text, pat_id=None, enc_id=None, diag_rpt=None):
        if pat_id == None:
            pat_id = self.patient_id
        if enc_id == None:
            enc_id = self.encounter_id
        if diag_rpt == None:
            diag_rpt = self.diagnostic_report
        if not pat_id or not enc_id or not diag_rpt:
            print('I am missing a patient_id, encounter_id, or diagnostic_report to create observations')
            return None

        search_headers = {'Accept': 'application/json'}
        search_params = {'subject': pat_id, 'encounter': enc_id, 'category': 'fall_prevention'}
        resp = requests.get(self.api_base + 'Observation/', headers=search_headers, params=search_params)
        i = question_code
        updated_existing = False
        if resp.json()['total'] > 0:
            for obs in resp.json()['entry']:
                if obs['resource']['code']['coding'][0]['system'] == 'fall_prevention' and \
                                obs['resource']['code']['coding'][0]['code'] == question_code:
                    return self.update_observation_by_observation(obs, note_text)
        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        save_obs = {}
        save_obs['resourceType'] = "Observation"
        save_obs['status'] = "final"
        save_obs['category'] = {}
        save_obs['category']['coding'] = []
        save_obs['category']['coding'].append({})
        save_obs['category']['coding'][0]['code'] = 'fall_prevention'
        save_obs['category']['coding'][0]['display'] = 'Fall Prevention Assessment Results'
        save_obs['category']['coding'][0]['system'] = 'fall_prevention'
        save_obs['category']['coding'][0]['text'] = 'Fall Prevention Assessment Results'
        save_obs['code'] = {}
        save_obs['code']['coding'] = []
        save_obs['code']['coding'].append({})
        # save_obs['code']['coding']['system'] = 'http://fall_prevention_algorithm.org'
        save_obs['code']['coding'][0]['system'] = 'fall_prevention'
        # save_obs['code']['coding']['code'] = str(questions_code[i])
        save_obs['code']['coding'][0]['code'] = str(question_code)
        # save_obs['code']['coding']['display'] = str(questions[i])
        save_obs['code']['coding'][0]['display'] = self.questions_text[
            self.questions_code.index(str(question_code))]
        save_obs['code']['coding'][0]['text'] = self.questions_text[self.questions_code.index(str(question_code))]
        save_obs['subject'] = {}
        save_obs['subject']['reference'] = 'Patient/' + str(pat_id)
        save_obs['encounter'] = {}
        save_obs['encounter']['reference'] = enc_id
        save_obs['effectiveDateTime'] = (time.strftime("%Y-%m-%dT%H:%M:%S"))
        save_obs['valueQuantity'] = {}
        save_obs['valueQuantity']['value'] = str(note_text)
        save_obs['valueQuantity']['unit'] = 'Free form notes'
        save_obs['valueQuantity']['system'] = "fall_prevention"
        save_obs['valueQuantity']['code'] = "Free form notes"
        resp = requests.post(self.api_base + 'Observation/', data=json.dumps(save_obs), headers=write_headers)
        if resp.status_code != 201:
            print('Something went wrong when trying to write to the server')
            return False
        else:
            return True
            diag_rpt['resource']['result'].append({})
            diag_rpt['resource']['result'][-1]['reference'] = 'Observation/' + resp.json()['entry'][0]['resource']['id']
            return True

    # Function to create a new observation for a yes/no or true/false question.
    # Input: question_code from the standards document, response to question, patient_id, encounter_id
    # (the default uses client values if they have been set)
    # Returns: True if succeeds in creating a new observation or False if fails.
    # Note: Some of the coding names are a bit made up. We can probably just use them.
    # Sets effective date as current date.
    def create_new_observation(self, falls_question_code, response, pat_id=None, enc_id=None, diag_rpt=None):
        if pat_id == None:
            pat_id = self.patient_id
        if enc_id == None:
            enc_id = self.encounter_id
        if diag_rpt == None:
            diag_rpt = self.diagnostic_report
        if not pat_id or not enc_id or not diag_rpt:
            print('I am missing a patient_id, encounter_id, or diagnostic_report to create observations')
            return None

        # q_info = self.standards_document_dict[falls_question_code]
        q_ind = self.questions_code.index(str(falls_question_code))

        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        save_obs = {}
        save_obs['resourceType'] = "Observation"
        save_obs['status'] = "final"

        save_obs['category'] = {}
        save_obs['category']['coding'] = []
        save_obs['category']['coding'].append({})
        save_obs['category']['coding'][0]['code'] = 'fall_prevention'
        save_obs['category']['coding'][0]['display'] = 'Fall Prevention Assessment Results'
        save_obs['category']['coding'][0]['system'] = 'fall_prevention'
        save_obs['category']['coding'][0]['text'] = 'Fall Prevention Assessment Results'
        save_obs['code'] = {}
        save_obs['code']['coding'] = []
        save_obs['code']['coding'].append({})
        # save_obs['code']['coding']['system'] = 'http://fall_prevention_algorithm.org'
        save_obs['code']['coding'][0]['system'] = 'fall_prevention'
        # save_obs['code']['coding']['code'] = str(questions_code[i])
        save_obs['code']['coding'][0]['code'] = str(falls_question_code)
        # save_obs['code']['coding']['display'] = str(questions[i])
        save_obs['code']['coding'][0]['display'] = self.questions_text[q_ind]
        save_obs['code']['coding'][0]['text'] = self.questions_text[q_ind]
        save_obs['subject'] = {}
        save_obs['subject']['reference'] = 'Patient/'+str(pat_id)
        save_obs['encounter'] = {}
        save_obs['encounter']['reference'] = enc_id
        save_obs['effectiveDateTime'] = (time.strftime("%Y-%m-%dT%H:%M:%S"))
        save_obs['valueCodeableConcept'] = {}
        save_obs['valueCodeableConcept']['coding'] = []
        save_obs['valueCodeableConcept']['coding'].append({})
        # save_obs['valueCodeableConcept']['coding']['value'] = str(response)
        # if not str(response):
            # response = ''
        save_obs['valueCodeableConcept']['coding'][0]['code'] = str(response)
        save_obs['valueCodeableConcept']['coding'][0]['system'] = self.questions_units[q_ind]
        save_obs['valueCodeableConcept']['coding'][0]['display'] = self.questions_answer_description[q_ind]
        # print('This observation response:', str(response))
        # save_obs['valueCodeableConcept']['value'] = str(response)
        # save_obs['valueCodeableConcept']['unit'] = self.questions_units[q_ind]
        # save_obs['valueCodeableConcept']['system'] = "fall_prevention"
        # save_obs['valueCodeableConcept']['code'] = self.questions_answer_description[q_ind]
        resp = requests.post(self.api_base + 'Observation/', data=json.dumps(save_obs), headers=write_headers)
        print('response:', resp)
        print(resp.json())
        if resp.status_code != 201:
            print('Something went wrong when trying to write to the server')
            return False
        else:
            return True
            diag_rpt['resource']['result'].append({})
            diag_rpt['resource']['result'][-1]['reference'] = 'Observation/'+resp.json()['entry'][0]['resource']['id']
            return True

    # Update an existing observation, searched by ID
    # Input: medication_order_id (from the searched medication order list), response (value for observation),
    # patient_id (defaults to the client's patient id if it has been set).
    # Returns: True if write is successful. False otherwise.
    def update_observation_by_id(self, observation_id, response, pat=None):
        if pat == None:
            pat = self.patient_id
        if not pat:
            print('I am missing a patient_id to search for relevant medications')
            return False
        print('Updating observation ID:', observation_id)
        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        search_headers = {'Accept': 'application/json'}
        search_params = {'patient': pat}
        resp = requests.get(self.api_base + 'Observation/' + observation_id, headers=search_headers,
                            params=search_params)
        if resp.status_code != 200:
            print('Could not find the medication order by that medication order id and patient id or something else ' \
                  'went wrong.')
            return False
        alter_obs = resp.json()
        if 'valueCodeableConcept' in alter_obs.keys():
            alter_obs['valueCodeableConcept']['coding'][0]['code'] = str(response)
        else:
            print('Tried to update observation using codeable concept but old observation used valueQuantity')
        alter_obs['effectiveDateTime'] = (time.strftime("%Y-%m-%dT%H:%M:%S"))
        resp = requests.put(self.api_base + 'Observation/' + observation_id, data=json.dumps(alter_obs),
                            headers=write_headers)
        if resp.status_code != 200:
            print('Something went wrong in writing the update to end the medication order by setting its status to ' \
                  'complete')
            return False
        else:
            return True

    # Update an existing observation, selected by putting in the entire observation (e.g., raw from search).
    # Input: observation (from the searched observation), response (value for observation)
    # Returns: True if write is successful. False otherwise.
    def update_observation_by_observation(self, observation, response):
        pat = observation['resource']['subject']['reference'].split('/')[1]
        observation_id = observation['resource']['id']
        print('Updating observation ID:', observation_id)
        write_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        search_headers = {'Accept': 'application/json'}
        search_params = {'patient': pat}
        resp = requests.get(self.api_base + 'Observation/' + observation_id, headers=search_headers,
                            params=search_params)
        if resp.status_code != 200:
            print('Could not find the observation or something else ' \
                  'went wrong.')
            return False
        alter_obs = resp.json()
        if 'valueCodeableConcept' in alter_obs.keys():
            alter_obs['valueCodeableConcept']['coding'][0]['code'] = str(response)
        else:
            print('Tried to update observation using codeable concept but old observation used valueQuantity')
        alter_obs['effectiveDateTime'] = (time.strftime("%Y-%m-%dT%H:%M:%S"))
        resp = requests.put(self.api_base + 'Observation/' + observation_id, data=json.dumps(alter_obs),
                            headers=write_headers)
        if resp.status_code != 200:
            print('Something went wrong in writing the update to end the medication order by setting its status to ' \
                  'complete')
            return False
        else:
            return True


if __name__ == "__main__":
    # This is some example of how to run this:
    # QUESTIONS_URL = "https://raw.githubusercontent.com/akapusta/team_falls/master/standards/questions.json"
    # with ur.urlopen(QUESTIONS_URL) as url_questions:
    #     questions = json.loads(url_questions.read().decode('utf8'))

    client = FallsFHIRClient()
    # client.load_standards_document(questions)

    # Search for a patient by first and last name
    patients = client.search_patient('Stephan P.', 'Graham')
    print('Patient info:')
    print(patients[0], '\n')
    print(patients[0]['resource']['name'][0]['given'], '\n')
    print(patients[0]['resource']['name'][0]['family'], '\n')

    # Or search by name and date of birth
    patients = client.search_patient_dob('Sarah', 'Graham', '1949')
    print('Patient info:')
    print(patients[0], '\n')

    # Set the client's patient to the client we just found by the patient id in the first person from the search
    client.select_patient(patients[0]['resource']['id'])

    # Or set the client's patient by just giving it the whole patient resource
    client.select_patient_from_patient_result(client.search_patient('Sarah', 'Graham'))
    print('Patient ID:')
    print(client.patient_id, '\n')

    patient = client.search_patient_by_id(pat=client.patient_id)
    # print(patient)
    print(patient[0]['resource'])
    # print(patient['resource'][0]['id'])

    # Search for encounters by the patient by searching the date. The date must be right.
    encounters = client.search_encounter_all()
    # print(len(encounters))
    # for enc in encounters:
    #     print(enc['resource']['patient'])
    client.select_encounter_from_encounter_result(encounters)
    # client.create_new_encounter(set_as_active_encounter=True)

    # client.select_encounter(patients[0]['resource']['id'])
    print('Encounter ID:')
    print(client.encounter_id, '\n')

    # Search for all medications being taken by the patient
    meds = client.search_medication()

    # See the last medication order on the list
    print('The last medication on the list is:')
    # print(meds[-1], '\n')

    # End that medication order (e.g., if doctor decides to change the prescription)
    # Commented out so you don't keep removing medications.
    # client.end_medication_by_order(meds[-1])
    # print 'Ended medication!', '\n'

    # If the standards document has been updated, run this to update the dict the client is using to perform its search
    # for relevant observations
    # client.load_standards_document("https://raw.githubusercontent.com/akapusta/team_falls/master/standards/questions.json")

    # Find all observations that are on fall prevention for this patient and this encounter:
    # current_obs = client.search_observations()
    # print('Observations for this patient and this encounter:')
    # print(current_obs, '\n')

    # Write to FHIR server a bunch of observations from the app. Makes new observations if a previous one does not
    # exist for this question and this encounter. Updates existing observation if it does exist.
    # 1 is for yes. 0 is for no.
    question_codes = ['1', '2', '7']
    responses = ['1', '0', '1', '1', '0']

    # question_codes = client.questions_code[]
    client.diagnostic_report = True
    # client.write_list_of_observations_to_fhir(question_codes, responses)



    print('Did a bunch of things!!')
