import json
import requests
from datetime import datetime


class detailAsteriod():
    def __init__(self, date, date_full, epoch_data, relative_velocity, miss_distance, orbiting_body):
        self.date = date
        self.date_full = date_full
        self.epoch_data = epoch_data
        self.relative_velocity = relative_velocity
        self.miss_distance = miss_distance
        self.orbiting_body = orbiting_body

    def __str__(self):
            return "date: {}, \ndate_full: {}, \nepoch_data: {}, \nrelative_velocity: {}, \nmiss_distance: {}, \norbiting_body: {}".format(self.date, self.date_full, self.epoch_data, self.relative_velocity, self.miss_distance, self.orbiting_body)


class asteroidNearMiss():
    def __init__(self, id, neo_reference_id, name, nasa_jpl_url, absolute_magnitude_h):
        self.id = id
        self.neo_reference_id = neo_reference_id
        self.name = name
        self.nasa_jpl_url = nasa_jpl_url
        self.absolute_magnitude_h = absolute_magnitude_h

    def __str__(self):
        return "id: {},neo_reference_id: {}, name: {}, nasa_jpl_url: {}, absolute_magnitude_h: {}".format( self.id, self.neo_reference_id, self.name, self.nasa_jpl_url, self.absolute_magnitude_h)

#Write a function that gets start and end dates from the user
def GetDate(dateType):
    while True:
        date = input("Please pick a {} yyyy-mm-dd:".format(dateType))
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print('Sorry, but it looks like you have entered an invalid date.')
            continue


def IsDate(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True 
    except ValueError:
        return False 

    return True

# Write a function that validates the date entered by the user.
def ValidDateRange(startdate, enddate):
    if IsDate(startdate) and IsDate(enddate):
        time_diff = datetime.strptime(enddate, '%Y-%m-%d') - datetime.strptime(startdate, '%Y-%m-%d')
        print('time_diff: ' + str(time_diff))
    else:
        return False
    if 5 >= time_diff.days >= 0:
        return True
    return False


def get_index():
    while True:
        user_choice = input('Please select which asteroid you will like to see by using the numbers addressed to them:\t')
        try:
            int(user_choice)
            return int(user_choice) - 1
        except ValueError():
            print("Sorry but you have entered the wrong value.")
            continue


def main():
    print('-'*150, '\n')
    print('Hello and welcome to my NASA API', '\n')
    print('-'*150, '\n')

    print('Please enter the start and finish date that you would like to see', '\n')

# Get start and end dates from the user
    start_date = GetDate("Start Date")
    end_date = GetDate("End Date")

    #validation
    if IsDate(start_date) and IsDate(end_date) and ValidDateRange(start_date, end_date):
        strAPI = "https://api.nasa.gov/neo/rest/v1/feed?start_date="+ start_date +"&end_date="+ end_date +"&api_key=9IwBXrBUTE3lOQBarXs2KEnCBq5Mp30av40eL22A"
        response = requests.get(strAPI)
        json_data = response.json()
        objects = json_data.get("near_earth_objects")

        #Put everything in a list
        result = []
        for date in objects:
            for value in objects[date]:
                result.append(asteroidNearMiss(value.get('id'), value.get('neo_reference_id'), value.get('name'), value.get('nasa_jpl_url'), value.get('absolute_magnitude_h')))
        
        asteroidID = []

        for value in result:
            asteroidID.append(value.id)
        else: 
            print('Sorry you inputted a wrong date or your start and end date difference was over 5 days')

    print('-'*150, '\n')
    print('Please choose an asteroid to see its data.', '\n')


    for i in range(len(asteroidID)):
        print('{}. {}'.format(i + 1, asteroidID[i]))

    print('\n', '-'*150)

    strAPI = "https://api.nasa.gov/neo/rest/v1/neo/" + asteroidID[get_index()] + "?api_key=9IwBXrBUTE3lOQBarXs2KEnCBq5Mp30av40eL22A"
    print(strAPI)
    response = requests.get(strAPI)
    json_data = response.json()
    objects = json_data.get("close_approach_data")

    result = []

    for i in range(1): 
        result.append(detailAsteriod(objects[i].get('close_approach_date'), objects[i].get('close_approach_date_full'), objects[i].get('epoch_date_close_approach'), objects[i].get('relative_velocity'), objects[i].get('miss_distance'),objects[i].get("orbiting_body")))
    
    for datapoint in result:
        print('\n', '-'*150, '\n')
        print(datapoint)
        print('-'*150, '\n')

if __name__ == "__main__":
    main()
    while True:
        user_quit = input('Would you like to continue using the NASA API?(y/n)')

        if user_quit.upper() == 'Y':
            main()

        elif user_quit.upper() == 'N':
            print('Thank you and have a nice day!')
            break

        else:
            print('Sorry, but it looks like you have entered an invalid option.')
            continue

def ValidInputRange(user_choice, upper):
    while True:
        try:
            if user_choice >= 0 and user_choice <= upper:
                return True
            else:
                print("Sorry but it looks like you have entered the wrong value.")
        except ValueError:
            print("Pick a number between 0 and ", upper,":n/")
            continue
