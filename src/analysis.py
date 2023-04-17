"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

from datetime import datetime


class Lab:
    """Lab class to store lab information."""

    def __init__(
        self,
        patient_id: str,
        admission_id: str,
        name: str,
        value: str,
        units: str,
        dates: str,
    ):
        """Initialize a lab object."""
        self.patient_id = patient_id
        self.admission_id = admission_id
        self.name = name
        self.value = float(value)
        self.units = units
        self.dates = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S.%f")


class Patient:
    """Patient class to store patient information."""

    def __init__(
        self,
        patient_id: str,
        gender: str,
        dob: str,
        race: str,
        labs: list[Lab],
    ):
        """Initialize a patient object."""
        self.patient_id = patient_id
        self.gender = gender
        self.dob = datetime.strptime(dob, "%Y-%m-%d %H:%M:%S.%f")
        self.race = race
        self.lab = labs

    @property
    def age(self) -> int:
        """Calculate the age of the patient."""
        today = datetime.today()
        return (
            today.year
            - self.dob.year
            - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )

    @property
    def first_admit(self) -> int:
        """Calculate the age of the patient at first admission."""
        # sort the lab list by dates
        self.lab.sort(key=lambda x: x.dates)
        return (
            self.lab[0].dates.year
            - self.dob.year
            - (
                (self.lab[0].dates.month, self.lab[0].dates.day)
                < (self.dob.month, self.dob.day)
            )
        )

    def is_sick(self, lab_name: str, operator: str, value: float) -> bool:
        """Check if the patient is sick."""
        for lab in self.lab:
            if (
                (lab.name == lab_name)
                and (operator == ">")
                and (lab.value > value)
            ):  # O(1)
                return True  # O(1)
            elif (
                (lab.name == lab_name)
                and (operator == "<")
                and (lab.value < value)
            ):
                return True  # O(1)
        return False  # O(1)


def patient_data(patient_filename: str) -> dict[str, dict[str, str]]:
    """
    Create a dictionary of patient personal file.

    Time complexity analysis:
    The function will run O(1) time complexity to create dictionary.
    The function will scale according to the number of patients (NP) and
        the number of columns in the patient personal file (MP).
    Thus, the function will scale according to O(NP*MP).
    """
    patient_dict = {}  # O(1)
    with open(
        patient_filename, "r", encoding="utf-8-sig"
    ) as patient_file:  # O(1)
        patient_column_names = (
            patient_file.readline().strip().split("\t")
        )  # O(MP)
        for line in patient_file:  # O(NP)
            patient_values = line.strip().split("\t")  # O(MP)
            patient = {
                patient_column_names[i]: patient_values[i]
                for i in range(len(patient_column_names))
            }  # O(1) to create the dictionary,
            # but then scale to O(MP), number of columns
            patient_id = patient["PatientID"]  # O(1)
            patient_dict[patient_id] = patient  # O(1)
    return patient_dict  # O(1)


def lab_data(lab_filename: str) -> dict[str, list[dict[str, str]]]:
    """
    Create a dictionary of lab results.

    Time complexity analysis:
    The function will run O(1) time complexity to create dictionary.
    The function will scale according to the number of rows in the
    lab results (NL) and the number of columns in the lab results file (ML).
    Thus, the function will scale according to O(NL*ML).
    """
    lab_dict: dict[str, list[dict[str, str]]] = {}  # O(1)
    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:  # O(1)
        lab_column_names = lab_file.readline().strip().split("\t")  # O(ML)
        for line in lab_file:  # O(NL)
            lab_values = line.strip().split("\t")  # O(ML)
            lab = {
                lab_column_names[i]: lab_values[i]
                for i in range(len(lab_column_names))
            }  # O(1) to create the dictionary,
            # but then scale to O(ML), number of columns
            patient_id = lab["PatientID"]  # O(1)
            if patient_id not in lab_dict:  # O(1)
                lab_dict[patient_id] = []  # O(1)
            lab_dict[patient_id].append(lab)  # O(1)
    return lab_dict  # O(1)


def parse_data(patient_filename: str, lab_filename: str) -> dict[str, Patient]:
    """
    Read and parse data from patient and lab files to create patient objects.

    Patient objects are stored in a dictionary with patient ID as the key.
    """
    patient_dict = patient_data(patient_filename)  # O(NP*MP)
    lab_dict = lab_data(lab_filename)  # O(NL*ML)
    patient = {}  # O(1)
    lab_list = []  # O(1)
    for patient_id in patient_dict:
        for lab in lab_dict[patient_id]:
            lab_obj = Lab(
                patient_id,
                lab["AdmissionID"],
                lab["LabName"],
                lab["LabValue"],
                lab["LabUnits"],
                lab["LabDateTime"],
            )
            lab_list.append(lab_obj)
        patient[patient_id] = Patient(
            patient_dict[patient_id]["PatientID"],
            patient_dict[patient_id]["PatientGender"],
            patient_dict[patient_id]["PatientDateOfBirth"],
            patient_dict[patient_id]["PatientRace"],
            lab_list,
        )  # O(1)
    return patient  # O(1)
