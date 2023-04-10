# EHR data analysis tools

This ehr-utils application provides some simple analytical capabilities for EHR data.

## Instruction for use (End User)

### Requirements

To use this ehr-utils application, you need to have a working Python 3.6+ environment.

### Installation

Clone the repository:

    git clone git@github.com:biostat821-2023/ehr-utils-Yer1k.git

### Usage

To use the ehr-utils application, you need to import the analysis module:

    import analysis

#### Patient data and lab data tabular files sturcture

The patient data and lab data are stored in two **Tab Delimited** files, either in `.txt` or `.csv` format, such as `patients.txt` and `labs.txt`, respectively.

The `patients.txt` file contains the following columns:

- `PatientID`: a unique identifier for each patient
- `PatientGender`: gender of the patient
- `PatientDateOfBirth`: date of birth of the patient in the format of `YYYY-MM-DD HH:MM:SS.SSS`
- `PatientRace`: race of the patient
- `PatientMaritalStatus`: marital status of the patient
- `PatientLanguage`: language of the patient
- `PatientPopulationPercentageBelowPoverty`: percentage of the population below poverty of the patient's residence

The `labs.txt` file contains the following columns:

- `PatientID`: a unique identifier for each patient
- `AdmissionID`: a unique identifier for each admission
- `LabName`: name of the lab test
- `LabValue`: value of the lab test
- `LabUnits`: units of the lab test
- `LabDateTime`: date and time of the lab test in the format of `YYYY-MM-DD HH:MM:SS.SSS`


Then, you can use the `analysis` module to perform analyses, including parsing the patient and lab data with `parse_data` function, checking patient age with `patient_age` function, and testing whether patient is sick with `patient_is_sick` function. Specifically:

#### Parse data
The function `patient_data(patient_filename: str) -> dict[str, dict[str, str]]` should take the path to the patient data and the path to the lab data and return a dictionary of patient records. For example,

```python
>> records = parse_data("[data]/patients.csv", "[data]/labs.csv")
```

#### Patient age
The function `patient_age(records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]], patient_id: str) -> int` should take the data and return the age of the patient. For example,

```python
>> patient_age(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C")
49
```

#### Sick patients
The function `patient_is_sick(records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]], patient_id: str, lab_name: str, operator: str, value: float,) -> bool` should take the data and return a boolean indicating whether **the patient has ever had a test** with value above (">") or below ("<") the given level. For example,

```python
>> patient_is_sick(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "METABOLIC: ALBUMIN", ">", 4.0)
True
```

## Instruction for contributors


