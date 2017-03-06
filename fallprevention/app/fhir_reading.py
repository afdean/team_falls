#!/usr/bin/env python

from fhirclient import client

import fhirclient.models.patient as fhir_patient
import fhirclient.models.encounter as fhir_encounter
import fhirclient.models.procedure as fhir_procedure
import fhirclient.models.observation as fhir_observation
import fhirclient.models.practitioner as fhir_practitioner
import fhirclient.models.humanname as fhir_hn



settings = {
    'app_id': 'team_falls_app',
    'api_base': 'https://fhir-open-api-dstu2.smarthealthit.org'
}
smart = client.FHIRClient(settings=settings)

patient = fhir_patient.Patient.read('hca-pat-1', smart.server)
patient.birthDate.isostring
print str(patient.birthDate.isostring)
# '1963-06-12'
smart.human_name(patient.name[0])
print smart.human_name(patient.name[0])
# 'Christy Ebert'

name = fhir_hn.HumanName()
name.given = ['Christy']
name.family = ['Ebert']
# patient.name = [name]
# print name.isostring
search = fhir_patient.Patient.where(struct={'given': 'Christy', 'family':'Ebert'})
# search = fhir_patient.Patient.where(struct={'name': name.as_json()})#, 'birthDate': '1963-06-12'})
# patients = search.perform(smart.server)
patients = search.perform_resources(smart.server)
for patient in patients:
    print patient.name[0].as_json()
    # patient.name.to_json()
    # print smart.human_name(patient[0])

# search = encounter.Procedure.where(struct={'subject': 'hca-pat-1', 'status': 'completed'})
# procedures = search.perform_resources(smart.server)
# for procedure in procedures:
#     procedure.as_json()
#     # {'status': u'completed', 'code': {'text': u'Lumpectomy w/ SN', ...
#
# # to get the raw Bundle instead of resources only, you can use:
# bundle = search.perform(smart.server)