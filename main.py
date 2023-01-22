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


class Sex(Enum):
    FEMALE = "female"
    MALE = "male"

class Disease(Enum):
    NONE = "none"
    COLD = "cold"
    HEART_PROBLEM = "heart problem"
    LIVER_PROBLEM = "liver problem"
    DEATH = "death"
    OTHER_DISEASE = "other disease"


class Patient:
    def __init__(
            self,
            age: int,
            temperature: float,
            blood_pressure: int,
            cas: bool,
            waf: bool,
            bpm: int,
            umw: int,
            tpw: int,
            fed: bool,
            weight: float,
            height: float,
            sex: Sex
    ):
        self.__age = age
        self.__temperature = temperature
        self.__blood_pressure = blood_pressure
        self.__cas = cas  # cas -> coughing and sneezing
        self.__waf = waf  # waf -> weakness and fatigue
        self.__bpm = bpm  # bpm -> beers per month
        self.__umw = umw  # umw -> unhealthy meals a week
        self.__tpw = tpw  # tpw -> training per week
        self.__fed = fed  # fed -> family early deaths
        self.__weight = weight
        self.__height = height
        self.__sex = sex

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
    def waf(self):
        return self.__waf

    @property
    def bpm(self):
        return self.__bpm

    @property
    def umw(self):
        return self.__umw
    
    @property
    def tpw(self):
        return self.__tpw
    
    @property
    def fed(self):
        return self.__fed

    @property
    def weight(self):
        return self.__weight

    @property
    def height(self):
        return self.__height

    @property
    def sex(self):
        return self.__sex


class DiseaseDeterminant:
    def __init__(self, patient: Patient):
        self.__patient = patient
    
    def determine_obesity_probability(self): # otyłość
        height = self.__patient.height
        weights = self.__patient.weight
        bmi = (weights / height ** 2)
        if bmi < 10:
            probability = 0.0 + (self.__patient.age / 80) * 0.2
        elif bmi < 20 :
            probability = 0.2 + (self.__patient.age / 80) * 0.2
        elif bmi < 30 :
            probability = 0.4 + (self.__patient.age / 80) * 0.2
        else :
            probability = 0.6 + (self.__patient.age / 80) * 0.2

        probability = probability + ((self.__patient.umw / 7) * 0.1) - ((self.__patient.tpw / 5) * 0.2)

        return min(max(probability, 0.0), 1.0)
    
    def determine_flu_probability(self):  # grypa
        normal_temperature = 36.5
        temperature = self.__patient.temperature
        probability = 0.0
        if self.__patient.cas:
            probability = probability + (self.__patient.age / 80) 
        if self.__patient.waf:
            probability = probability + (self.__patient.age / 70) 

        if normal_temperature < temperature:
            abs_temperature = abs(normal_temperature-temperature) 
            probability = probability + (abs_temperature / 5) * 0.4

        return min(probability, 1.0)
    
    def determine_heart_attack_probability(self): # atak serca
        age = self.__patient.age
        obesity = self.determine_obesity_probability()
        liver = self.determine_liver_problem_probability()
        probability = age * 0.75 / 100

        if obesity > 0.9 and liver > 0.9:
            probability = 1
        else:
            probability = (0.4 * obesity + 0.6 * liver) * 0.7

        return min(probability, 1.0)
    
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

    def determine_liver_problem_probability(self):
        month_length = 28.0
        apd = self.__patient.bpm / month_length  # apd -> average (beers) per day
        opw = 1.0 / 7.0  # opw -> one per week
        opd = 1.0  # opd -> one per day
        tpd = 10.0  # tpd -> ten per day
        if apd <= opw:
            probability = apd
        elif apd <= opd:
            probability = (((apd - opw) / (opd - opw)) * (0.4 - opw)) + opw
        elif apd <= tpd:
            probability = ((((apd - opd) / (tpd - opd)) * 0.6) + 0.4) ** 0.5
        else:
            probability = 1.0

        age = self.__patient.age
        if self.__patient.fed and age >= 20:
            probability = probability * (1.0 + ((age - 20) / 40) * 0.3)

        if age <= 10:
            probability = probability * 0.8
        elif age <= 20:
            probability = probability * 0.9
        else:
            probability = probability * (1.0 + (age - 20) / 50)

        return min(probability, 1.0)


