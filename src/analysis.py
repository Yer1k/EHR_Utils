"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

from datetime import datetime


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


def lab_data(
    lab_filename: str, patient_id: str
) -> dict[str, list[dict[str, str]]]:
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


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """
    Read and parse data from patient and lab files.

    Time complexity analysis:
    The function will run O(1) time complexity to call two functions.
    The function will scale according to the number of patients (NP) and
        the number of columns in the patient personal file (MP).
    In addition, the function will scale according to the number of rows
        in the lab results (NL) and the number of columns in the lab results
        file (ML).
    To sum up, the time complexity will be O(NP*MP + NL*ML).
    """
    patient_dict = patient_data(patient_filename)  # O(NP*MP)
    # patient = {}  # O(1)
    # patient["PatientID"] = patient_dict[patient["PatientID"]]  # O(1)

    # patient = Patient(
    #     patient_dict["PatientID"],
    #     patient_dict["PatientGender"],
    #     patient_dict["PatientDOB"],
    #     patient_dict["PatientRace"],
    #     lab_dict["PatientID"],
    # )
    # patient_dict = {
    #     id: patient_object(),
    # }  # O(1)
    # with open(
    #     patient_filename, "r", encoding="utf-8-sig"
    # ) as patient_file:  # O(1)
    #     patient_column_names = (
    #         patient_file.readline().strip().split("\t")
    #     )  # O(MP)
    #     for line in patient_file:  # O(NP)
    #         patient_values = line.strip().split("\t")  # O(MP)
    #         patient = {
    #             patient_column_names[i]: patient_values[i]
    #             for i in range(len(patient_column_names))
    #         }  # O(1) to create the dictionary,
    #         # but then scale to O(MP), number of columns
    #         patient_dict[patient["PatientID"]] = Patient(
    #             patient["PatientID"],
    #             patient["PatientGender"],
    #             patient["PatientDateOfBirth"],
    #             patient["PatientRace"],
    #         )  # O(1)

    return patient_data(patient_filename), lab_data(lab_filename)
    # O(NP*MP + NL*ML)


def patient_age(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
) -> int:
    """
    Return the age of the patient.

    Time complexity analysis:
    The function will run O(1) time complexity to calculate the age.
    Overall, the function will not scale, istead it will run O(1).
    """
    patient = records[0][patient_id]  # O(1)
    birth_date = datetime.strptime(
        patient["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
    )  # O(1)
    day_now = datetime.now()  # O(1)
    patient_age = int((day_now - birth_date).days / 365)  # O(1)
    return patient_age  # O(1)


def patient_is_sick(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """
    Return True if the patient is sick, False otherwise.

    Time complexity analysis:
    The function will run O(1) time complexity to check if the patient_id
        is on the dictionary of lab results.
    The function will scale according to the loop of the lab results (NL),
        if for a patient have multiple lab results, it will scale to O(MNL),
        this may be implement in the future.
    Thus, the function will scale according to O(MNL).
    """
    if patient_id in records[1]:  # O(1)
        for lab in records[1][patient_id]:  # O(NL)
            if (
                (lab["LabName"] == lab_name)
                and (operator == ">")
                and (float(lab["LabValue"]) > value)
            ):  # O(1)
                return True  # O(1)
            elif (
                (lab["LabName"] == lab_name)
                and (operator == "<")
                and (float(lab["LabValue"]) < value)
            ):
                return True  # O(1)
    return False  # O(1)


def age_at_first_admit(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
) -> int:
    """
    Return the age of the patient at the first admission.

    If results are not available, return -1 instead.
    Time complexity analysis:
    The function will run O(1) time complexity to check if the patient_id
        is on the dictionary of lab results.
    The function will scale according to the loop of the lab results (NL),
        if for a patient have multiple lab results, it will scale to O(NLlogNL)
        to sort the list of lab results by LabDateTime.
    Thus, the function will scale according to O(NLlogNL).
    """
    if patient_id in records[1]:  # O(1)
        for lab in records[1][patient_id]:  # O(NL)
            if lab["AdmissionID"] == "1":  # O(1)
                # sort the list of lab results by LabDateTime
                sorted_lab = sorted(
                    records[1][patient_id], key=lambda t: t["LabDateTime"]
                )  # O(NLlogNL)
                birth_date = datetime.strptime(
                    records[0][patient_id]["PatientDateOfBirth"],
                    "%Y-%m-%d %H:%M:%S.%f",
                )  # O(1)
                first_admit_date = datetime.strptime(
                    sorted_lab[0]["LabDateTime"], "%Y-%m-%d %H:%M:%S.%f"
                )  # O(1)
                patient_age = int(
                    (first_admit_date - birth_date).days / 365
                )  # O(1)
                return patient_age  # O(1)
    return -1  # O(1)
