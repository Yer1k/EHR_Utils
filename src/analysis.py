"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

from datetime import datetime
import sqlite3


class Lab:
    """Lab class to store lab information."""

    def __init__(
        self,
        id: str,
        admission_id: str,
        name: str,
        value: str,
        units: str,
        dates: str,
    ):
        """Initialize a lab object."""
        self.id = id
        self.admission_id = admission_id
        self.name = name
        self.value = float(value)
        self.units = units
        self.dates = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S.%f")


class Patient:
    """Patient class to store patient information."""

    def __init__(
        self, id: str, gender: str, dob: str, race: str, labs: list[Lab]
    ):
        """Initialize a patient object."""
        self.id = id
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


def patient_data(patient_filename: str) -> None:
    """Pass patient data to database."""
    conn = sqlite3.connect("patient.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS patient (
            id text PRIMARY KEY,
            gender text,
            dob text,
            race text,
            marital_status text,
            language text,
            PatientPopulationPercentageBelowPoverty float,
            """
    )
    with open(patient_filename, "r", encoding="utf-8-sig") as patient_file:
        next(patient_file)
        for line in patient_file:
            patient_values = line.strip().split("\t")
            c.execute(
                f"""
                INSERT INTO patient VALUES (?, ?, ?, ?, ?, ?, ?)
                [
                    {patient_values[0]},
                    {patient_values[1]},
                    {patient_values[2]},
                    {patient_values[3]},
                    {patient_values[4]},
                    {patient_values[5]},
                    {patient_values[6]},
                ]
                """
            )
    conn.commit()
    patient_file.close()
    conn.close()


def lab_data(lab_filename: str) -> None:
    """Pass lab data to database."""
    conn = sqlite3.connect("lab.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS lab (
            id text,
            admission_id text,
            lab_name text,
            lab_value float,
            lab_units text,
            lab_dates text,
            PRIMARY KEY (id, admission_id)
        """
    )
    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:
        next(lab_file)
        for line in lab_file:
            lab_values = line.strip().split("\t")
            c.execute(
                f"""
                INSERT INTO lab VALUES (?, ?, ?, ?, ?, ?)
                [
                    {lab_values[0]},
                    {lab_values[1]},
                    {lab_values[2]},
                    {lab_values[3]},
                    {lab_values[4]},
                    {lab_values[5]},
                ]
                """
            )
    conn.commit()
    lab_file.close()
    conn.close()


# def parse_data(patient_filename: str, lab_filename: str) -> None:
#     """
#    Read and parse data from patient and lab files to create sqlite databases.

#     Both files are tab-delimited.
#     """
#     conn = sqlite3.connect("patient.db")
#     c = conn.cursor()
#     c.execute(
#         """
#         CREATE TABLE IF NOT EXISTS patient (


# patient_dict = patient_data(patient_filename)  # O(NP*MP)
# lab_dict = lab_data(lab_filename)  # O(NL*ML)
# patient = {}  # O(1)
# lab_list = []  # O(1)
# for patient_id in patient_dict:
#     for lab in lab_dict[patient_id]:
#         lab_obj = Lab(
#             patient_id,
#             lab["AdmissionID"],
#             lab["LabName"],
#             lab["LabValue"],
#             lab["LabUnits"],
#             lab["LabDateTime"],
#         )
#         lab_list.append(lab_obj)
#     patient[patient_id] = Patient(
#         patient_dict[patient_id]["PatientID"],
#         patient_dict[patient_id]["PatientGender"],
#         patient_dict[patient_id]["PatientDateOfBirth"],
#         patient_dict[patient_id]["PatientRace"],
#         lab_list,
#     )  # O(1)
# return patient  # O(1)
