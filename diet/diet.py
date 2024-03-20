import datetime
import pandas as pd
import csv

class Person:
    def __init__(self,
                 name: str,
                 year: int,
                 gender: str,
                 height: int,
                 weight: float,
                 exercise: float,
                 bmr=None,
                 tdee=None):
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
        # Define the path of the database
        self.path = path      
        # Create the nutritional empty dictionary
        self.df = {}       
        # Open the csv nutritional database
        with open(self.path, 'r') as file:
            csv_reader = csv.reader(file)         
            # Skip the header
            next(csv_reader)           
            for row in csv_reader:              
                # The index is the first item of the row
                index = str(row[0])          
                # The values are all the other value and replace comma
                values = [value.replace(',', '.') for value in row[1:]]            
                # Create the key value pair in the nutritional empty list
                self.df[index] = values

class Day:
    def __init__(self, ):
        self.breakfast = {}
        self.lunch = {}
        self.dinner = {}
    
    def adding_food(self, dictionary_food, nutritional_dataframe, meal_label):
        """Create a function which creates a dictionary for each meal"""
        # Create an empty dataframe which will contain info for each meal
        food_data = {}
        for food, quantity in dictionary_food.items():
            # Create a list which will return the nutritional value of the food you'd like to eat, multiplied by the quantity of it starting from the nutritional db
            lista = [round(quantity * float(value), 2) for value in nutritionaltable[food][3:-1]]
            # Append the quantity and the meal label on the list
            lista.insert(0, quantity)
            lista.append(meal_label)
            # Associate each food with its information
            food_data[food] = lista
        
        if meal_label == 'breakfast':
            self.breakfast = food_data
        elif meal_label == 'lunch':
            self.lunch = food_data
        elif meal_label == 'dinner':
            self.dinner = food_data
        
        return food_data

    def summary(self):
        self.day = {**self.breakfast, **self.lunch, **self.dinner}
        self.day = pd.DataFrame.from_dict(self.day, orient='index', columns=['Quantity', 'Kcal', 'Fat', 'Sat_Fat', 'Carbs', 'Sugars', 'Fibers', 'Proteins', 'Salt', 'Meal'])
        print(self.day)
        
        print("Today you eat: ")
        for column in self.day.columns[1:-1]:
            print(round(self.day[column].sum(), 2), column)
            
        print("\nFor each meal you eat:")
        print(self.day.groupby('Meal').sum())
      
vincenzo = Person("Vincenzo", 1999, "M", 177, 83.5, 1.2)
nutritionaltable = NutritionalTable('/home/vincenzopi/Scrivania/pythonproject/dataframe.csv').df
daily_breakfast = {'skyr': 1, 'fette toast': 4, 'schocokreme': 50}.

Monday = Day()
Monday.adding_food({'pasta': 150, 'olio evo' : 15}, nutritionaltable, 'lunch')
Monday.adding_food(daily_breakfast, nutritionaltable, 'breakfast')
Monday.summary()
Monday.day
