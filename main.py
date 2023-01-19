from enum import Enum


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
    def __init__(self, age: int, temperature: float, blood_pressure: int, coughing: bool, alcohol_consumption: AlcoholConsumption):
        self.__age = age
        self.__temperature = temperature
        self.__blood_pressure = blood_pressure
        self.__coughing = coughing

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
    def coughing(self):
        return self.__coughing

class DiseaseDeterminant:
    @staticmethod
    def determine_cold_probability(patient: Patient) -> float:
        temperature_threshold = TemperatureThreshold.determine_temperature_threshold(patient.temperature)
        if temperature_threshold == TemperatureThreshold.DEADLY:
            probability = 0.0
        else:
            cold_temperature = TemperatureThreshold.CRITICAL.value - TemperatureThreshold.ABNORMAL.value
            if temperature_threshold == TemperatureThreshold.CRITICAL:
                if patient.temperature < TemperatureThreshold.BASE.value:
                    probability = (patient.temperature - (TemperatureThreshold.BASE.value - TemperatureThreshold.CRITICAL.value)) / cold_temperature
                else:
                    probability = 1.0 - ((patient.temperature - (TemperatureThreshold.BASE.value + TemperatureThreshold.ABNORMAL.value)) / cold_temperature)
            else:
                absolute_temperature = abs(TemperatureThreshold.BASE.value - patient.temperature)
                probability = absolute_temperature / cold_temperature
        if temperature_threshold != TemperatureThreshold.DEADLY and patient.coughing:
            probability = probability + 0.1
        return min(probability, 1)

    @staticmethod
    def determine_heart_problem_probability(patient: Patient) -> float:
        return 0.0

    @staticmethod
    def determine_liver_problem_probability(patient: Patient) -> float:
        return 0.0

    @staticmethod
    def determine_death_probability(patient: Patient) -> float:
        return 0.0

    @staticmethod
    def determine_other_disease_probability(patient: Patient) -> float:
        return 0.0


if __name__ == "__main__":
    p = Patient(13, 34.0, 0, False)
    print(DiseaseDeterminant.determine_cold_probability(p))
