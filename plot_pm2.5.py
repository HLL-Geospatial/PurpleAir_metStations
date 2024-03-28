import pandas as pd
import os
import matplotlib.pyplot as plt

# Folder containing CSV files
folder_path = r'C:\Users\mehdi\OneDrive\Bureau\P_AirData'

# List to store PM2.5 data for all files
all_pm25_data = []

# Recursively search for CSV files in all subfolders
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith('.csv'):
            file_path = os.path.join(root, file_name)

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Convert timestamp to datetime
            df['time_stamp_UTC'] = pd.to_datetime(df['time_stamp'], unit='s')

            # Check if 'pm2.5_atm' column exists
            if 'pm2.5_atm' in df.columns:
                # Extract PM2.5 data
                pm25_data = df['pm2.5_atm']

                # Plot PM2.5 data
                plt.figure(figsize=(10, 5))  # Adjust size as needed
                plt.plot(df['time_stamp_UTC'], pm25_data, label=file_name)
                plt.xlabel('Time')
                plt.ylabel('PM2.5 Concentration (µg/m³)')
                plt.title(f'PM2.5 Concentration Data from {file_name}')
                plt.legend()
                plt.grid(True)

                # Save the figure as PNG
                output_file_path = os.path.join(root, f'{file_name[:-4]}_PM25.png')
                plt.savefig(output_file_path)

                # Close the figure to release memory
                plt.close()

                # Append PM2.5 data to the list
                all_pm25_data.append(pm25_data)

# Check if any PM2.5 data was extracted
if all_pm25_data:
    print("PM2.5 data extracted from the CSV files.")
else:
    print("No PM2.5 data found in the CSV files.")