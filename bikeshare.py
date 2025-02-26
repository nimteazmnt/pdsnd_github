import time
import pandas as pd
import numpy as np

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}

def get_filters():
    """
    Asks user to select a city, month, and day to analyze.
   
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore 3 cities US bikeshare data!')
    
    # Ask for city from user
    cities = ['chicago', 'new york city', 'washington']
    city = ''
    while city not in cities:
        city = input("Please specify a city from chicago, new york city and washington): ").lower()
        if city not in cities:
            print("Invalid input. Please try again.")

    # Ask for month from user
    months = ['january', 'february', 'march', 'april', 'may', 'june','all']
    month = ''
    while month not in months:
        month = input("Please type a month from january, february, march, april, may, june or all for no filter): ").lower()
        if month not in months:
            print("Invalid input. Please try again.")
    
    # Ask for day of the week from user
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']
    day = ''
    while day not in days:
        day = input("Please type a day from monday, tuesday, wednesday, thursday, friday, saturday, sunday or all for no filter): ").lower()
        if day not in days:
            print("Invalid input. Please try again.")

    print('-' * 40)
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
    
    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Separating month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()  
    
    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1  # +1 because months are 1-indexed
        df = df[df['month'] == month_index]  # Filter the DataFrame by month

    # Filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day]  # Filter the DataFrame by day of week
    
    return df
def display_raw_data(df):
    """
    Asks user if would like to see raw data in chunks of 5 rows
    Displays raw data in chunks of 5 rows upon user request.
    Displays if no data to show
    """
    row_index = 0
    while True:
        # Ask the user if they want to see 5 lines of raw data
        show_data = input("Would you like to see 5 lines of raw data? Enter yes or no: ").lower()
        if show_data == 'yes':
            # to show data of next 5 rows
            print(df.iloc[row_index:row_index + 5])
            row_index += 5  
            
            # Informing user about not other data to show
            if row_index >= len(df):
                print('End of data.')
                break
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # To display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month: {}'.format(common_month))

    # To display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day: {}'.format(common_day))

    # To display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # To display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most common start station: {}'.format(start_station))

    # To display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most common end station: {}'.format(end_station))

    # To display most frequent combination of start station and end station trip
    frequent_station_comb = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of start and end station: {}'.format(frequent_station_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # To display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time: {}'.format(total_travel))

    # To display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean travel time: {}'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # To display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('Counts of user types:\n{}'.format(count_user_type))

    # To display counts of gender if the column exists
    if 'Gender' in df.columns:     #checking if the info available
        gender_count = df['Gender'].value_counts()
        print('Counts of gender:\n{}'.format(gender_count))
    else:
        print('Gender data not available.')

    # To display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:      #checking if the info available
        earliest_birth = df['Birth Year'].min()
        print('Earliest year of birth: {}'.format(earliest_birth))
        recent_birth = df['Birth Year'].max()
        print('Most recent year of birth: {}'.format(recent_birth))
        common_birth = df['Birth Year'].mode()[0]
        print('Most common year of birth: {}'.format(common_birth))
    else:
        print('Birth Year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Function loop to ask user to display raw data in chunks of 5 rows
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
       
if __name__ == "__main__":
    main()
