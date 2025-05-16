import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city_month_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data from 2017!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago','new york city','washington']
    city = None
    while city not in cities:
        city_input=input('Which city wold you like to explore?\n    1 - Chicago\n    2 - New York City\n    3 - Washington\nPlease enter your choice (Enter number or city name):').lower()
        if city_input.lower() in ['1','chicago']:
            city='chicago'
        elif city_input.lower() in ['2','nyc', 'ny','new york','new york city']:
            city='new york city'
        elif city_input.lower() in ['3','dc', 'washington dc','wash dc', 'washington']:
            city='washington'
        else:
            print('Could not interpret city name \"{}\". Please verify that you have typed correctly, and select a city from 1 - Chicago, 2 - New York City, or 3 - Washington.'.format(city_input))
    print('Thank you! We will analyze data from {}.'.format(city.title()))
    
    # TO DO: get user input for month (all, january, february, ... , june)
    print('\nNow we will select a month, and we will analyze bike ride trips that began in your selected month.')
    months = ['january','february','march','april','may','june']
    month = None
    while not month:
        month_input = input('Which month would you like to filter by? Please enter a month between January and June, or type \"All\" to use all available data:')

        if month_input.lower()=='all':
            month = 'all'
        else:
            try:
                month = months[[mth[0:3] for mth in months].index(month_input.lower()[0:3])]
            except ValueError:
                print('"{}\" is not a valid month in this data set. Please enter "All" or select one of the following months: January, February, March, April, May, June, or July.'.format(month_input))
    if month=='all':
        print("Thank you! We will analyze data during all months (January through June)")
    else:
        print("Thank you! We will analyze data during the month of {}.".format(month.title()))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = None
    while not day:
        weekday_input = input('\nWhich day of the week would you like to filter by? Please enter a weekday (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday) or type \"All\" to use all available data:')

        if weekday_input.lower()=='all':
            day = 'all'
        else:
            try:
                day = weekdays[[wkd[0:3] for wkd in weekdays].index(weekday_input.lower()[0:3])]
            except ValueError:
                print('"{}\" is not a valid day of the week in this data set. Please enter "All" or select one of the following days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday.'.format(weekday_input))
    if day=='all':
        print("Thank you! We will analyze data for all days of the week")
    else:
        print("Thank you! We will analyze data for {}s.".format(day.title()))

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
    
    df = pd.read_csv(CITY_DATA[city])

    # Change start time column to date time, and create month, weekday, and hour columns:
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Add a column to show the combination of start and end stations:
    df['Start to End'] = df['Start Station'] + ' to ' + df['End Station']

    # Apply month and weekday filters:
    if month!='all':
        df = df[df['month']==month.title()]
    if day!='all':
        df = df[df['day_of_week']==day.title()]
    return df

def view_data(df,n_rows=5):
    see_file = input('Would you like to see the first {} rows of this data set? Type yes or no: '.format(n_rows))
    if see_file.lower()=='yes':
        row_start=0
        while see_file.lower()=='yes':
            print(df.iloc[row_start:row_start+n_rows])
            row_start+=n_rows
            if row_start>=len(df):
                see_file = input('We\'ve reached the end of the raw data. Would you like to begin again with the first {} rows of this data set? Type yes or no: '.format(n_rows))
                row_start=0
            else:
                see_file = input('Would you like to see the next {} rows of this data set? Type yes or no: '.format(n_rows))
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month: {}".format(df['month'].mode()[0]))


    # TO DO: display the most common day of week
    print("Most common day of week: {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print("Most common start hour: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most common start station: {}".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("Most common end station: {}".format(df['End Station'].mode()[0]))


    # TO DO: display most frequent combination of start station and end station trip
    print("Most common start and end station combination: {}.".format(df['Start to End'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time in this slice of the data: {}.".format((df['End Time'] - df['Start Time']).sum()))

    # TO DO: display mean travel time
    print("Mean travel time in this slice of the data: %.2f minutes" %(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of rides by customer type:\n')
    for key, val in df['User Type'].fillna('Null').value_counts().items():
        print('{}: {}'.format(key,val))

    if city=='washington':
        print('\nGender and birth year not available for Washington customers.')
    else:
        # TO DO: Display counts of gender
        print('\nCounts of rides by customer gender:\n')
        for key, val in df['Gender'].fillna('Null').value_counts().items():
            print('{}: {}'.format(key,val))

        
        # TO DO: Display earliest, most recent, and most common year of birth
        print('\nCustomer birth year stats:\n')
        print('Earliest customer birth year: {}'.format(int(df['Birth Year'].min())))
        print('Most recent customer birth year: {}'.format(int(df['Birth Year'].max())))
        print('Most common customer birth year: {}'.format(int(df['Birth Year'].mode()[0])))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_city_month_filters()
        df = load_data(city, month, day)
        view_data(df,n_rows=5)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
