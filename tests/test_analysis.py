"""Test the analysis module."""
from analysis import patient_age, patient_is_sick, parse_data
from fake_files import fake_files

with fake_files(
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
            "Male",
            "1947-12-28 02:45:40.547",
            "Unknown",
            "Married",
            "Icelandic",
            "18.08",
        ],
        [
            "2",
            "Female",
            "1970-07-25 13:04:20.717",
            "Asian",
            "Married",
            "English",
            "6.67",
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
    records = parse_data(patient_file, lab_file)


def test_patient_data() -> None:
    """Test the patient_data function in analysis python."""
    assert records == (
        {
            "1": {
                "PatientID": "1",
                "PatientGender": "Male",
                "PatientDateOfBirth": "1947-12-28 02:45:40.547",
                "PatientRace": "Unknown",
                "PatientMaritalStatus": "Married",
                "PatientLanguage": "Icelandic",
                "PatientPopulationPercentageBelowPoverty": "18.08",
            },
            "2": {
                "PatientID": "2",
                "PatientGender": "Female",
                "PatientDateOfBirth": "1970-07-25 13:04:20.717",
                "PatientRace": "Asian",
                "PatientMaritalStatus": "Married",
                "PatientLanguage": "English",
                "PatientPopulationPercentageBelowPoverty": "6.67",
            },
        },
        {
            "1": [
                {
                    "PatientID": "1",
                    "AdmissionID": "1",
                    "LabName": "METABOLIC: ALBUMIN",
                    "LabValue": "4.0",
                    "LabUnits": "g/dL",
                    "LabDateTime": "2019-01-01 00:00:00.000",
                }
            ]
        },
    )


def test_patient_age() -> None:
    """ "Test the patient_age function in analysis python."""
    assert patient_age(records, "1") == 75
    assert patient_age(records, "2") == 52


def test_patient_is_sick() -> None:
    """Test the patient_is_sick function in analysis python."""
    assert (
        patient_is_sick(records, "1", "METABOLIC: ALBUMIN", ">", 5.0) is False
    )
    assert (
        patient_is_sick(records, "1", "METABOLIC: ALBUMIN", "<", 5.0) is True
    )
    assert (
        patient_is_sick(records, "1", "METABOLIC: ALBUMIN", ">", 2.0) is True
    )
