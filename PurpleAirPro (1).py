import pandas as pd
import requests as rq
import datetime as dt
from io import StringIO
import os

# List of sensors and corresponding names
sensors_list = ['185075', '176209', '176235', '176237', '176243']
names_for_filePath = ["Jane-Wyola", "John-Crow", "Sidney-Crow", "Joe-Hardin", "Bob-Hardin"]

# Define the base URL and headers
base_url = 'https://api.purpleair.com/v1/sensors/'
headers = {'X-API-Key': '43418ADC-5C99-11EE-A77F-42010A800009'}
payload = {'fields': 'humidity_a, humidity_b, temperature_a, temperature_b, pressure_a, pressure_b, voc_a, voc_b, pm1.0_atm, pm2.5_atm, pm10.0_atm'}

# Create a new folder for the data
folderpath = r'C:\Users\mehdi\Documents\Purple_Air\NewData'
os.makedirs(folderpath, exist_ok=True)

# Loop through each sensor
for i, sensor_num in enumerate(sensors_list):
    # Build the URL for the sensor
    url = f'{base_url}{sensor_num}/history/csv'

    # Make the API call
    r = rq.get(url=url, headers=headers, params=payload)

    # Check if the API call was successful (status code 200)
    if r.status_code == 200:
        # Read the CSV data into a DataFrame
        result = pd.read_csv(StringIO(r.text))

        # Convert UNIX time to UTC and then to local time (Mountain)
        result['time_stamp_UTC'] = pd.to_datetime(result['time_stamp'], unit='s', utc=True).dt.tz_convert('US/Mountain')

        # Sort the DataFrame by timestamp
        df = result.sort_values(by=['time_stamp'], ascending=False)

        # Extract the date from the timestamp for creating daily folders
        date_str = df['time_stamp_UTC'].iloc[0].strftime('%Y-%m-%d') if not df.empty else dt.datetime.now().strftime('%Y-%m-%d')

        # Create a folder for each day
        day_folder = os.path.join(folderpath, date_str)
        os.makedirs(day_folder, exist_ok=True)

        # Create a filename based on the sensor name
        filename = f'{names_for_filePath[i]}-{sensor_num}.csv'

        # Full path for the CSV file
        filepath = os.path.join(day_folder, filename)

        # Save the DataFrame to the CSV file
        df.to_csv(filepath, index=False, header=True)

    else:
        print(f"Failed to retrieve data for sensor {sensor_num}. Status code: {r.status_code}")
