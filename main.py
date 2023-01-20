from enum import Enum
import tkinter
import tkinter.messagebox as messagebox


class Probability(Enum):
    LOW = 0.2
    MODERATE_LOW = 0.4
    MODERATE = 0.6
    MODERATE_HIGH = 0.8
    HIGH = 1.0

    @staticmethod
    def determine_probability(probability_value: float):
        if probability_value <= Probability.LOW.value:
            return Probability.LOW
        elif probability_value <= Probability.MODERATE_LOW.value:
            return Probability.MODERATE_LOW
        elif probability_value <= Probability.MODERATE.value:
            return Probability.MODERATE
        elif probability_value <= Probability.MODERATE_HIGH.value:
            return Probability.MODERATE_HIGH
        else:
            return Probability.HIGH


class Disease(Enum):
    NONE = "none"
    COLD = "cold"
    HEART_PROBLEM = "heart problem"
    LIVER_PROBLEM = "liver problem"
    DEATH = "death"
    OTHER_DISEASE = "other disease"


class TemperatureThreshold(Enum):
    BASE = 36.5
    NORMAL = 0.5
    ABNORMAL = 2.5
    CRITICAL = 5.5
    DEADLY = 100.0

    @staticmethod
    def determine_temperature_threshold(temperature: float):
        if 36.0 <= temperature <= 37.0:
            return TemperatureThreshold.NORMAL
        elif 34.0 <= temperature <= 39.0:
            return TemperatureThreshold.ABNORMAL
        elif 31.0 <= temperature <= 42.0:
            return TemperatureThreshold.CRITICAL
        else:
            return TemperatureThreshold.DEADLY


class Patient:
    def __init__(self, age: int, temperature: float, blood_pressure: int, cas: bool, bpm: int):
        self.__age = age
        self.__temperature = temperature
        self.__blood_pressure = blood_pressure
        self.__cas = cas  # cas -> coughing and sneezing
        self.__bpm = bpm  # bpm -> beers per month

    @property
    def age(self):
        return self.__age

    @property
    def temperature(self):
        return self.__temperature

    @property
    def blood_pressure(self):
        return self.__blood_pressure

    @property
    def cas(self):
        return self.__cas

    @property
    def bpm(self):
        return self.__bpm

# class DiseaseDeterminant:
#     @staticmethod
#     def determine_cold_probability(patient: Patient) -> float:
#         temperature_threshold = TemperatureThreshold.determine_temperature_threshold(patient.temperature)
#         if temperature_threshold == TemperatureThreshold.DEADLY:
#             probability = 0.0
#         else:
#             cold_temperature = TemperatureThreshold.CRITICAL.value - TemperatureThreshold.ABNORMAL.value
#             if temperature_threshold == TemperatureThreshold.CRITICAL:
#                 if patient.temperature < TemperatureThreshold.BASE.value:
#                     probability = (patient.temperature - (TemperatureThreshold.BASE.value - TemperatureThreshold.CRITICAL.value)) / cold_temperature
#                 else:
#                     probability = 1.0 - ((patient.temperature - (TemperatureThreshold.BASE.value + TemperatureThreshold.ABNORMAL.value)) / cold_temperature)
#             else:
#                 absolute_temperature = abs(TemperatureThreshold.BASE.value - patient.temperature)
#                 probability = absolute_temperature / cold_temperature
#         if temperature_threshold != TemperatureThreshold.DEADLY and patient.cas:
#             probability = probability + 0.1
#         return min(probability, 1)
#
#     @staticmethod
#     def determine_heart_problem_probability(patient: Patient) -> float:
#         return 0.0
#
#     @staticmethod
#     def determine_liver_problem_probability(patient: Patient) -> float:
#         return 0.0
#
#     @staticmethod
#     def determine_death_probability(patient: Patient) -> float:
#         return 0.0
#
#     @staticmethod
#     def determine_other_disease_probability(patient: Patient) -> float:
#         return 0.0


class DiseaseDeterminant:
    def __init__(self, patient: Patient):
        self.__patient = patient

    def determine_cold_probability(self):
        base_temperature = 36.5
        temperature = self.__patient.temperature
        probability = 0.0
        att = 2.5  # att -> abnormal temperature threshold
        ctt = 5.5  # ctt -> critical temperature threshold
        if base_temperature - att <= temperature <= base_temperature + att:
            absolute_temperature = abs(base_temperature - temperature)
            probability = absolute_temperature / att
        elif base_temperature - ctt <= temperature <= base_temperature + ctt:
            if temperature < base_temperature:
                relative_temperature = temperature - (base_temperature - ctt)
                probability = relative_temperature / (ctt - att)
            else:
                relative_temperature = temperature - (base_temperature + att)
                probability = 1.0 - (relative_temperature / (ctt - att))
        else:
            probability = 0.0

        if self.__patient.cas:
            probability = probability + 0.1
        if self.__patient.age <= 12:
            probability = probability * 1.1
        return min(probability, 1.0)


class PatientApplication:
    def __init__(self):
        self.__root = tkinter.Tk()
        self.__root.title("app")

        self.__age_label = tkinter.Label(self.__root, text="age:")
        self.__age_label.grid(row=0, column=0, columnspan=2)
        self.__age_entry = tkinter.Entry(self.__root)
        self.__age_entry.grid(row=0, column=2, columnspan=3)

        self.__temperature_label = tkinter.Label(self.__root, text="temperature:")
        self.__temperature_label.grid(row=1, column=0, columnspan=2)
        self.__temperature_entry = tkinter.Entry(self.__root)
        self.__temperature_entry.grid(row=1, column=2, columnspan=3)

        self.__cas_label = tkinter.Label(self.__root, text="cas:")
        self.__cas_label.grid(row=2, column=0, columnspan=2)
        self.__cas_entry = tkinter.Entry(self.__root)
        self.__cas_entry.grid(row=2, column=2, columnspan=3)

        self.__info_button = tkinter.Button(self.__root, text="info")
        self.__info_button.grid(row=3, column=0, columnspan=2)
        self.__info_button["command"] = PatientApplication.__show_info
        self.__determine_disease_button = tkinter.Button(self.__root, text="determine disease")
        self.__determine_disease_button.grid(row=3, column=2, columnspan=3)

    @staticmethod
    def __show_info():
        messagebox.showinfo("info", "expert system by Maciej Moryń & Przemysław Gogacz")

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    # app = PatientApplication()
    # app.run()
    patient = Patient(13, 33.6, 100, False, 3000)
    determinant = DiseaseDeterminant(patient)
    print(determinant.determine_cold_probability())
