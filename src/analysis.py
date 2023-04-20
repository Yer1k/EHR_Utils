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
        patient_id: str,
    ):
        """Initialize a lab object."""
        self.patient_id = patient_id
        self.conn = sqlite3.connect("patient.db")
        self.c = self.conn.cursor()

    @property
    def admission_id(self) -> None:
        """Get admission id from lab table."""
        self.c.execute(
            "SELECT admission_id FROM Lab WHERE patient_id = ?",
            (self.patient_id,),
        )
        self.c.fetchall()

    @property
    def lab_name(self) -> None:
        """Get lab name from lab table."""
        self.c.execute(
            f"SELECT lab_name FROM Lab WHERE patient_id = {self.patient_id}"
        )
        self.c.fetchall()

    @property
    def lab_value(self) -> float:
        """Get lab value from lab table."""
        self.c.execute(
            f"SELECT lab_value FROM Lab WHERE patient_id = {self.patient_id}"
        )
        lab_value = self.c.fetchall()
        return float(lab_value[0])

    @property
    def lab_units(self) -> None:
        """Get lab units from lab table."""
        self.c.execute(
            f"SELECT lab_units FROM Lab WHERE patient_id = {self.patient_id}"
        )
        self.c.fetchall()

    @property
    def lab_dates(self) -> None:
        """Get lab dates from lab table."""
        self.c.execute(
            f"SELECT lab_dates FROM Lab WHERE patient_id = {self.patient_id}"
        )
        self.c.fetchall()

    def is_sick(self, lab_name: str, operator: str, value: float) -> bool:
        """Check if the patient is sick."""
        if (
            (self.lab_name == lab_name)
            and (operator == ">")
            and (self.lab_value > value)
        ):
            return True
        elif (
            (self.lab_name == lab_name)
            and (operator == "<")
            and (self.lab_value < value)
        ):
            return True
        return False


class Patient:
    """Patient class to store patient information."""

    def __init__(
        self,
        patient_id: str,
    ):
        """Initialize a patient object."""
        self.patient_id = patient_id
        self.conn = sqlite3.connect("patient.db")
        self.c = self.conn.cursor()

    @property
    def gender(self) -> None:
        """Get Patient Gender from Patient table."""
        self.c.execute(
            f"SELECT gender FROM Patient WHERE patient_id = {self.patient_id}"
        )
        self.c.fetchall()
        # return

    @property
    def dob(self) -> datetime:
        """Get Patient DOB from Patient table."""
        self.c.execute(
            f"SELECT dob FROM Patient WHERE patient_id = {self.patient_id}"
        )
        dob = datetime.strptime(self.c.fetchall()[0], "%Y-%m-%d-%H.%M.%S.%f")
        return dob

    @property
    def race(self) -> None:
        """Get Patient Race from Patient table."""
        self.c.execute(
            f"SELECT race FROM Patient WHERE patient_id = {self.patient_id}"
        )
        self.c.fetchall()

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
        self.c.execute(
            f"SELECT MIN(Dates) FROM Lab WHERE patient_id = {self.patient_id}"
        )
        min_lab_date = datetime.strptime(
            self.c.fetchall()[0], "%Y-%m-%d-%H.%M.%S.%f"
        )
        return (
            min_lab_date.year
            - self.dob.year
            - (
                (min_lab_date.month, min_lab_date.day)
                < (self.dob.month, self.dob.day)
            )
        )


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


def parse_data(patient_filename: str, lab_filename: str) -> str:
    """
    Read and parse data from patient and lab files to create patient objects.

    Patient objects are stored in a dictionary with patient ID as the key.
    """
    conn = sqlite3.connect("patient.db")
    c = conn.cursor()
    patient_dict = patient_data(patient_filename)
    lab_dict = lab_data(lab_filename)
    c.execute("DROP TABLE IF EXISTS patient")
    c.execute("DROP TABLE IF EXISTS lab")
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS patient (
            patient_id TEXT,
            gender TEXT,
            dob TEXT,
            race TEXT)
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS lab (
            patient_id TEXT,
            admission_id TEXT,
            lab_name TEXT,
            lab_value REAL,
            lab_units TEXT,
            lab_date TEXT)
        """
    )
    for patient_id in patient_dict:
        c.execute(
            """
            INSERT INTO patient VALUES (?, ?, ?, ?)
            """,
            (
                patient_dict[patient_id]["PatientID"],
                patient_dict[patient_id]["PatientGender"],
                patient_dict[patient_id]["PatientDateOfBirth"],
                patient_dict[patient_id]["PatientRace"],
            ),
        )
        for lab in lab_dict[patient_id]:
            c.execute(
                """
                INSERT INTO lab VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    lab["PatientID"],
                    lab["AdmissionID"],
                    lab["LabName"],
                    lab["LabValue"],
                    lab["LabUnits"],
                    lab["LabDateTime"],
                ),
            )
    conn.commit()
    conn.close()

    return "patient.db created"
