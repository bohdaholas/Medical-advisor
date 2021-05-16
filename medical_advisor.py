from functools import reduce
import requests


class MedicalAdvisor:
    def __init__(self):
        self.ACCEPTANCE_STATEMENT = "I have read, understood and I accept and agree to comply with the Terms of Use " \
                                    "of EndlessMedicalAPI and Endless Medical services. The Terms of Use are " \
                                    "available on endlessmedical.com"
        self.base_url = "https://api.endlessmedical.com"

    def init_session(self) -> str:
        """
        This method generates session id which is necessary for Medical Advisor application to run
        :return: session_id
        """
        end_point = self.base_url + "/v1/dx/InitSession"
        response = requests.get(end_point).json()
        if response["status"] == "ok":
            session_id = response["SessionID"]
            return session_id
        return ""

    def accept_terms_of_use(self, session_id: str) -> bool:
        """
        Agree with Medical Advisor terms of use
        This method is necessary for application to provide any kind of diagnosis
        :param session_id:
        :return: whether operation is successful
        """
        end_point = self.base_url + "/v1/dx/AcceptTermsOfUse"
        request_data = {"SessionID": session_id,
                        "passphrase": self.ACCEPTANCE_STATEMENT}
        response = requests.request("POST", end_point, params=request_data)
        if response.status_code == 200:
            return True
        return False

    def set_use_of_default_values(self, session_id: str, value: bool):
        """
        Set each value to the defaults if it is not provided by the patient
        :param session_id: str
        :param value: bool
        :return: whether operation is successful
        """
        end_point = self.base_url + "/v1/dx/SetUseDefaultValues"
        request_data = {"SessionID": session_id,
                        "value": value}
        response = requests.request("POST", end_point, params=request_data)
        if response.status_code == 200:
            return True
        return False

    def add_feature(self, session_id: str, feature_name: str, value: int) -> bool:
        """
        Set each value to the defaults if it is not provided by the patient
        :param session_id: str
        :param feature_name: str
        :param value: bool
        :return: whether operation is successful
        """
        end_point = self.base_url + "/v1/dx/UpdateFeature"
        request_data = {"SessionID": session_id,
                        "name": feature_name,
                        "value": value}
        response = requests.request("POST", end_point, params=request_data)
        if response.status_code == 200:
            return True
        return False

    def delete_feature(self, session_id: str, feature_name: str):
        """
        Set each value to the defaults if it is not provided by the patient
        :param session_id: str
        :param feature_name: str
        :return: whether operation is successful
        """
        end_point = self.base_url + "/v1/dx/DeleteFeature"
        request_data = {"SessionID": session_id,
                        "name": feature_name}
        response = requests.request("POST", end_point, params=request_data)
        if response.status_code == 200:
            return True
        return False

    def get_suggested_specializations(self, session_id: str, number_of_results: int) -> dict:
        """
        Direct patient to visit certain specialization based on his symptoms
        :param session_id: str
        :param number_of_results: int
        :return: dict
        """
        end_point = self.base_url + "/v1/dx/GetSuggestedSpecializations"
        request_data = {"SessionID": session_id,
                        "NumberOfResults": number_of_results}
        response = requests.get(end_point, request_data).json()
        if response["status"] == "ok":
            suggested_specializations = response["SuggestedSpecializations"]
            return suggested_specializations
        return {}

    def get_suggested_tests(self, session_id: str, number_of_results: int) -> list:
        """
        Get number_of_results more tests for patient to pass in order to increase the accuracy of diagnosis
        :param session_id: str
        :param number_of_results: int
        :return: list
        """
        end_points = self.base_url + "/v1/dx/GetSuggestedFeatures_PatientProvided", \
                     self.base_url + "/v1/dx/GetSuggestedFeatures_PhysicianProvided", \
                     self.base_url + "/v1/dx/GetSuggestedFeatures_Tests"
        request_data = {"SessionID": session_id,
                        "NumberOfResults": number_of_results}
        responses = []
        for end_point in end_points:
            response = requests.get(end_point, request_data).json()["SuggestedFeatures"]
            responses.append(response)
        suggested_tests = reduce(lambda x, y: x + y, responses)
        sorted_suggested_tests = sorted(suggested_tests, key=lambda el: int(el[-1]))
        tests = [test[0] for test in sorted_suggested_tests]
        return tests

    def analyze(self, session_id: str, number_of_results: int) -> dict:
        """
        List first number_of_results possible diagnosis
        :param session_id: str
        :param number_of_results: int
        :return: dict
        """
        end_point = self.base_url + "/v1/dx/Analyze"
        request_data = {"SessionID": session_id,
                        "NumberOfResults": number_of_results}
        response = requests.get(end_point, request_data).json()
        if response["status"] == "ok":
            analysis = response["Diseases"]
            return analysis
        return {}


if __name__ == '__main__':
    medical_advisor = MedicalAdvisor()
    user_session_id = medical_advisor.init_session()
    medical_advisor.accept_terms_of_use(user_session_id)
    medical_advisor.set_use_of_default_values(user_session_id, True)
    print(medical_advisor.get_suggested_tests(user_session_id, 5))
