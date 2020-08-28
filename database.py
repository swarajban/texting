from dataclasses import dataclass


@dataclass
class Patient:
    name: str
    drug_name: str


_numbers_to_patients = {
    '+14056736773': Patient(name='Swa', drug_name='Brilinta')
}


def look_up_patient_from_number(number: str) -> Patient:
    if number in _numbers_to_patients:
        return _numbers_to_patients[number]
    else:
        return Patient(name='Unknown name', drug_name='Unknown drug')
