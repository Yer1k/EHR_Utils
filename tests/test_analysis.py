"""Test the analysis module."""
from analysis import (
    parse_data,
    Lab,
    Patient,
)
from fake_files import fake_files
from datetime import datetime


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
            [
                "1",
                "2",
                "METABOLIC: ALBUMIN",
                "4.7",
                "g/dL",
                "2020-01-01 00:00:00.000",
            ],
            [
                "1",
                "2",
                "URINALYSIS: RED BLOOD CELLS",
                "1.8",
                "rbc/hpf",
                "2020-02-01 00:00:00.000",
            ],
        ],
    ) as (patient_file, lab_file):
        assert parse_data(patient_file, lab_file) == "patient.db created"
        assert Patient("1").patient_id == "1"
        assert Patient("1").gender == "Male"
        assert Patient("1").dob == datetime(1947, 12, 28, 2, 45, 40, 547000)
        assert Patient("1").race == "Unknown"
        assert Patient("1").age == 75
        assert Patient("1").first_admit == 71
        assert not Patient("1").is_sick("METABOLIC: ALBUMIN", ">", 4.8)
        assert Patient("1").is_sick("URINALYSIS: RED BLOOD CELLS", "<", 2.0)
        assert not Patient("1").is_sick("METABOLIC: ALBUMIN", "=", 4.0)
        assert Patient("1").is_sick("METABOLIC: ALBUMIN", "<", 5.0)
        assert Patient("1").is_sick("METABOLIC: ALBUMIN", ">", 3.0)
        assert Lab("1").lab_id == "1"
        assert Lab("1").admission_id == "1"
        assert Lab("1").lab_name == "METABOLIC: ALBUMIN"
        assert Lab("1").lab_value == 4.0
        assert Lab("1").lab_units == "g/dL"
        assert Lab("1").lab_date == datetime(2019, 1, 1, 0, 0)
