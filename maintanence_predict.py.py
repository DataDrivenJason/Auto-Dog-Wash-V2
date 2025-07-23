import mysql.connector
import pandas as pd
import numpy as np
from datetime import timedelta
from decimal import Decimal

config = {
    "user": "root",
    "password" : "mySQLprogrammingclass_25",
    "host" : "localhost",
    "database" : "dog_wash_V2",
}

def connect_db():
    return mysql.connector.connect(**config)

def fetch_data():
    db_connection = connect_db()
    cursor = db_connection.cursor(dictionary=True)

    query = """
    SELECT 
        machine_id, 
        timestamp, 
        water_level, 
        soap_level, 
        tick_remover_level
    FROM 
        product_log
    ORDER BY 
        machine_id, timestamp;
    """

    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    cursor.close()
    db_connection.close()
    return df

# Fetch data
df = fetch_data()

# Define functions for depletion rate and prediction
def calculate_depletion_rate(df, consumable_column):
    df['prev_' + consumable_column] = df.groupby('machine_id')[consumable_column].shift(1)
    df['time_diff'] = (df['timestamp'] - df.groupby('machine_id')['timestamp'].shift(1)).dt.total_seconds() / 60
    df[consumable_column] = df[consumable_column].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
    df['prev_' + consumable_column] = df['prev_' + consumable_column].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
    df['depletion_rate'] = (df[consumable_column] - df['prev_' + consumable_column]) / df['time_diff']
    df['depletion_rate'] = df['depletion_rate'].apply(lambda x: np.nan if x <= 0 else x)
    return df

def calculate_prediction(df, consumable_column, critical_level):
    df['predicted_time_to_critical'] = np.where(df['depletion_rate'] > 0, 
                                                (df[consumable_column] - critical_level) / df['depletion_rate'], 
                                                np.nan)
    df['predicted_time_to_critical'] = df['predicted_time_to_critical'].apply(lambda x: max(x, 0) if x is not np.nan else np.nan)
    df['predicted_' + consumable_column + '_replacement'] = pd.to_datetime(df['timestamp']) + pd.to_timedelta(df['predicted_time_to_critical'], unit='m')
    return df

# Apply the functions for each consumable
df = calculate_depletion_rate(df, 'water_level')
df = calculate_depletion_rate(df, 'soap_level')
df = calculate_depletion_rate(df, 'tick_remover_level')

df = calculate_prediction(df, 'water_level', 50)
df = calculate_prediction(df, 'soap_level', 20)
df = calculate_prediction(df, 'tick_remover_level', 10)

# Calculate the earliest refill time for each machine
df['earliest_refill'] = df[['predicted_water_level_replacement', 
                            'predicted_soap_level_replacement', 
                            'predicted_tick_remover_level_replacement']].min(axis=1)

# Export the data to CSV to use in Power BI
df.to_csv('dog_wash_predictions_grouped.csv', index=False)

# Display the result
print(df.head())























