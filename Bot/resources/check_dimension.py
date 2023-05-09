import json


class Dimension:
    def __init__(self):
        with open(r"./Bot/resources/dimensional_food.json", 'r', encoding='utf-8') as f:
            self.food = json.load(f)
        with open(r"./Bot/resources/dimensional_mass.json", 'r', encoding='utf-8') as f:
            self.mass = json.load(f)

    def check_food_dimensional(self, mess):
        return self.__check_in_mess(self.food, mess)

    def check_mass_dimensional(self, mess):
        return self.__check_in_mess(self.mass, mess)

    def get_food_dimens_mult(self, mess):
        return self.__get_dimens_mult(self.food, mess)

    def get_mass_dimens_mult(self, mess):
        return self.__get_dimens_mult(self.mass, mess)

    @staticmethod
    def __check_in_mess(demiss: dict, mess: str) -> bool:
        for dem in demiss.keys():
            if dem in mess:
                return True
        return False

    @staticmethod
    def __get_dimens_mult(demiss: dict, mess: str) -> (bool, str, float):

        for dem in demiss.keys():
            if dem in mess:
                return True, dem, demiss[dem]
        return False, '', ''
