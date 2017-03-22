# from __future__ import print_function
import json

def run():
    '''
    Function to check if medication file was formatted correctly
    '''

    med_file = open("medication.json", "r")
    med = json.load(med_file)
    gpi_list = []

    for i in range(0, len(med)):
        for j in range(0, len(med[i].get("gpi_codes"))):
            gpi_list.append(med[i].get("gpi_codes")[j])

    for code in gpi_list:
        if code < 1000000000 or code > 9999999999:
            print("Incorrectly formatted code: " + code)

    for i in range(0, len(gpi_list) - 1):
        if gpi_list[i] == gpi_list[i + 1]:
            print("Incorrectly formatted code: " + str(gpi_list[i]) + " " + str(gpi_list[i + 1]))

    for i in range(0, len(gpi_list) - 2):
        if gpi_list[i] == gpi_list[i + 2]:
            print("Incorrectly formatted code: " + str(gpi_list[i]) + " " + str(gpi_list[i + 2]))

if __name__ == '__main__':
    run()
