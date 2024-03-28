import pandas as pd
import requests as rq
import datetime as dt
import os

# List of sensors, corresponding names, and date ranges
sensors_info = [
    ('149972', 'C2 - Site A', '2021-09-11', '2021-09-13'),
    ('105200', 'Albuquerque', '2023-08-07', '2023-08-09'),
    ('170533', 'Albuquerque - Site B', '2021-03-15', '2021-03-17'),
    ('78031', 'Austin', '2023-08-15', '2023-08-17'),
    ('115313', 'Bend', '2023-08-01', '2023-08-03'),
    ('104690', 'Casper', '2023-08-20', '2023-08-22'),
    ('156841', 'Dekalb Co.', '2021-08-16', '2021-08-18'),
    ('127155', 'Dundas', '2023-05-21', '2023-05-23'),
    ('57157', 'Glendale', '2023-08-11', '2023-08-13'),
    ('51959', 'Houston', '2023-08-10', '2023-08-12'),
    ('137120', 'Irvine', '2020-10-25', '2020-10-27'),
    ('165605', 'Jefferson', '2023-05-10', '2023-05-12'),
    ('181053', 'Kansas City', '2023-05-18', '2023-05-20'),
    ('110634', 'Las Cruces - Site A', '2023-07-21', '2023-07-23'),
    ('2938', 'Las Cruces - Site B', '2021-11-20', '2021-11-22'),
    ('37693', 'Oakland', '2023-08-08', '2023-08-10'),
    ('12799', 'Pender Co.', '2021-02-13', '2021-02-15'),
    ('193773', 'Pensacola', '2023-08-14', '2023-08-16'),
    ('57157', 'Phoenix', '2021-06-06', '2021-06-08'),
    ('72315', 'Pitt Co.', '2023-08-05', '2023-08-07'),
    ('31619', 'Raleigh', '2022-11-25', '2022-11-27'),
    ('171959', 'Richmond', '2023-04-10', '2023-04-12'),
    ('156491', 'Rio Rancho - Site A', '2023-06-20', '2023-06-22'),
    ('55967', 'Rio Rancho - Site B', '2022-08-24', '2022-08-26'),
    ('36659', 'Roseburg', '2020-08-19', '2020-08-21'),
    ('197593', 'Salt River Reservation', '2019-10-24', '2019-10-26'),
    ('52019', 'Simi Valley', '2021-09-30', '2021-10-02'),
    ('121385', 'St. Clair Co.', '2023-08-12', '2023-08-14'),
    ('91785', 'Tuscon', '2021-04-29', '2021-05-01'),
    ('192023', 'Vinton', '2023-07-31', '2023-08-02'),
    ('186825', 'Wellford - Fire 1', '2023-07-14', '2023-07-16'),
    ('124793', 'Wellford - Fire 2', '2019-09-25', '2019-09-27'),
    ('115035', 'C2 - Site C', '2021-09-15', '2021-09-17')
]

# Define the base URL and headers
base_url = 'https://api.purpleair.com/v1/sensors/'
headers = {'X-API-Key': '43418ADC-5C99-11EE-A77F-42010A800009'}

# Create a new folder for the data
folderpath = r'C:\Users\mehdi\OneDrive\Bureau\lat-AirData'
os.makedirs(folderpath, exist_ok=True)

# Create an empty list to store latitude and longitude dictionaries
location_data = []

# Loop through each sensor
for sensor_info in sensors_info:
    sensor_num, station_name, start_date_str, end_date_str = sensor_info

    # Build the URL for the sensor
    url = f'{base_url}{sensor_num}'

    # Make the API call
    r = rq.get(url=url, headers=headers)

    # Check if the API call was successful (status code 200)
    if r.status_code == 200:
        sensor_info = r.json()
        latitude = sensor_info['sensor']['latitude']
        longitude = sensor_info['sensor']['longitude']
        location_data.append({'Station Name': station_name, 'Sensor Number': sensor_num, 'Latitude': latitude, 'Longitude': longitude})
    else:
        print(f"Failed to retrieve sensor info for sensor {sensor_num}. Status code: {r.status_code}")

# Convert location data to a DataFrame
location_df = pd.DataFrame(location_data)

# Save sensor location data to a CSV file
location_filepath = os.path.join(folderpath, 'sensor_locations.csv')
location_df.to_csv(location_filepath, index=False)