class PatientApplication:
    def __init__(self):
        self.__root = tkinter.Tk()
        self.__root.title("es")

        self.__age_unit_label = tkinter.Label(self.__root, text="[int]")
        self.__age_unit_label.grid(row=0, column=0, columnspan=1)
        self.__age_label = tkinter.Label(self.__root, text="age:")
        self.__age_label.grid(row=0, column=1, columnspan=2)
        self.__age_entry = tkinter.Entry(self.__root)
        self.__age_entry.grid(row=0, column=3, columnspan=3)

        self.__temperature_unit_label = tkinter.Label(self.__root, text="[float]")
        self.__temperature_unit_label.grid(row=1, column=0, columnspan=1)
        self.__temperature_label = tkinter.Label(self.__root, text="temperature:")
        self.__temperature_label.grid(row=1, column=1, columnspan=2)
        self.__temperature_entry = tkinter.Entry(self.__root)
        self.__temperature_entry.grid(row=1, column=3, columnspan=3)

        self.__blood_pressure_unit_label = tkinter.Label(self.__root, text="[int]")
        self.__blood_pressure_unit_label.grid(row=2, column=0, columnspan=1)
        self.__blood_pressure_label = tkinter.Label(self.__root, text="blood pressure:")
        self.__blood_pressure_label.grid(row=2, column=1, columnspan=2)
        self.__blood_pressure_entry = tkinter.Entry(self.__root)
        self.__blood_pressure_entry.grid(row=2, column=3, columnspan=3)

        self.__cas_unit_label = tkinter.Label(self.__root, text="[bool]")
        self.__cas_unit_label.grid(row=3, column=0, columnspan=1)
        self.__cas_label = tkinter.Label(self.__root, text="coughing and sneezing:")
        self.__cas_label.grid(row=3, column=1, columnspan=2)
        self.__cas_entry = tkinter.Entry(self.__root)
        self.__cas_entry.grid(row=3, column=3, columnspan=3)

        self.__bpm_unit_label = tkinter.Label(self.__root, text="[int]")
        self.__bpm_unit_label.grid(row=4, column=0, columnspan=1)
        self.__bpm_label = tkinter.Label(self.__root, text="beers per month:")
        self.__bpm_label.grid(row=4, column=1, columnspan=2)
        self.__bpm_entry = tkinter.Entry(self.__root)
        self.__bpm_entry.grid(row=4, column=3, columnspan=3)

        self.__umw_unit_label = tkinter.Label(self.__root, text="[int]")
        self.__umw_unit_label.grid(row=5, column=0, columnspan=1)
        self.__umw_label = tkinter.Label(self.__root, text="unhealthy meals a week:")
        self.__umw_label.grid(row=5, column=1, columnspan=2)
        self.__umw_entry = tkinter.Entry(self.__root)
        self.__umw_entry.grid(row=5, column=3, columnspan=3)

        self.__tpw_unit_label = tkinter.Label(self.__root, text="[int]")
        self.__tpw_unit_label.grid(row=6, column=0, columnspan=1)
        self.__tpw_label = tkinter.Label(self.__root, text="training per week:")
        self.__tpw_label.grid(row=6, column=1, columnspan=2)
        self.__tpw_entry = tkinter.Entry(self.__root)
        self.__tpw_entry.grid(row=6, column=3, columnspan=3)

        self.__fed_unit_label = tkinter.Label(self.__root, text="[bool]")
        self.__fed_unit_label.grid(row=7, column=0, columnspan=1)
        self.__fed_label = tkinter.Label(self.__root, text="family early deaths:")
        self.__fed_label.grid(row=7, column=1, columnspan=2)
        self.__fed_entry = tkinter.Entry(self.__root)
        self.__fed_entry.grid(row=7, column=3, columnspan=3)

        self.__weight_unit_label = tkinter.Label(self.__root, text="[float]")
        self.__weight_unit_label.grid(row=8, column=0, columnspan=1)
        self.__weight_label = tkinter.Label(self.__root, text="weight:")
        self.__weight_label.grid(row=8, column=1, columnspan=2)
        self.__weight_entry = tkinter.Entry(self.__root)
        self.__weight_entry.grid(row=8, column=3, columnspan=3)

        self.__height_unit_label = tkinter.Label(self.__root, text="[float]")
        self.__height_unit_label.grid(row=9, column=0, columnspan=1)
        self.__height_label = tkinter.Label(self.__root, text="height:")
        self.__height_label.grid(row=9, column=1, columnspan=2)
        self.__height_entry = tkinter.Entry(self.__root)
        self.__height_entry.grid(row=9, column=3, columnspan=3)

        self.__sex_unit_label = tkinter.Label(self.__root, text="[sex]")
        self.__sex_unit_label.grid(row=10, column=0, columnspan=1)
        self.__sex_label = tkinter.Label(self.__root, text="sex:")
        self.__sex_label.grid(row=10, column=1, columnspan=2)
        self.__sex_entry = tkinter.Entry(self.__root)
        self.__sex_entry.grid(row=10, column=3, columnspan=3)

        self.__waf_unit_label = tkinter.Label(self.__root, text="[bool]")
        self.__waf_unit_label.grid(row=11, column=0, columnspan=1)
        self.__waf_label = tkinter.Label(self.__root, text="weakness and fatigue:")
        self.__waf_label.grid(row=11, column=1, columnspan=2)
        self.__waf_entry = tkinter.Entry(self.__root)
        self.__waf_entry.grid(row=11, column=3, columnspan=3)

        self.__info_button = tkinter.Button(self.__root, text="info")
        self.__info_button.grid(row=12, column=0, columnspan=1)
        self.__info_button["command"] = PatientApplication.__show_info
        self.__determine_disease_button = tkinter.Button(self.__root, text="determine disease")
        self.__determine_disease_button.grid(row=12, column=1, columnspan=5)
        self.__determine_disease_button["command"] = self.__determine_disease

    @staticmethod
    def __show_info():
        messagebox.showinfo("info", "expert system by Maciej Moryń & Przemysław Gogacz")

    @staticmethod
    def __validate_int_entry(value: str, value_name: str, allow_negative: bool):
        if allow_negative:
            error_message = F"{value_name} must be integer value"
        else:
            error_message = F"{value_name} must be non-negative integer value"

        if len(value) == 0:
            messagebox.showerror("error", F"{value_name} must not be empty")
            return None
        try:
            int_value = int(value)
            if not allow_negative and int_value < 0:
                messagebox.showerror("error", error_message)
                return None
            return int_value
        except ValueError:
            messagebox.showerror("error", error_message)
            return None

    @staticmethod
    def __validate_float_entry(value: str, value_name: str, allow_negative: bool):
        if allow_negative:
            error_message = F"{value_name} must be float value"
        else:
            error_message = F"{value_name} must be non-negative float value"

        if len(value) == 0:
            messagebox.showerror("error", F"{value_name} must not be empty")
            return None
        try:
            float_value = float(value)
            if not allow_negative and float_value < 0.0:
                messagebox.showerror("error", error_message)
                return None
            return float_value
        except ValueError:
            messagebox.showerror("error", error_message)
            return None

    @staticmethod
    def __validate_bool_entry(value: str, value_name: str):
        if len(value) == 0:
            messagebox.showerror("error", F"{value_name} must not be empty")
            return None
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            messagebox.showerror("error", F"{value_name} must be bool [\'true\'\\\'false\'] value")
            return None

    @staticmethod
    def __validate_sex_entry(value: str):
        if len(value) == 0:
            messagebox.showerror("error", "sex value must not be empty")
            return None
        if value == "female":
            return Sex.FEMALE
        elif value == "male":
            return Sex.MALE
        else:
            messagebox.showerror("error", "sex value must be \'female\' or \'male\'")
            return None

    def __determine_disease(self):
        age_value = PatientApplication.__validate_int_entry(self.__age_entry.get(), "age", False)
        if age_value is None:
            return

        temperature_value = PatientApplication.__validate_float_entry(self.__temperature_entry.get(), "temperature", True)
        if temperature_value is None:
            return

        blood_pressure_value = PatientApplication.__validate_int_entry(self.__blood_pressure_entry.get(), "blood pressure", False)
        if blood_pressure_value is None:
            return

        cas_value = PatientApplication.__validate_bool_entry(self.__cas_entry.get(), "cas")
        if cas_value is None:
            return
        
        waf_value = PatientApplication.__validate_bool_entry(self.__waf_entry.get(), "waf")
        if waf_value is None:
            return

        bpm_value = PatientApplication.__validate_int_entry(self.__bpm_entry.get(), "bpm", False)
        if bpm_value is None:
            return
        
        umw_value = PatientApplication.__validate_int_entry(self.__umw_entry.get(), "umw", False)
        if umw_value is None:
            return
        
        tpw_value = PatientApplication.__validate_int_entry(self.__tpw_entry.get(), "tpw", False)
        if tpw_value is None:
            return
        
        fed_value = PatientApplication.__validate_bool_entry(self.__fed_entry.get(), "fed")
        if fed_value is None:
            return

        weight_value = PatientApplication.__validate_float_entry(self.__weight_entry.get(), "weight", False)
        if weight_value is None:
            return

        height_value = PatientApplication.__validate_float_entry(self.__height_entry.get(), "height", False)
        if height_value is None:
            return

        sex_value = PatientApplication.__validate_sex_entry(self.__sex_entry.get())
        if sex_value is None:
            return

        patient = Patient(
            age_value,
            temperature_value,
            blood_pressure_value,
            cas_value,
            waf_value,
            bpm_value,
            umw_value,
            tpw_value,
            fed_value,
            weight_value,
            height_value,
            sex_value
        )
        determinant = DiseaseDeterminant(patient)

        cold_probability = determinant.determine_cold_probability()
        cold_probability_enum = Probability.determine_probability(cold_probability)
        cold_probability_percent = round(cold_probability * 100, ndigits=3)
        cold_string = F"cold : {cold_probability_enum.name} [{cold_probability_percent}%]"

        liver_problem_probability = determinant.determine_liver_problem_probability()
        liver_problem_probability_enum = Probability.determine_probability(liver_problem_probability)
        liver_problem_probability_percent = round(liver_problem_probability * 100, ndigits=3)
        liver_problem_string = F"liver problem : {liver_problem_probability_enum.name} [{liver_problem_probability_percent}%]"
        
        obesity_probability = determinant.determine_obesity_probability()
        obesity_probability_enum = Probability.determine_probability(obesity_probability)
        obesity_probability_percent = round(obesity_probability * 100, ndigits=3)
        obesity_problem_string = F"obesity : {obesity_probability_enum.name} [{obesity_probability_percent}%]"
        
        flu_probability = determinant.determine_flu_probability()
        flu_probability_enum = Probability.determine_probability(flu_probability)
        flu_probability_percent = round(flu_probability * 100, ndigits=3)
        flu_problem_string = F"flu : {flu_probability_enum.name} [{flu_probability_percent}%]"

        heart_attack_probability = determinant.determine_heart_attack_probability()
        heart_attack_probability_enum = Probability.determine_probability(heart_attack_probability)
        heart_attack_probability_percent = round(heart_attack_probability * 100, ndigits=3)
        heart_attack_string = F"heart_attack : {heart_attack_probability_enum.name} [{heart_attack_probability_percent}%]"

        messagebox.showinfo("results",
                            F"{cold_string}\n{liver_problem_string}\n{obesity_problem_string}\n{flu_problem_string}\n{heart_attack_string}" )
        # messagebox.showinfo("results",
        #                     F"{flu_problem_string}" )  
    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    app = PatientApplication()
    app.run()
