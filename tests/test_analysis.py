"""Test the analysis module."""
from analysis import (
    parse_data,
    Lab,
    Patient,
)
from fake_files import fake_files
import unittest
from datetime import datetime


class TestLab(unittest.TestCase):
    """Test the Lab class."""

    def setUp(self) -> None:
        """Initialize a Lab object for testing."""
        self.lab = Lab(
            "1", "2", "test", "10.0", "mg/dL", "2023-04-16 10:00:00.000000"
        )

    def test_attributes(self) -> None:
        """Test the attributes of the Lab object."""
        self.assertEqual(self.lab.id, "1")
        self.assertEqual(self.lab.admission_id, "2")
        self.assertEqual(self.lab.name, "test")
        self.assertEqual(self.lab.value, 10.0)
        self.assertEqual(self.lab.units, "mg/dL")
        self.assertEqual(self.lab.dates, datetime(2023, 4, 16, 10, 0))

    def test_value_type(self) -> None:
        """Test the value type of the Lab object."""
        with self.assertRaises(ValueError):
            Lab(
                "1",
                "2",
                "test",
                "invalid_value",
                "mg/dL",
                "2023-04-16 10:00:00.000000",
            )


class TestPatient(unittest.TestCase):
    """Test the Patient class."""

    def setUp(self) -> None:
        """Initialize a Patient object for testing."""
        self.lab1 = Lab(
            "1", "2", "test1", "10.0", "mg/dL", "2022-04-16 10:00:00.000000"
        )
        self.lab2 = Lab(
            "2", "2", "test2", "20.0", "mg/dL", "2023-04-15 09:00:00.000000"
        )
        self.labs = [self.lab1, self.lab2]
        self.patient = Patient(
            "1", "male", "1990-01-01 00:00:00.000000", "white", self.labs
        )

    def test_attributes(self) -> None:
        """Test the attributes of the Patient object."""
        self.assertEqual(self.patient.id, "1")
        self.assertEqual(self.patient.gender, "male")
        self.assertEqual(self.patient.dob, datetime(1990, 1, 1))
        self.assertEqual(self.patient.race, "white")
        self.assertEqual(self.patient.lab, self.labs)

    def test_age(self) -> None:
        """Test the age of the patient."""
        self.assertEqual(self.patient.age, 33)

    def test_first_admit(self) -> None:
        """Test the age of the patient at first admission."""
        self.assertEqual(self.patient.first_admit, 32)

    def test_is_sick(self) -> None:
        """Test if the patient is sick."""
        self.assertTrue(self.patient.is_sick("test1", ">", 5.0))
        self.assertTrue(self.patient.is_sick("test2", "<", 30.0))
        self.assertFalse(self.patient.is_sick("test1", "<", 5.0))
        self.assertFalse(self.patient.is_sick("test2", ">", 30.0))


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
        assert patient["1"].id == "1"
        assert patient["1"].gender == "Male"
        assert patient["1"].dob == datetime(1947, 12, 28, 2, 45, 40, 547000)
        assert patient["1"].race == "Unknown"
        assert patient["1"].lab[0].id == "1"
        assert patient["1"].lab[0].admission_id == "1"
        assert patient["1"].lab[0].name == "METABOLIC: ALBUMIN"
        assert patient["1"].lab[0].value == 4.0
        assert patient["1"].lab[0].units == "g/dL"
        assert patient["1"].lab[0].dates == datetime(2019, 1, 1)
