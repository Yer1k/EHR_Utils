"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

import datetime


def parse_data(
    patient_filename: str, lab_filename: str
) -> dict[str, str | list[dict[str, str]]]:
    """Read and parse data from patient and lab files."""
    # (dict[str, str], sict[str, list[str]])
    # PATIENT_DICT = ...
    # LAB_DICT = ...
    # (PATIENT_DICT, LAB_DICT)
    patients = {}
    # read the files and parse the data into a dictionary
    with open(patient_filename, "r", encoding="utf-8-sig") as f:
        column_names = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            patient = {
                column_names[i]: values[i] for i in range(len(column_names))
            }
            patients[patient["PatientID"]] = patient

    labs = {}
    with open(lab_filename, "r", encoding="utf-8-sig") as f:
        column_names = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            lab = {
                column_names[i]: values[i] for i in range(len(column_names))
            }
            patient_id = lab["PatientID"]
            if patient_id not in labs:
                labs[patient_id] = []
            labs[patient_id].append(lab)
            if "labs" not in patients[patient_id]:
                patients[patient_id]["labs"] = []
            patients[patient_id]["labs"].append(lab)

    # convert the dates to datetime objects
    for patient_id in patients:
        patient = patients[patient_id]
        patient["PatientDateOfBirth"] = datetime.datetime.strptime(
            patient["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
        )
        if "labs" in patient:
            for lab in patient["labs"]:
                lab["LabDateTime"] = datetime.datetime.strptime(
                    lab["LabDateTime"], "%Y-%m-%d %H:%M:%S.%f"
                )

    # add the age of the patient to the dictionary
    for patient_id in patients:
        patient = patients[patient_id]
        patient["age"] = int(
            (datetime.datetime.now() - patient["PatientDateOfBirth"]).days
            / 365
        )

    # return the dictionary

    return patients


def patient_age(records: dict, patient_id: str) -> float:
    if patient_id not in records:
        return None
    return records[patient_id]["age"]


def patient_is_sick(
    records: dict, patient_id: str, lab_name: str, operator: str, value: float
) -> bool:
    if patient_id not in records:
        return False
    patient = records[patient_id]
    if "labs" not in patient:
        return False
    for lab in patient["labs"]:
        if lab["LabName"] != lab_name:
            continue
        lab_value = float(lab["LabValue"])
        if operator == ">":
            if lab_value > value:
                return True
        elif operator == "<":
            if lab_value < value:
                return True
    return False


if __name__ == "__main__":
    # Path to the table of patients with demographic data
    patient_filename = "../00_source_data/PatientCorePopulatedTable.txt"
    # Download the data if not, http://people.ee.duke.edu/~pkw3/static/PatientCorePopulatedTable.txt

    # Path to the table of laboratory results
    lab_filename = "../00_source_data/LabsCorePopulatedTable.txt"
    # Download the data if not, http://people.ee.duke.edu/~pkw3/static/LabsCorePopulatedTable.txt
    records = parse_data(patient_filename, lab_filename)

    print(patient_age(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"))

    print(
        patient_is_sick(
            records,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "METABOLIC: ALBUMIN",
            ">",
            4.0,
        )
    )
    # test files exist
"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

from datetime import datetime


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
            patient_dict[patient["PatientID"]] = patient  # O(1)
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
