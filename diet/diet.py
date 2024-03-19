import datetime
import pandas as pd

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
        self.path = path
        self.df = pd.read_csv(self.path, decimal = ',')
        self.df.set_index('item', drop = True, inplace = True)
        
    def add_element(self, lista):
        """ Add a row to the nutritional table, in form of a list, where each elements is 'item', 'state', 'piece', 'gr/pack', 'kcal', 'fat', 'sat_fat', 'carb', 'sugar', 'fiber', 'protein', 'salt', 'price_per_pack']"""
        with open(self.path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(lista)
   
class Day:
    def adding_food(self, dictionary_food, nutritional_dataframe, meal_label):
        """ Create a function which creates dataframe for each meal """       
        # Initialize a dataframe
        dataframe = pd.DataFrame()
        
        # Given a dictionary of [food, quantity], iterate over food
        for food, quantity in dictionary_food.items():
            # Create a temporary dataframe, which contains macronutrients multiplied by the quantity
            df_to_concat = nutritional_dataframe.loc[food, ['kcal', 'fat', 'sat_fat', 'carb', 'sugar', 'fiber', 'protein', 'salt']] * quantity
            # Add a 'quantity' column
            df_to_concat['quantity'] = quantity
            # Add a 'meal_label' column
            df_to_concat['meal_label'] = meal_label
            
            # Concatenate the original dataframe and the temporary one and transpose it
            dataframe = pd.concat([dataframe, df_to_concat], axis=1)
        return dataframe.T
    
    def __init__(self, dictionary_food, nutritional_dataframe):
        self.breakfast = self.adding_food(dictionary_food, nutritional_dataframe, 'breakfast')
        self.lunch = pd.DataFrame()  
        self.dinner = pd.DataFrame() 
        
    def adding_meal(self, dictionary_food, nutritional_dataframe, meal):
        """ Add meal for a certain day """ 
        df = self.adding_food(dictionary_food, nutritional_dataframe, meal)
        
        if meal == 'lunch':
            self.lunch = pd.concat([self.lunch, df], axis=0)
        elif meal == 'dinner':
            self.dinner = pd.concat([self.dinner, df], axis=0)

        self.day = pd.concat([self.breakfast, self.lunch, self.dinner], axis=0)
        
    def add_summary(self):
        """ Add summaries per day and per meal """
        
        # For each column in the daily meals dataframe
        for column in self.day.columns[:-1]:
            # Print the total by column
            print(f'Total daily {column}', round(self.day[column].sum()))
            
        # and the total grouped by meal
        print(self.day.groupby('meal_label').sum())
            
vincenzo = Person("Vincenzo", 1999, "M", 177, 83.5, 1.2)
nutritionaltable = NutritionalTable('/home/vincenzopi/Scrivania/pythonproject/dataframe.csv').df

daily_breakfast = {'skyr': 1, 'fette toast': 4, 'schocokreme': 50}

Monday = Day(daily_breakfast, nutritionaltable)
Monday.adding_meal({'pasta': 150, 'olio evo' : 15}, nutritionaltable, 'lunch')
Monday.adding_meal({'pane integrale': 3,  'olio evo': 30}, nutritionaltable, 'dinner')
Monday.add_summary()

Tuesday = Day(daily_breakfast, nutritionaltable)
Tuesday.adding_meal({'pasta': 150, 'olio evo' : 15}, nutritionaltable, 'lunch')
Tuesday.adding_meal({'pane integrale': 3,  'olio evo': 30}, nutritionaltable, 'dinner')

print(Monday.day)

