import pandas as pd
import numpy as np
from math import sqrt
from sqlalchemy import create_engine

# Database connection parameters
username = 'root'
password = 'Passw0rd'
hostname = 'localhost'
database = 'k_test'

# Create a connection to the database
engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}/{database}")

# Read the CSV file
df = pd.read_csv('sensor_data.csv')

# Convert the 'Timestamp' column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Set 'Timestamp' as the index
df.set_index('Timestamp', inplace=True)

# Apply the Hanning window and FFT to each axis
for axis in ['X', 'Y', 'Z']:
    # Filter the DataFrame to only include accelerometer readings
    accelerometer_data = df[df['Sensor'] == 'Accelerometer'][axis]

    # Apply the Hanning window
    windowed_data = accelerometer_data * np.hanning(len(accelerometer_data))

    # Convert the Pandas Series to a NumPy array
    windowed_data = windowed_data.to_numpy()

    # Apply FFT
    fft_data = np.fft.fft(windowed_data)

    # Calculate the sampling period (assuming the data is evenly sampled)
    sampling_period = (df.index[1] - df.index[0]).total_seconds()

    # Compute the frequencies for the FFT
    freq = np.fft.fftfreq(len(accelerometer_data), sampling_period)

    # Only keep the positive frequencies
    positive_freq_mask = freq >= 0
    freq = freq[positive_freq_mask]
    fft_data = fft_data[positive_freq_mask]

    # Create a DataFrame from the FFT data
    fft_df = pd.DataFrame({
        'Frequency': freq,
        'Amplitude': np.abs(fft_data),
        'Timestamp': df[df['Sensor'] == 'Accelerometer'].index[:len(freq)]  # Add the timestamp from the original DataFrame
    })

    # Write the DataFrame to the MySQL database
    fft_df.to_sql(f'fft_{axis}', engine, if_exists='append')

# Filter the DataFrame to only include temperature readings
temperature_data = df[df['Sensor'] == 'Temperature']['X']

# Remove any rows with missing 'X' values
temperature_data = temperature_data.dropna()

# Calculate the RMS of the temperature data
rms_temperature = sqrt((temperature_data**2).mean())

# Create a DataFrame from the RMS
rms_df = pd.DataFrame({
    'RMS_Temperature': [rms_temperature],
    'Timestamp': df[df['Sensor'] == 'Temperature'].index[:1]  # Add the timestamp from the original DataFrame
})

# Write the DataFrame to the MySQL database
rms_df.to_sql('rms_temperature', engine, if_exists='append')