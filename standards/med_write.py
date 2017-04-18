def run():
    med_file = open("medication_data.txt", "r")
    med = open("medication.json", "w")

    med_list = med_file.readlines()
    med.write("[\n")

    for i in range(0, len(med_list)):
        med.write("  {\n")
        med.write("    \"name\": \"" + med_list[i][:-1] + "\",\n")
        med.write("    \"date\": \"" + "2015-12" + "\",\n")
        med.write("    \"gpi_codes\": [],\n")
        med.write("    \"rx_codes\": []\n")
        if i < len(med_list) - 1:
            med.write("  },\n")
        else:
            med.write("  }\n")

if __name__ == '__main__':
    run()
