"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

from datetime import datetime


def patient_data(patient_filename: str) -> dict[str, dict[str, str]]:
    """Create a dictionary of patient personal file."""
    patient_dict = {}
    with open(patient_filename, "r", encoding="utf-8-sig") as patient_file:
        patient_column_names = patient_file.readline().strip().split("\t")
        for line in patient_file:
            patient_values = line.strip().split("\t")
            patient = {
                patient_column_names[i]: patient_values[i]
                for i in range(len(patient_column_names))
            }
            patient_dict[patient["PatientID"]] = patient
    return patient_dict


def lab_data(lab_filename: str) -> dict[str, list[dict[str, str]]]:
    """Create a dictionary of lab results."""
    lab_dict: dict[str, list[dict[str, str]]] = {}
    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:
        lab_column_names = lab_file.readline().strip().split("\t")
        for line in lab_file:
            lab_values = line.strip().split("\t")
            lab = {
                lab_column_names[i]: lab_values[i]
                for i in range(len(lab_column_names))
            }
            patient_id = lab["PatientID"]
            if patient_id not in lab_dict:
                lab_dict[patient_id] = []
            lab_dict[patient_id].append(lab)
    return lab_dict


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """Read and parse data from patient and lab files."""
    return patient_data(patient_filename), lab_data(lab_filename)


def patient_age(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
) -> int:
    """Return the age of the patient."""
    patient = records[0][patient_id]
    birth_date = datetime.strptime(
        patient["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
    )
    day_now = datetime.now()
    patient_age = int((day_now - birth_date).days / 365)
    return patient_age


def patient_is_sick(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return True if the patient is sick, False otherwise."""
    if patient_id in records[1]:
        for lab in records[1][patient_id]:
            if lab["LabName"] == lab_name:
                if operator == ">":
                    if float(lab["LabValue"]) > value:
                        return True
                elif operator == "<":
                    if float(lab["LabValue"]) < value:
                        return True
                elif operator == "=":
                    if float(lab["LabValue"]) == value:
                        return True
    return False


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
    # test files exist
