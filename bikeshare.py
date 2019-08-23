import time
import pandas as pd
import numpy as np

DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to see data for: Chicago, New York City or Washington?"
                     "\n").split(": ")[0].lower()
        try:
            if city not in DATA:
                print("Sorry,I have no idea about {}. Entering again within 'Chicago',"
                      "'New York City' or 'Washington' again.".format(city))
                continue
            else:
                break
        except ValueError as e:
            print("Exception occurred:{}".format(e))

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? January, February, March, April, May or June?\n").lower()
        try:
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
            if month not in months:
                print("Sorry, {} is not a valid month. Please type again by entering again".format(month))
                continue
            else:
                break
        except ValueError as e:
            print("Exception occurred: {}".format(e))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which Day of a week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, "
                    "All\n").lower()
        try:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
            if day not in days:
                print("Sorry, {} is not a valid day. Please enter the day of week again.".format(day))
                continue
            else:
                break
        except ValueError as e:
            print("Exception occurred: {}".format(e))

    print(city, ' ', month, ' ', day)
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

    df = pd.read_csv(DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]

    print("The Most Common Month: ", common_month)

    # display the most common day of week
    df['week'] = df['Start Time'].dt.week
    common_week = df['week'].mode()[0]

    print('The Most Common Day of a Week: ', common_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    print("The Most Common Start Hour: ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print("The Most Common Start Station: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print("The Most Common End Station: ", common_end_station)

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + ' to ' + ['End Station']
    common_station_combo = df['combo'].mode()[0]

    print("The Most Common Combination: ", common_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total Travel Time: ', total_travel_time)

    # display mean travel time
    average = df['Trip Duration'].mean()

    print('Mean Travel Time: ', average)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types: ', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Counts of Gender: ', gender)
    else:
        print("Gender info is not available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print("Earliest Birth Year: ", earliest_birth_year)

        recent_birth_year = df['Birth Year'].max()
        print("Recent Birth Year:", recent_birth_year)

        common_birth_year = df['Birth Year'].mode()[0]
        print("Most Common Birth Year: ", common_birth_year)
    else:
        print("Birth year info is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """ Displays 5 rows of raw data at a time """
    index1 = 0
    index2 = 5
    while True:
        raw_data = input('Would you like to see 5 more rows of data?\nPlease enter yes or no.\n').lower()
        if raw_data == 'yes':
            print(df.iloc[index1:index2])
            index1 += 5
            index2 += 5
        else:
            break


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
