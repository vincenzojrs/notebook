import datetime
import pandas as pd

class Person:
    def __init__(self, name: str, year: int, gender: str, height: int, weight: float, exercise: float, bmr=None, tdee=None):
        self.name = name
        self.age = int(datetime.date.today().year) - year 
        self.gender = gender
        self.height = height
        self.weight = weight
        self.exercise = exercise
        
        # if the bmw is not known, calculate using Harris-Benedict formula
        if bmr is None:
            if gender == 'F':
                self.bmr = round(655 + (9.6 * weight) + (1.8 * height) - (4.7 * self.age))
            elif gender == 'M':
                self.bmr = round(66 + (13.7 * weight) + (5 * height) - (6.8 * self.age))
        else:
            self.bmr = bmr
        
        # if tdee is not known, calculate using the activity multiplier 
        if tdee is None:
            self.tdee = self.bmr * exercise
        else:
            self.tdee = tdee
            
class NutritionalTable:
    """ Create a class for storing the nutritional database """
    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(self.path, decimal = ',')
        self.df.set_index('item', drop = True, inplace = True)
        
    def add_element(lista):
        """ Add a row to the nutritional table, in form of a list, where each elements is 'item', 'state', 'piece', 'gr/pack', 'kcal', 'fat', 'sat_fat', 'carb', 'sugar', 'fiber', 'protein', 'salt', 'price_per_pack']"""
        with open(self.path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(lista)
        
class Day:
    def __init__(self, dictionary_food, nutritional_dataframe):
        self.breakfast = adding_food(dictionary_food, nutritional_dataframe)
        self.lunch = None
        self.dinner = None
    
    @staticmethod
    def adding_food(dictionary_food, nutritional_dataframe):
        """ Create a function which is shared among all the classes """
        
        # Initialize a dataframe
        dataframe = pd.DataFrame()
        
        # Given a dictionary of [food, quantity], iterate over food
        for food in dictionary_food:
            quantity = dictionary_food[food]
            
            # Create a temporary dataframe, which contains macronutrients multiplied by the quantity
            df_to_concat = nutritional_dataframe.loc[food, ['kcal', 'fat', 'sat_fat', 'carb', 'sugar', 'fiber', 'protein', 'salt']] * quantity
            
            # Concatenate the original dataframe and the temporary one and transpose it
            dataframe = pd.concat([dataframe, df_to_concat], axis=1)
        return dataframe.T
    

vincenzo = Person("Vincenzo", 1999, "M", 177, 83.5, 1.2)
nutritionaltable = NutritionalTable('/home/vincenzopi/Scrivania/pythonproject/dataframe.csv').df

daily_breakfast = {'skyr': 1, 'fette toast': 10}

Monday = Day(daily_breakfast, nutritionaltable)
Tuesday = Day(daily_breakfast, nutritionaltable)
