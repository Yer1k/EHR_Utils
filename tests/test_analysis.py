"""Test the analysis module."""
from analysis import (
    parse_data,
    Lab,
    Patient,
)
from fake_files import fake_files
from datetime import datetime


def test_lab_class() -> None:
    """Test the lab class in analysis python."""
    lab = Lab(
        "1",
        "1",
        "METABOLIC: ALBUMIN",
        "4.0",
        "g/dL",
        "2019-01-01 00:00:00.000",
    )
    assert lab is not None
    assert lab.patient_id == "1"
    assert lab.admission_id == "1"
    assert lab.name == "METABOLIC: ALBUMIN"
    assert lab.value == 4.0
    assert lab.units == "g/dL"
    assert lab.dates == datetime(2019, 1, 1)


def test_patient_class() -> None:
    """Test the patient class in analysis python."""
    patient = Patient(
        "1",
        "Male",
        "1993-12-21 17:45:40.547",
        "Asian",
        [
            Lab(
                "1",
                "1",
                "METABOLIC: ALBUMIN",
                "4.0",
                "g/dL",
                "2019-01-01 00:00:00.000",
            ),
        ],
    )
    assert patient is not None
    assert patient.patient_id == "1"
    assert patient.gender == "Male"
    assert patient.dob == datetime(1993, 12, 21, 17, 45, 40, 547000)
    assert patient.race == "Asian"
    assert patient.age == 29
    assert patient.first_admit == 25
    assert patient.lab[0].patient_id == "1"
    assert patient.lab[0].admission_id == "1"
    assert patient.lab[0].name == "METABOLIC: ALBUMIN"
    assert patient.lab[0].value == 4.0
    assert patient.lab[0].units == "g/dL"
    assert patient.lab[0].dates == datetime(2019, 1, 1)


def test_parse_data() -> None:
    """Test the parse_data function in analysis python."""
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
        patient = parse_data(patient_file, lab_file)
        assert patient is not None
        assert patient["1"].patient_id == "1"
        assert patient["1"].gender == "Male"
        assert patient["1"].dob == datetime(1947, 12, 28, 2, 45, 40, 547000)
        assert patient["1"].race == "Unknown"
        assert patient["1"].age == 75
        assert patient["1"].first_admit == 71
        assert patient["1"].is_sick("METABOLIC: ALBUMIN", ">", 4.1) is False
        assert patient["1"].is_sick("METABOLIC: ALBUMIN", "<", 5.0)
        assert patient["1"].is_sick("METABOLIC: ALBUMIN", ">", 3.0)
        assert patient["1"].lab[0].patient_id == "1"
        assert patient["1"].lab[0].admission_id == "1"
        assert patient["1"].lab[0].name == "METABOLIC: ALBUMIN"
        assert patient["1"].lab[0].value == 4.0
        assert patient["1"].lab[0].units == "g/dL"
        assert patient["1"].lab[0].dates == datetime(2019, 1, 1)
