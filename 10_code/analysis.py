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
            }  # O(1)
            patient_dict[patient["PatientID"]] = patient  # O(1)
    return patient_dict  # O(1)


def lab_data(lab_filename: str) -> dict[str, list[dict[str, str]]]:
    """
    Create a dictionary of lab results.

    Time complexity analysis:
    The function will run O(1) time complexity to create dictionary.
    The function will scale according to the number of patients (NP) and
        the number of columns in the lab results file (ML).
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
            }  # O(1)
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
    """
    return patient_data(patient_filename), lab_data(lab_filename)  # O(1)


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
    The function will run O(1) time complexity to check if the patient_id is on
        the dictionary of lab results.
    The function will scale according to the loop of the lab results (NL).
    Thus, the function will scale according to O(NL).
    """
    if patient_id in records[1]:  # O(1)
        for lab in records[1][patient_id]:  # O(NL)
            if lab["LabName"] == lab_name:  # O(1)
                if operator == ">":  # O(1)
                    if float(lab["LabValue"]) > value:  # O(1)
                        return True  # O(1)
                elif operator == "<":  # O(1)
                    if float(lab["LabValue"]) < value:  # O(1)
                        return True  # O(1)
                elif operator == "=":  # O(1)
                    if float(lab["LabValue"]) == value:  # O(1)
                        return True  # O(1)
    return False  # O(1)



if __name__ == "__main__":
    """Test the functions in this module."""
    # Path to the table of patients with demographic data
    patient_filename = "../00_source_data/PatientCorePopulatedTable.txt"

    # Path to the table of laboratory results
    lab_filename = "../00_source_data/LabsCorePopulatedTable.txt"

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

