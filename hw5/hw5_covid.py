import sys
import os
os.system(sys.executable + " -m pip install requests")

import requests
import json
import time
from datetime import datetime


# Read the file and create a list of state abbreviations 
file_path = "/Users/haydenhatch/data5500/hw5/states_territories.txt"
states_t = [ line.strip() for line in open(file_path).readlines() ]
print(states_t)

# Url's for API
url1 = "https://api.covidtracking.com/v1/states/"
url2 = "/daily.json"

#keys used to call to the API
key_date = "date"
key_state = "state"
key_positive_increase = "positiveIncrease"


for state in states_t:
    # Constructs full URL with state included and puts data in a dictionary
    url = url1 + state + url2
    req = requests.get(url)
    data = json.loads(req.text)

    # Saves the dictionary for each state into a JSON file in the specified folder

    folder_path = "/Users/haydenhatch/data5500/hw5/StateJSONs"
    filename = os.path.join(folder_path,f"{state}.json")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

        # Creates variables to hold stats as well as a dictionary to specify months
    total_positives = []
    highest_positives = 0
    no_new_cases_counter = 0
    monthly_cases = {}

    #Iterate over each day's data for the state

    for day in data:
        #extract and format date from the data
        date = str(day.get(key_date))
        year = date[:4]
        month = date[4:6]
        date2 = year + "-" + month
        state = day.get(key_state)
        positive_cases = day.get(key_positive_increase)
        positive_cases = int(positive_cases)

        #check if current day is the new highest cases so far

        if positive_cases > highest_positives:
            highest_positives = positive_cases
            highest_date = date

        #check if there were no new cases on the current day
        
        if positive_cases == 0:
            if no_new_cases_counter == 0:
                no_new_cases_date = date
                no_new_cases_counter = 1
        else:
            no_new_cases_date = "none"

        total_positives.append(positive_cases)
        # Calculate average number of new cases
        average_positives = sum(total_positives)/len(total_positives)

        if date2 not in monthly_cases:
            monthly_cases[date2] = 0
        monthly_cases[date2] += positive_cases
        # Find month with highest and lowest number of cases
        max_month = max(monthly_cases, key=monthly_cases.get)
        min_month = min(monthly_cases, key=monthly_cases.get)

    #Prints all analysis into the console for each state

    print("\nCovid confirmed cases stats")
    print(f"State: {state}")
    print(f"Average number of new daily confirmed cases for entire state dataset: {average_positives}")
    print(f"Date with highest new number of covid cases: {highest_date}")
    print(f"Most recent date with no new covid cases: {no_new_cases_date}")
    print(f"Month with highest new number of covid cases: {max_month}")
    print(f"Month with lowest new number of covid cases: {min_month}")


    

