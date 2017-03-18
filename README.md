# CS 6440: Health Informatics Project
Repository for Georgia Tech CS6440 group "Team Falls"

## Overview
This is a clinical decision support app for to assist physicians in fall prevention support for the elderly.
It is a direct implementation of the STEADI algorithm that provides flexibility for individual clinics through modular design.
Previous implementations have been attempted to transform the STEADI algorithm into an app, but they struggled to address three aspects in particular:

    1. Modularity
    2. Interoperability
    3. Maintainability

With respect to modularity, our goal is to reduce the clutter in the page, and simplify the process so that any provider only sees what is relevant at any point during the course of using the app. Although our app adheres tightly to the flow of the algorithm, the app's ability to jump between broad categories of the algorithm fulfills the modularity requirement. Furthermore, the ability of the patient to login to answer self-assessment questions allows individual clinics to expedite the entire process.

With respect to interoperability, our solution is to use FHIR to add our app to the SMART on FHIR catalog.

With respect to maintainability, the usage of FHIR allows us to give more control to the CDC on what appears on the app at any given point. Given the amount of flexibility FHIR gives its users in terms of reading and writing data, we solve our problem of maintainability by populating as much of the pages of the app as possible at launch from information pulled from JSON documents. We refer to these as the "standards documents".

## Dependencies

    * Python3
    * Django
    * Django-Crispy-Forms
    * Memcached

    Using OSX:
    * pip3 install Django
    * brew install memcached

### Standards Documents
These are hosted on a github page maintained by the CDC:

    * questions.json
    * func_ability_test.json
    * medication.json
    * physical_exam.json

questions.json includes all screening questions, and the logic for the screening test. Both are pulled from the "Stay Independent Brochure." Each question object includes the following fields:

    * content: String representing the question itself
    * code: String representing a code to match FHIR resources
    * score: Integer indicating the weight of the question when its scored to determine risk level
    * is_key: Boolean indicating if the question is key or not
    * medication_related: Boolean indicating if the answer is relevant to the medication screening process
    * reason: String representing why the question is relevant

The question logic object includes the following fields:
    * min_score: Integer indicating the minimum score needed to fail.
    * min_key: Integer indicating the minimum number of key questions answered "yes" needed to fail.

func_ability_test.json includes all of the functional ability tests that can be conducted provided the patient "fails" the screening process. Each functional ability test object includes the following fields:

    * name: String representing the name of the test
    * is_recommended: Boolean indicating if the test is recommended above the others.
    * video_link: String containing a URL to video instructions for the test, hosted by the CDC.
    * pdf_link: String containing a URL to a PDF with instructions for the test
    * test_parameters:
    * integer_parameters: String indicating the name of an integer field related to the question
    * boolean_parameters: String indicating the name of a boolean field related to the question

medication.json includes all medications related to the AGS 2015 Beers Criteria at the time of writing. Each medication object includes the following fields:

    * name: String representing the name of the medicine
    * date: String representing the date the medicine was classified in the Beers Criteria
    * gpi_codes: Array of integers representing the first 10 digits of a medication's GPI code to be matched.

JSON objects can be easily added/modified to the files provided it is formatted in accordance to the fields. The app simply iterates through all objects to fill the pages. Keep this in mind when adding or removing objects, since the order in which they appear in an array matters for the order they appear on a page. Modification to existing objects must keep the data structure intact (i.e do not change an integer into a string).

### FHIR
We use three different resources to keep track of data on FHIR:

    1. Observations: Contains very small amounts of data. Each observation contains the answer to a single question. For example, an observation would be “I fell in the past 30 days”: value=True. The observation contains references to the patient, the provider, and the encounter.
    2. Encounters: Records a visit to the doctor. Includes the patient, status (complete or in progress), location, date, and type of visit(emergency, inpatient, outpatient)
    3. Procedures: Contains the type of assessment or procedure being done (fall assessment). Procedures reference the patient, provider, and encounter. There is no direct connection between observations and procedures; they are connected through the encounter.

When accessing the app, patients’ answers are associated with an upcoming appointment with a doctor. Each answered question is saved as an observation.When providers access the app, the app looks up observations associated with the encounter that match question codes from our standards document. Questions with saved observations will fill in with those answers. Questions with unsaved observations (if previously answered or a new question since the form was previously filled) will say that they have not yet been answered.The app saves responses to FHIR at almost any time. At the point its saved, current responses are saved as Observations in FHIR. Every time the App is launched, it checks for observations in FHIR based on the standards documents.When the provider selects the patient, all relevant FHIR information is loaded into memory for the session.
# something about the pages themselves and design?




