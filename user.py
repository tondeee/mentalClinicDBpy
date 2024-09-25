from datetime import date
from enum import Enum


class MentalHealthIssue(Enum):
    DEPRESSION = "Depression"
    ANXIETY = "Anxiety"
    BIPOLAR = "Bipolar Disorder"
    SCHIZOPHRENIA = "Schizophrenia"
    PTSD = "Post-Traumatic Stress Disorder"
    OCD = "Obsessive-Compulsive Disorder"


class Appointment:
    _counter = 0

    def __init__(self, date, time, psychiatrist, patient):
        self.date = date
        self.time = time
        self.psychiatrist = psychiatrist
        self.patient = patient
        self._id = Appointment._counter
        Appointment._counter += 1

    def __str__(self):
        return f"Appointment #{self._id} with Dr. {self.psychiatrist.last_name} at {self.time} on {self.date}"

    @staticmethod
    def get_appointment_count():
        return Appointment._counter


class User:
    def __init__(self, first_name, last_name, username, email, password, birth_date, id):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self._password = password
        self.birth_date = birth_date
        self.id = id
        self.appointments = []

    def login(self, username, password):
        return username == self.username and password == self._password

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )


class Psychiatrist(User):
    def __init__(self, first_name, last_name, username, email, password, birth_date, specialization, id):
        super().__init__(first_name, last_name, username, email, password, birth_date, id)
        self.specialization = specialization

        self._patients = set()

    def __str__(self):
        return f"Dr. {self.last_name} - {self.specialization}"

    def add_patient(self, patient):
        self._patients.add(patient)

    def get_patient_count(self):
        return len(self._patients)


class Patient(User):
    def __init__(self, first_name, last_name, username, email, password, birth_date, id):
        super().__init__(first_name, last_name, username, email, password, birth_date, id)
        self.diagnoses = []
        self._medical_history = ""

    def add_diagnosis(self, issue: MentalHealthIssue):
        if issue not in self.diagnoses:
            self.diagnoses.append(issue)

    def remove_diagnosis(self, issue: MentalHealthIssue):
        if issue in self.diagnoses:
            self.diagnoses.remove(issue)

    def update_medical_history(self, new_info):
        self._medical_history += f"\n{date.today()}: {new_info}"

    def __str__(self):
        return f"{super().__str__()}"


# Demonstration
if __name__ == "__main__":
    psychiatrist = Psychiatrist("John", "Doe", "johndoe", "john@clinic.com", "password123",
                                date(1975, 5, 15), "Clinical Psychiatrist",  1)

    patient = Patient("Jane", "Smith", "janesmith", "jane@email.com", "pass456",
                      date(1990, 8, 20), 2)

    print(psychiatrist)
    print(patient)

    patient.add_diagnosis(MentalHealthIssue.ANXIETY)
    patient.add_diagnosis(MentalHealthIssue.DEPRESSION)
    psychiatrist.add_patient(patient)

    users = [psychiatrist, patient]
    for user in users:
        print(f"{user} - Age: {user.get_age()}")

    appointment = Appointment(date(2024, 10, 5), "14:00", psychiatrist, patient)
    psychiatrist.add_appointment(appointment)
    patient.add_appointment(appointment)

    print(f"\nCreated appointment: {appointment}")
    print(f"Total appointments: {Appointment.get_appointment_count()}")

    print(f"\nPatient's diagnoses: {', '.join([issue.value for issue in patient.diagnoses])}")
    patient.remove_diagnosis(MentalHealthIssue.ANXIETY)
    print(f"Updated patient's diagnoses: {', '.join([issue.value for issue in patient.diagnoses])}")

    patient.update_medical_history("Initial consultation completed. Prescribed antidepressants.")
    print(f"\nPsychiatrist's patient count: {psychiatrist.get_patient_count()}")
