"""Test the analysis module."""
import pytest
from analysis import patient_age, patient_is_sick, parse_data
from fake_files import fake_files


def test_patient_data() -> None:
    """Test the patient_data function in analysis python."""
    with fake_files(  # list of list (table) as txt file
        [
            [
                "PatientID",
                "PatientGender",
                "PatientDateOfBirth",
                "PatientRace",
                "PatientMaritalStatus",
                "PatientLanguage",
                "PatientPopulationPercentageBelowPoverty",
            ],
            [
                "1",
                "M",
                "1990-01-01 00:00:00.000",
                "White",
                "Married",
                "English",
                "0.1",
            ],
            [
                "2",
                "F",
                "1990-01-01 00:00:00.000",
                "White",
                "Married",
                "English",
                "0.1",
            ],
            [
                "3",
                "M",
                "1989-01-01 00:00:00.000",
                "Asian",
                "Unkown",
                "Chinese",
                "0.2",
            ],
            [
                "4",
                "F",
                "1979-01-01 00:00:00.000",
                "Black",
                "Divorced",
                "English",
                "0.3",
            ],
            [
                "5",
                "M",
                "1969-01-01 00:00:00.000",
                "Unknown",
                "Single",
                "Spanish",
                "0.4",
            ],
        ],
        [
            [
                "PatientID",
                "AdmissionID",
                "LabName",
                "LabValue",
                "LabUnits",
                "LabDateTime",
            ],
            [
                "1",
                "1",
                "METABOLIC: ALBUMIN",
                "4.0",
                "g/dL",
                "2019-01-01 00:00:00.000",
            ],
        ],
    ) as (patient_file, lab_file):
        assert parse_data(patient_file, lab_file) == (
            {
                "1": {  # patient_id
                    "PatientGender": "M",
                    "PatientDateOfBirth": "1990-01-01 00:00:00.000",
                    "PatientRace": "White",
                    "PatientMaritalStatus": "Married",
                    "PatientLanguage": "English",
                    "PatientPopulationPercentageBelowPoverty": "0.1",
                },
                "2": {
                    "PatientGender": "F",
                    "PatientDateOfBirth": "1990-01-01 00:00:00.000",
                    "PatientRace": "White",
                    "PatientMaritalStatus": "Married",
                    "PatientLanguage": "English",
                    "PatientPopulationPercentageBelowPoverty": "0.1",
                },
                "3": {
                    "PatientGender": "M",
                    "PatientDateOfBirth": "1989-01-01 00:00:00.000",
                    "PatientRace": "Asian",
                    "PatientMaritalStatus": "Unkown",
                    "PatientLanguage": "Chinese",
                    "PatientPopulationPercentageBelowPoverty": "0.2",
                },
                "4": {
                    "PatientGender": "F",
                    "PatientDateOfBirth": "1979-01-01 00:00:00.000",
                    "PatientRace": "Black",
                    "PatientMaritalStatus": "Divorced",
                    "PatientLanguage": "English",
                    "PatientPopulationPercentageBelowPoverty": "0.3",
                },
                "5": {
                    "PatientGender": "M",
                    "PatientDateOfBirth": "1969-01-01 00:00:00.000",
                    "PatientRace": "Unknown",
                    "PatientMaritalStatus": "Single",
                    "PatientLanguage": "Spanish",
                    "PatientPopulationPercentageBelowPoverty": "0.4",
                },
            },
            {
                # lab...
                "1": [
                    {
                        "PatientID": "1",
                        "AdmissionID": "1",
                        "LabName": "METABOLIC: ALBUMIN",
                        "LabValue": "4.0",
                        "LabUnits": "g/dL",
                        "LabDateTime": "2019-01-01 00:00:00.000",
                    }
                ],
            },
        )


def test_patient_age() -> None:
    with fake_files(  # list of list (table) as txt file
        [
            [
                "PatientID",
                "PatientGender",
                "PatientDateOfBirth",
                "PatientRace",
                "PatientMaritalStatus",
                "PatientLanguage",
                "PatientPopulationPercentageBelowPoverty",
            ],
            [
                "1",
                "M",
                "1990-01-01 00:00:00.000",
                "White",
                "Married",
                "English",
                "0.1",
            ],
            [
                "2",
                "F",
                "1990-01-01 00:00:00.000",
                "White",
                "Married",
                "English",
                "0.1",
            ],
            [
                "3",
                "M",
                "1989-01-01 00:00:00.000",
                "Asian",
                "Unkown",
                "Chinese",
                "0.2",
            ],
            [
                "4",
                "F",
                "1979-01-01 00:00:00.000",
                "Black",
                "Divorced",
                "English",
                "0.3",
            ],
            [
                "5",
                "M",
                "1969-01-01 00:00:00.000",
                "Unknown",
                "Single",
                "Spanish",
                "0.4",
            ],
        ],
        [
            [
                "PatientID",
                "AdmissionID",
                "LabName",
                "LabValue",
                "LabUnits",
                "LabDateTime",
            ],
            [
                "1",
                "1",
                "METABOLIC: ALBUMIN",
                "4.0",
                "g/dL",
                "2019-01-01 00:00:00.000",
            ],
        ],
    ) as (patient_file, lab_file):
        result = parse_data(patient_file, lab_file)
        assert patient_age(result, "1") == 30
        assert patient_age(result, "2") == 30
        assert patient_age(result, "3") == 31
        assert patient_age(result, "4") == 41
        assert patient_age(result, "5") == 51


# def test_patient_is_sick()-> None:
#     with fake_fake_files(  # list of list (table) as txt file
#         [
#             [
#                 "PatientID",
#                 "PatientGender",
#                 "PatientDateOfBirth",
#                 "PatientRace",
#                 "PatientMaritalStatus",
#                 "PatientLanguage",
#                 "PatientPopulationPercentageBelowPoverty",
#             ],
#             [
#                 "1",
#                 "M",
#                 "1990-01-01 00:00:00.000",
#                 "White",
#                 "Married",
#                 "English",
#                 "0.1",
#             ],
#             [
#                 "2",
#                 "F",
#                 "1990-01-01 00:00:00.000",
#                 "White",
#                 "Married",
#                 "English",
#                 "0.1",
#             ],
#             [
#                 "3",
#                 "M",
#                 "1989-01-01 00:00:00.000",
#                 "Asian",
#                 "Unkown",
#                 "Chinese",
#                 "0.2",
#             ],
#             [
#                 "4",
#                 "F",
#                 "1979-01-01 00:00:00.000",
#                 "Black",
#                 "Divorced",
#                 "English",
#                 "0.3",
#             ],
#             [
#                 "5",
#                 "M",
#                 "1969-01-01 00:00:00.000",
#                 "Unknown",
#                 "Single",
#                 "Spanish",
#                 "0.4",
#             ],
#         ],
#         [
#             [
#                 "PatientID",
#                 "AdmissionID",
#                 "LabName",
#                 "LabValue",
#                 "LabUnits",
#                 "LabDateTime",
#             ],
#             [
#                 "1",
#                 "1",
#                 "METABOLIC: ALBUMIN",
#                 "4.0",
#                 "g/dL",
#                 "2019-01-01 00:00:00.000",
#             ],
#         ],
#     ) as (patient_file, lab_file):
