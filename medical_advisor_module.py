from functools import reduce
import requests


class MedicalAdvisor:
    def __init__(self):
        self.ACCEPTANCE_STATEMENT = "I have read, understood and I accept and agree to comply with the Terms of Use " \
                                    "of EndlessMedicalAPI and Endless Medical services. The Terms of Use are " \
                                    "available on endlessmedical.com"
        self.base_url = "https://api.endlessmedical.com"
        self.session_id = None

    def init_session(self) -> None:
        """
        This method generates session id which is necessary for Medical Advisor application to run
        :return: self.session_id
        """
        end_point = self.base_url + "/v1/dx/InitSession"
        response = requests.get(end_point).json()
        self.session_id = response["SessionID"]

    def accept_terms_of_use(self) -> None:
        """
        Agree with Medical Advisor terms of use
        This method is necessary for application to provide any kind of diagnosis
        :return: whether operation is successful
        """
        end_point = self.base_url + "/v1/dx/AcceptTermsOfUse"
        request_data = {"SessionID": self.session_id,
                        "passphrase": self.ACCEPTANCE_STATEMENT}
        requests.request("POST", end_point, params=request_data)

    def set_use_of_default_values(self, value: bool) -> None:
        """
        Set each value to the defaults if it is not provided by the patient
        :param value: bool
        :return: whether operation is successful
        """
        end_point = self.base_url + "/v1/dx/SetUseDefaultValues"
        request_data = {"SessionID": self.session_id,
                        "value": value}
        requests.request("POST", end_point, params=request_data)

    def add_symptom(self, feature_name: str, value: int) -> None:
        """
        Add symptom
        :param feature_name: str
        :param value: bool
        :return: whether operation is successful
        """
        end_point = self.base_url + "/v1/dx/UpdateFeature"
        request_data = {"SessionID": self.session_id,
                        "name": feature_name,
                        "value": value}
        requests.request("POST", end_point, params=request_data)

    def delete_feature(self, feature_name: str) -> None:
        """
        Delete symptom
        :param feature_name: str
        """
        end_point = self.base_url + "/v1/dx/DeleteFeature"
        request_data = {"SessionID": self.session_id,
                        "name": feature_name}
        requests.request("POST", end_point, params=request_data)

    def analyze(self, number_of_results: int) -> dict:
        """
        List first number_of_results possible diagnosis
        :param number_of_results: int
        :return: dict
        """
        end_point = self.base_url + "/v1/dx/Analyze"
        request_data = {"SessionID": self.session_id,
                        "NumberOfResults": number_of_results}
        response = requests.get(end_point, request_data).json()
        if response["status"] == "ok":
            analysis = response["Diseases"]
            return analysis
        return {}

    def get_suggested_specializations(self, number_of_results: int) -> dict:
        """
        Direct patient to visit certain specialization based on his symptoms
        :param number_of_results: int
        :return: dict
        """
        end_point = self.base_url + "/v1/dx/GetSuggestedSpecializations"
        request_data = {"SessionID": self.session_id,
                        "NumberOfResults": number_of_results}
        response = requests.get(end_point, request_data).json()
        if response["status"] == "ok":
            suggested_specializations = response["SuggestedSpecializations"]
            return suggested_specializations
        return {}

    def get_suggested_tests(self, number_of_results: int) -> list:
        """
        Get number_of_results more tests for patient to pass in order to increase the accuracy of diagnosis
        :param number_of_results: int
        :return: list
        """
        end_points = self.base_url + "/v1/dx/GetSuggestedFeatures_PatientProvided", \
                     self.base_url + "/v1/dx/GetSuggestedFeatures_PhysicianProvided", \
                     self.base_url + "/v1/dx/GetSuggestedFeatures_Tests"
        request_data = {"SessionID": self.session_id,
                        "NumberOfResults": number_of_results}
        responses = []
        for end_point in end_points:
            response = requests.get(end_point, request_data).json()["SuggestedFeatures"]
            responses.append(response)
        suggested_tests = reduce(lambda x, y: x + y, responses)
        sorted_suggested_tests = sorted(suggested_tests, key=lambda el: el[-1], reverse=True)[:number_of_results + 1]
        tests = [test[0] for test in sorted_suggested_tests]
        return tests


# if __name__ == '__main__':
#     medical_advisor = MedicalAdvisor()
#     medical_advisor.init_session()
#     medical_advisor.accept_terms_of_use()
#     medical_advisor.set_use_of_default_values(True)
#     print(medical_advisor.analyze(5))
    # medical_advisor.analyze(5)
    # print(medical_advisor.get_suggested_specializations(5))
