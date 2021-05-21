import unittest
from medical_advisor_module import MedicalAdvisor


class TestMedicalAdvisor(unittest.TestCase):
    def setUp(self) -> None:
        self.medical_advisor = MedicalAdvisor()
        self.medical_advisor.init_session()
        self.medical_advisor.accept_terms_of_use()
        self.medical_advisor.set_use_of_default_values(True)
        self.number_of_results = 5
        self.covid_19_symptoms = [("DyspneaSeveritySubjective", 4), ("SeverityCough", 4), ("DiarrheaSx", 3),
                                  ("LossOfSmell", 3), ("LossOfTaste", 3)]
        self.hypertension_symptoms = [("HeadacheAssociatedWithHTN", 3), ("ChestPainSeverity", 2), ("GrossHematuria", 3),
                                      ("GeneralizedFatigue", 3)]
        self.diabetes_symptoms = [("WeightLoss", 6), ("SkinMoistureHx", 3), ("GrossHematuria", 3),
                                  ("UrinaryFrequency", 3), ("VisualAcuityRos", 6)]

    def test_covid_19(self):
        for covid_symptom in self.covid_19_symptoms:
            self.medical_advisor.add_symptom(covid_symptom[0], covid_symptom[1])
        self.assertEqual('COVID-19 virus identified' in self.medical_advisor.analyze(self.number_of_results), True)

    def test_hypertension(self):
        for hypertension_symptom in self.hypertension_symptoms:
            self.medical_advisor.add_symptom(hypertension_symptom[0], hypertension_symptom[1])
        self.assertEqual('Headache due to uncontrolled hypertension.' in
                         self.medical_advisor.analyze(self.number_of_results), True)

    def test_diabetes(self):
        self.medical_advisor.set_use_of_default_values(False)
        for diabetes_symptom in self.diabetes_symptoms:
            self.medical_advisor.add_symptom(diabetes_symptom[0], diabetes_symptom[1])
        self.assertEqual('Diabetes melltus type 2' in
                         self.medical_advisor.analyze(self.number_of_results), True)

    def test_get_suggested_specializations(self):
        self.medical_advisor.add_symptom("LossOfSmell", 3)
        self.medical_advisor.analyze(self.number_of_results)
        self.assertEqual('Internal medicine' in
                         self.medical_advisor.get_suggested_specializations(self.number_of_results), True)

    def test_get_suggested_tests(self):
        self.medical_advisor.add_symptom("LossOfTaste", 3)
        self.medical_advisor.analyze(5)
        self.assertEqual("ExposureToCovid" in self.medical_advisor.get_suggested_tests(self.number_of_results), True)


if __name__ == '__main__':
    unittest.main()
