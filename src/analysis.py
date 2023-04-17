"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

from datetime import datetime
import sqlite3


class Lab:
    """Lab class to read lab data from sqlite database."""

    def __init__(
        self,
        patient_id: str,
        connection: sqlite3.Connection,
        # like define connection here?
        #     # admission_id: str,
        #     # name: str,
        #     # value: str,
        #     # units: str,
        #     # dates: str,
    ):
        """Initialize a lab object."""
        self.patient_id = patient_id

    @property
    def adimission_id(self):
        """Get admission id from sqlite."""
        admission_id = c.execute(
            f"SELECT admission_id FROM lab WHERE patient_id = {self.patient_id}"
        ).fetchall()
        return admission_id

    @property
    def lab_name(self):
        """Get lab name from sqlite."""
        self.name = c.execute(
            f"SELECT lab_name FROM lab WHERE patient_id = {self.patient_id}"
        ).fetchall()

    @property
    def lab_value(self):
        """Get lab value from sqlite."""
        self.value = c.execute(
            f"SELECT lab_value FROM lab WHERE patient_id = {self.patient_id}"
        ).fetchall()

    #     # self.admission_id = admission_id
    #     # self.name = name
    #     # self.value = float(value)
    #     # self.units = units
    #     # self.dates = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S.%f")


class Patient:
    """Patient class to store patient information."""

    def __init__(
        self,
        patient_id: str,
        # gender: str,
        # dob: str,
        # race: str,
        # labs: list[Lab],
    ):
        """Initialize a patient object."""
        self.patient_id = patient_id
        # self.gender = gender
        # self.dob = datetime.strptime(dob, "%Y-%m-%d %H:%M:%S.%f")
        # self.race = race
        # self.lab = labs

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
        min_lab_date = min(self.lab, key=lambda x: x.dates).dates
        return (
            min_lab_date.year
            - self.dob.year
            - (
                (min_lab_date.month, min_lab_date.day)
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


def patient_data(
    patient_filename: str, db_connection: sqlite3.Connection
) -> None:
    """Pass patient data to database."""
    conn = db_connection
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS patient (
            patient_id text PRIMARY KEY,
            gender text,
            dob text,
            race text,
            """
    )
    with open(patient_filename, "r", encoding="utf-8-sig") as patient_file:
        patient_column_names = patient_file.readline().strip().split("\t")
        for line in patient_file:
            patient_values = line.strip().split("\t")
            patient = {
                patient_column_names[i]: patient_values[i]
                for i in range(len(patient_column_names))
            }
            c.execute(
                f"""
                INSERT INTO patient VALUES (?, ?, ?, ?)
                [
                    {patient["PatientID"]},
                    {patient["PatientGender"]},
                    {patient["PatientDateOfBirth"]},
                    {patient["PatientRace"]},
                ]
                """
            )
    conn.commit()
    patient_file.close()
    conn.close()


def lab_data(lab_filename: str, db_connection: sqlite3.Connection) -> None:
    """Pass lab data to database."""
    conn = db_connection
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS lab (
            patient_id text,
            admission_id text,
            lab_name text,
            lab_value float,
            lab_units text,
            lab_dates text,
            PRIMARY KEY (patient_id, admission_id, lab_name),
        """
    )
    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:
        lab_column_names = lab_file.readline().strip().split("\t")
        for line in lab_file:
            lab_values = line.strip().split("\t")
            lab = {
                lab_column_names[i]: lab_values[i]
                for i in range(len(lab_column_names))
            }
            c.execute(
                f"""
                INSERT INTO lab VALUES (?, ?, ?, ?, ?, ?)
                [
                    {lab["PatientID"]},
                    {lab["AdmissionID"]},
                    {lab["LabName"]},
                    {lab["LabValue"]},
                    {lab["LabUnits"]},
                    {lab["LabDateTimes"]},
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
