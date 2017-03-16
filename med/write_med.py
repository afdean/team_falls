import datetime

def run():
    med_file = open("medication_data.txt", "r")
    med = open("medication.json", "w")
    med_list = med_file.readlines()
    for i in range(0, len(med_list)):
        med.write("  {\n")
        med.write("    \"model\": \"app.Medication\",\n")
        med.write("    \"pk\": " + str(i + 1) + ",\n")
        med.write("    \"fields\": {\n")
        med.write("      \"name\": \"" + med_list[i][:-1] + "\",\n")
        med.write("      \"date\": \"" + str(datetime.date(2015,12,1)) + "\"\n")
        med.write("    }\n")
        med.write("  },\n")

if __name__ == '__main__':
    run()