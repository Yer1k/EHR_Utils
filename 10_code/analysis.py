"""A module reading and parsing data from patient and lab files.

This module is desigened to be generalizable to other data files.
See readme.md for more information, including assumptions, limitations, etc.
"""

from datetime import datetime
from typing import Dict, Any

# VarType = Union[
#     SupportsIndex, slice, str, datetime, Dict[str, str], Dict[str, List[str]]
# ]

VarType = Dict[Any, Any]


def parse_data(patient_filename: str, lab_filename: str) -> VarType:
    """Read and parse data from patient and lab files."""
    # (dict[str, str], dict[str, list[str]])
    # PATIENT_DICT = ...
    # LAB_DICT = ...
    # (PATIENT_DICT, LAB_DICT)

    patients = {}
    labs: VarType = {}

    # read the patient and parse the data into a dictionary
    with open(patient_filename, "r", encoding="utf-8-sig") as f:
        column_names = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            patient = {
                column_names[i]: values[i] for i in range(len(column_names))
            }
            patients[patient["PatientID"]] = patient

    # read the lab file and parse the data into the dictionary
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
        patient["PatientDateOfBirth"] = datetime.strptime(
            patient["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
        )
        if "labs" in patient:
            for lab in patient["labs"]:
                lab["LabDateTime"] = datetime.strptime(
                    lab["LabDateTime"], "%Y-%m-%d %H:%M:%S.%f"
                )

    # add the age of the patient to the dictionary
    for patient_id in patients:
        patient = patients[patient_id]
        patient["age"] = int(
            (datetime.now() - patient["PatientDateOfBirth"]).days / 365
        )

    # return the dictionary

    return patients


def patient_age(records: VarType, patient_id: str) -> float | None:
    """Return the age of the patient."""
    if patient_id not in records:
        return None
    return records[patient_id]["age"]


def patient_is_sick(
    records: VarType,
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return True if the patient is sick, False otherwise."""
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
    # Download the data if not,
    # http://people.ee.duke.edu/~pkw3/static/PatientCorePopulatedTable.txt

    # Path to the table of laboratory results
    lab_filename = "../00_source_data/LabsCorePopulatedTable.txt"
    # Download the data if not,
    # http://people.ee.duke.edu/~pkw3/static/LabsCorePopulatedTable.txt

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
