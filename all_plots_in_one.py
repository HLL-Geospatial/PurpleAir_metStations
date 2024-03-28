import pandas as pd
import os
import matplotlib.pyplot as plt

# Folder containing CSV files
folder_path = r'C:\Users\mehdi\OneDrive\Bureau\P_AirData'

# List to store PM2.5 data and corresponding site names for all files
all_pm25_data = []
site_names = []

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
                site_name = file_name[:-4]  # Extract site name

                # Append PM2.5 data and site name to the lists
                all_pm25_data.append(pm25_data)
                site_names.append(site_name)

# Create a single figure with subplots
num_plots = len(all_pm25_data)
num_cols = 3  # Number of columns
num_rows = -(-num_plots // num_cols)  # Calculate number of rows (ceiling division)

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

# Flatten axes if num_rows > 1
axes = axes.flatten() if num_rows > 1 else [axes]

# Plot each PM2.5 concentration data with site name as label
for ax, pm25_data, site_name in zip(axes, all_pm25_data, site_names):
    ax.plot(pm25_data)
    #ax.set_xlabel('Time')
    #ax.set_ylabel('PM2.5 Concentration (µg/m³)')
    #ax.set_title(f'PM2.5 Concentration Data from {site_name}')
    ax.legend([site_name])
    ax.grid(True)

# Adjust layout
plt.tight_layout()
plt.show()