
import pandas as pd
import warnings
from datetime import datetime

def Write_Log(file_path, message, log_df, flag):
    """Add a new entry to the log DataFrame, suppressing FutureWarnings for concat."""
    new_entry = pd.DataFrame({
        'Timestamp': [datetime.now()],
        'File_Path': [file_path],
        'Message': [message],
        'Flag': [flag]
    })

    # Suppress FutureWarnings when concatenating DataFrames
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        log_df = pd.concat([log_df, new_entry], ignore_index=True)

    return log_df