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


class Patient:
    def __init__(self, age: int, temperature: float, blood_pressure: int, cas: bool, bpm: int, fed: bool, weight: float):
        self.__age = age
        self.__temperature = temperature
        self.__blood_pressure = blood_pressure
        self.__cas = cas  # cas -> coughing and sneezing
        self.__bpm = bpm  # bpm -> beers per month
        self.__fed = fed  # fed -> family early deaths
        self.__weight = weight

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

    @property
    def fed(self):
        return self.__fed

    @property
    def weight(self):
        return self.__weight


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

        age = self.__patient.age
        min_age = 12
        max_age = 64
        max_age_multiplier = 0.15
        if age <= min_age or age >= max_age:
            age_multiplier = 1.0 + max_age_multiplier
        else:
            midpoint = (max_age - min_age) / 2
            absolute_age = abs(midpoint - age)
            age_multiplier = 1.0 + max_age_multiplier * (absolute_age / (max_age - midpoint))
        probability = probability * age_multiplier
        return min(probability, 1.0)

    # def determine_liver_problem_probability(self):
    #     month_length = 28.0
    #     apd = self.__patient.bpm / month_length  # apd -> average (beers) per day
    #     opw = 1.0 / 7.0  # opw -> one per week
    #     opd = 1.0  # opd -> one per day
    #     if apd <= opw:
    #         probability = 1.0 / 14
    #     elif apd <= opd:
    #         probability =
    #     return 0.0


class PatientApplication:
    def __init__(self):
        self.__root = tkinter.Tk()
        self.__root.title("es")

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
        self.__determine_disease_button["command"] = self.__determine_disease

    @staticmethod
    def __show_info():
        messagebox.showinfo("info", "expert system by Maciej Moryń & Przemysław Gogacz")

    def __determine_disease(self):
        patient = Patient(16, 32.0, 100, True, 100, True)
        determinant = DiseaseDeterminant(patient)
        cold_probability = round(determinant.determine_cold_probability(), ndigits=3)
        cold_probability_enum = Probability.determine_probability(cold_probability)
        result = F"cold : {cold_probability_enum.name} [{cold_probability * 100}%]"
        messagebox.showinfo("results", result)

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    app = PatientApplication()
    app.run()
