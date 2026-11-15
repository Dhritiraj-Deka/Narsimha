#Imports

import pandas as pd
from pathlib import Path
import ipaddress

#Required columns for missing column detection
REQUIRED_COLUMNS = {
    "timestamp",
    "ip_address",
    "username",
    "status"
}
#Valid statuses for status detection 
VALID_STATUSES = {"failed","success"}

def parse_auth_logs(file_path):

    #Check whether the file exists
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    #Read CSV file
    logs = pd.read_csv(path)

    #Check required columns
    missing_columns = REQUIRED_COLUMNS - set(logs.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )
    
    #Checks for missing data in those columns
    if logs[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise ValueError("CSV contains missing values in required columns.")

    #Checks in the ip ads are valid
    for ip in logs['ip_address']:
        try:
            ipaddress.ip_address(str(ip).strip())
        except ValueError:
            raise ValueError(f"Invalid IP address found: {ip}")
    
    #Checks for invalid time stamps
    try:
        logs["timestamp"]=pd.to_datetime(
            #pd(pandas).to_datetime converts CSV data into proper timestamp
            logs["timestamp"],
            errors="raise"
        )
    except (ValueError, TypeError):
        raise ValueError("CSV contains invalid timestamps.")    

    #Checks for invalid login status (failed or success  thing)
    invalid_statuses = set(logs["status"].str.lower()) - VALID_STATUSES
    #.str.lower() makes it case insensitive 
    if invalid_statuses:
        raise ValueError(f"Invalid login statuses found: {invalid_statuses}")

    return logs