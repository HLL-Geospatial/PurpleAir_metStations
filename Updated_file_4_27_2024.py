import pandas as pd
import requests as rq
import datetime as dt
import os
from io import StringIO

# Define the base URL and headers
base_url = 'https://api.purpleair.com/v1/sensors/'
headers = {'X-API-Key': '43418ADC-5C99-11EE-A77F-42010A800009'}

# Define sensor IDs and names
sensor_list = {
    '210525': 'CG-1',
    '210571': 'CG-2',
    '210549': 'CG-3',
    '210537': 'CG-6',
    '210551': 'CG-8',
    '210539': 'CG-5'
}

# Get the current date
current_date = dt.datetime.now().strftime('%Y-%m-%d')

# Construct the folder path using the current date
folderpath = rf'C:\Users\mehdi\OneDrive\Bureau\sensors_auto_data_upload\{current_date}'
os.makedirs(folderpath, exist_ok=True)

# Set the start date and end date based on the system clock
end_timestamp = int(dt.datetime.utcnow().timestamp())
start_timestamp = end_timestamp - 86400  # 86400 seconds = 1 day

for sensor_id, station_name in sensor_list.items():
    # Build the URL for the sensor
    url = f'{base_url}{sensor_id}/history/csv'

    payload = {
        'fields': 'humidity_a, temperature_a, pressure_a, pm1.0_atm, pm2.5_atm, pm10.0_atm',
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp
    }

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

        # Create a filename based on the sensor name
        filename = f'{station_name}-{sensor_id}.csv'

        # Full path for the CSV file
        filepath = os.path.join(folderpath, filename)

        # Save the DataFrame to the CSV file
        df.to_csv(filepath, index=False, header=True)

    else:
        print(f"Failed to retrieve data for sensor {sensor_id}. Status code: {r.status_code}")


# import pandas as pd
# import requests as rq
# import datetime as dt
# import os
# from io import StringIO

# # Define the base URL and headers
# base_url = 'https://api.purpleair.com/v1/sensors/'
# headers = {'X-API-Key': '43418ADC-5C99-11EE-A77F-42010A800009'}

# # Define sensor IDs and names
# sensor_list = {
#     '210525': 'CG-1',
#     '210571': 'CG-2',
#     '210549': 'CG-3',
#     '210537': 'CG-6',
#     '210551': 'CG-8',
#     '210539': 'CG-5'
# }

# # Create a new folder for the data
# folderpath = r'C:\Users\mehdi\OneDrive\Bureau\auto_data'
# os.makedirs(folderpath, exist_ok=True)

# # Set the start date and end date based on the system clock
# end_timestamp = int(dt.datetime.utcnow().timestamp())
# start_timestamp = end_timestamp - 86400  # 86400 seconds = 1 day

# for sensor_id, station_name in sensor_list.items():
#     # Build the URL for the sensor
#     url = f'{base_url}{sensor_id}/history/csv'

#     payload = {
#         'fields': 'humidity_a, temperature_a, pressure_a, pm1.0_atm, pm2.5_atm, pm10.0_atm',
#         'start_timestamp': start_timestamp,
#         'end_timestamp': end_timestamp
#     }

#     # Make the API call
#     r = rq.get(url=url, headers=headers, params=payload)

#     # Check if the API call was successful (status code 200)
#     if r.status_code == 200:
#         # Read the CSV data into a DataFrame
#         result = pd.read_csv(StringIO(r.text))

#         # Convert UNIX time to UTC and then to local time (Mountain)
#         result['time_stamp_UTC'] = pd.to_datetime(result['time_stamp'], unit='s', utc=True).dt.tz_convert('US/Mountain')

#         # Sort the DataFrame by timestamp
#         df = result.sort_values(by=['time_stamp'], ascending=False)

#         # Extract the date from the timestamp for creating daily folders
#         date_str = df['time_stamp_UTC'].iloc[0].strftime('%Y-%m-%d') if not df.empty else dt.datetime.now().strftime('%Y-%m-%d')

#         # Create a folder for each day including the station name
#         day_folder = os.path.join(folderpath, f'{date_str} - {station_name}')
#         os.makedirs(day_folder, exist_ok=True)

#         # Create a filename based on the sensor name
#         filename = f'{station_name}-{sensor_id}.csv'

#         # Full path for the CSV file
#         filepath = os.path.join(day_folder, filename)

#         # Save the DataFrame to the CSV file
#         df.to_csv(filepath, index=False, header=True)

#     else:
#         print(f"Failed to retrieve data for sensor {sensor_id}. Status code: {r.status_code}")