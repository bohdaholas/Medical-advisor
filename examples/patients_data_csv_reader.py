import csv


class Patient:
    def __init__(self, patient_data):
        self.patient_data = patient_data


with open("diabetes_registry.csv") as file:
    patients_data = list(csv.reader(file))
    obtained_patient_data = patients_data[0]
    patients = []
    for patient in patients_data:
        patient_data = {}
        for idx, value in enumerate(patient):
            patient_data[obtained_patient_data[idx]] = value
        patients.append(Patient(patient_data))
