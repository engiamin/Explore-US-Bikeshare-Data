import time
import pandas as pd
import numpy as np

#Dictionary with city data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Dictionary with months' data (Key: name of month; Value:month index)
MONTH_DATA = {'january':1, 'february':2, 'march':3, 'april':4, 'may': 5, 'june':6, 'all':'all months'}

#Dictionary with days' data (Key: name of day; Value:day index)
DAY_DATA = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6, 'all':'all days'}


def get_filters():
    """"
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #1# Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    CityName = ""
    while CityName.lower() not in CITY_DATA:
        CityName = str(input("\nPlease enter the name of the city you want to explore (Chicago, New York City or Washington)\n"))
        if CityName.lower() in CITY_DATA: #if the name of the city matches any of those in CITY_DATA
            city=CITY_DATA[CityName.lower()] #city will be assigned the value of corresponding file
        else:
            print("\nThe city you are looking for is not currently in our database. Please try again.\nYou can enter Chicago, New York City or Washington.\n")

    #2# Get user input for month (all, january, february, ... , june)
    MonthSelect=""
    while MonthSelect.lower() not in MONTH_DATA:
        MonthSelect = str(input("\nPlease enter the month you want to explore (january, february, march, april, may or june)\nYou can also enter all to view all months available.\n"))
        if MonthSelect.lower() in MONTH_DATA: #if the name of the month matches any of those in MONTH_DATA
            month = MONTH_DATA[MonthSelect.lower()] #month will be assigned the corresponding value number of this month
        else:
            print("\nThe month you are looking for is not currently in our database. Please try again.\nYou can enter any month between january to june or enter all.\n")

    #3# Get user input for day of week (all, monday, tuesday, ... sunday)
    DaySelect=""
    while DaySelect.lower() not in DAY_DATA:
        DaySelect = str(input("\nPlease enter the day you want to explore (monday, tuesday, wednesday, thursday, friday, saturday or sunday)\nYou can also enter all to view all days available.\n"))
        if DaySelect.lower() in DAY_DATA: #if the name of the day matches any of those in DAY_DATA
            day = DAY_DATA[DaySelect.lower()] #day will be assigned the corresponding value number of this day
        else:
            print("\nThe day you entered is not correct. Please try again.\nYou can enter any day of the week or enter all.\n")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #1# Read data
    df = pd.read_csv(city)

    #2# Convert 'Start Time' column to a date-time format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #3# Extract month, day and hour from 'Start Time' and create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    #4# Filter by month if applicable
    if month != 'all months':
        df = df[df['month'] == month]

    #5# Filter by day if applicable
    if day != 'all days':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #1# Display the most common month
    common_month = df['month'].mode()[0]
        #get the key (i.e. month name) from the value (i.e. number value of the month)
        #https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary
    common_month_name = list(MONTH_DATA.keys())[list(MONTH_DATA.values()).index(common_month)]
    print("The most common month is {}".format(common_month_name.title()))

    #2# Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
        #get the key (i.e. day name) from the value (i.e. number value of the day)
        #https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary
    common_day_name = list(DAY_DATA.keys())[list(DAY_DATA.values()).index(common_day)]
    print("The most common day is {}".format(common_day_name.title()))

    #3# Display the most common start hour
    common_hour = df['hour'].mode()[0]
        # Convert time to 12-hour format
    if 1 <= common_hour <= 11 :
        common_hour_formatted = common_hour
        am_pm = "am"
    elif common_hour == 0:
        common_hour_formatted = 12
        am_pm = "am"
    elif common_hour == 12:
        common_hour_formatted =  12
        am_pm = "pm"
    else:
        common_hour_formatted = common_hour - 12
        am_pm = "pm"

    print("The most common start hour is {} {}".format(common_hour_formatted, am_pm))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #1# Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}".format(common_start_station))

    #2# Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is {}".format(common_end_station))

    #3# Display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is {}".format(frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #FUNCTION to convert seconds to hours, minutes and seconds
    def seconds_converter(secs):
        minute, second = divmod(secs, 60)
        hour, minute = divmod(minute, 60)
        return hour, minute, second

    #1# Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_formatted = seconds_converter(total_travel_time)
    print("The total travel time is {} hours, {} minutes and {} seconds".format(int(total_travel_time_formatted[0]), int(total_travel_time_formatted[1]), int(total_travel_time_formatted[2])))

    #2# Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_formatted = seconds_converter(mean_travel_time)
    print("The average travel time is {} hours, {} minutes and {} seconds".format(int(mean_travel_time_formatted[0]), int(mean_travel_time_formatted[1]), int(mean_travel_time_formatted[2])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #1# Display counts of user types
    user_types = df.groupby('User Type', as_index=False).count()
    user_types_freq = df['User Type'].value_counts()
    print("There are {} types of users:".format(len(user_types)))
    print("{}\n".format(user_types_freq.to_string()))

    #2# Display counts of gender
    if 'Gender' in df:
        gender_freq = df['Gender'].value_counts()
        print("The gender frequency is\n{}\n".format(gender_freq.to_string()))

    #3# Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_yob = df['Birth Year'].min()
        recent_yob = df['Birth Year'].max()
        common_yob = df['Birth Year'].mode()[0]
        print("The earliest year of birth is {}\n".format(int(earliest_yob)))
        print("The most recent year of birth is {}\n".format(int(recent_yob)))
        print("The most common year of birth is {}\n".format(int(common_yob)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    response = str(input ("\n Do you want to see raw data?\n"))
    counter=0
    while True:
        if response.lower() == "yes":
            showData = df.iloc[counter:counter+5]
            print("\n",showData)
            counter = counter + 5
            response = str(input ("\n Do you want to see 5 lines more of raw data?\n"))
        elif response.lower()=="no":
            break
        else:
            print("\n Please enter a valid response (yes/no)")
            response = str(input ("\n Do you want to see 5 lines of raw data?\n"))

    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
