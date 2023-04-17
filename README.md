# EHR data analysis tools

This ehr-utils application provides some simple analytical capabilities for EHR data.

## Instruction for use (End User)

### Requirements

To use this ehr-utils application, you need to have a working Python 3.10.8+ environment.

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
- [Optional]`PatientLanguage`: language of the patient
- [Optional]`PatientPopulationPercentageBelowPoverty`: percentage of the population below poverty of the patient's residence

The `labs.txt` file contains the following columns:

- `PatientID`: a unique identifier for each patient
- `AdmissionID`: a unique identifier for each admission
- `LabName`: name of the lab test
- `LabValue`: value of the lab test
- `LabUnits`: units of the lab test
- `LabDateTime`: date and time of the lab test in the format of `YYYY-MM-DD HH:MM:SS.SSS`


Then, you can use the `analysis` module to perform analyses, including parsing the patient and lab data with `parse_data` function which returns a dictionary of `Patient` objects, calculating the age of the patient with property `age` of `Patient` object, checking whether the patient is sick with `is_sick` method of `Patient` object, and calculating the age of the patient when their earliest lab was recorded with `first_admit` method of `Patient` object.


#### Parse data
The function `patient_data(patient_filename: str) -> dict[str, Patient]` should take the path to the patient data and the path to the lab data and return a dictionary of `Patient` objects. For example,

```python
>> patient_records = parse_data("[data]/patients.txt", "[data]/labs.txt")
```

#### Patient age property
The property `age` of `Patient` object should take the data and return the age of the patient. For example,

```python
>> patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].age
49
```

#### First admission age property
The property `first_admit` of `Patient` object should take the data and return the age of the patient when their earliest lab was recorded. For example,

```python
>> patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].first_admit
18
```

#### Sick patient check
The method `is_sick` of `Patient` object should take the data and return whether the patient is sick. For example,

```python
>> patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].is_sick( "METABOLIC: ALBUMIN", ">", 4.0)
True
```


## Instruction for contributors

For generalization purpose, the ehr-utils application is designed to be used by both end users and developers. The end users can use the ehr-utils application to perform simple analyses on EHR data. The developers can use the ehr-utils application as a template to develop their own EHR data analysis tools.

### Development requirements
**Pull requests are welcome.**

For major changes, please open an issue first to discuss what you would like to change. 

**Before submitting a pull request, please make sure that your code passes all the tests.**

Please make sure to update tests as appropriate. To contribute to this project, you need to have a working Python 3.10.8+ environment, and all source code should be formatted with `black`, `mypy`, `pycodestyle`, and `pydocstyle`. 

You may view the specifics of the checks in this repository's workflow specification: `.github/workflows`

### Tests
For testing, you would need the `pytest` package. To run the tests, you can use the following command:
```bash
    pytest filename.py
```

**To see coverage report**, you can use the `coverage` package. To run the coverage report, you can use the following command:
```bash
    coverage run -m pytest filename.py > test_report.txt
    coverage report --show-missing
```

For example:

![image](https://user-images.githubusercontent.com/81750079/230937155-ddac79dd-4402-4895-87ae-598be8f3d6d9.png)

You may need **at least 70% coverage** to pass the tests; however, if the coverage is not 100%, **please make sure to explain why in the pull request**.
