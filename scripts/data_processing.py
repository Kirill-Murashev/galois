import pandas as pd
import numpy as np
import unidecode


def read_and_process_data(file_path_to_process):
    # Determine the file extension
    file_extension = file_path_to_process.split('.')[-1].lower()

    # Load the data based on file type
    if file_extension == 'csv':
        data = pd.read_csv(file_path_to_process)
        message = f"Loading data from the file '{file_path_to_process}'"
    elif file_extension in ['xlsx', 'xls']:
        data = pd.read_excel(file_path_to_process)
        message = f"Loading data from the file '{file_path_to_process}'"
    elif file_extension == 'ods':
        data = pd.read_excel(file_path_to_process, engine='odf')
        message = f"Loading data from the file '{file_path_to_process}'"
    else:
        raise ValueError("Unsupported file format. Please provide a CSV, XLSX, or ODS file.")

    print(message)
    print(f"The file has {data.shape[0]} rows and {data.shape[1]} columns.")

    # Processing the data
    data.columns = [col.lower() for col in data.columns]
    data.columns = [unidecode.unidecode(col) for col in data.columns]

    # Verify and process 'id' column
    if 'id' not in data.columns:
        print("Error: The 'id' column is missing.")
        return None

    if data['id'].dtype != np.int64 or not data['id'].between(1, len(data)).all():
        print("Error: The 'id' column is not of type 'n' or contains invalid values.")
        return None
    else:
        print("Observation identifiers loaded successfully.")

    # Verify and process 'price' column
    if 'price' not in data.columns:
        print("Error: The 'price' column is missing.")
        return None

    if data['price'].dtype != np.float64:
        print("Error: The 'price' column is not of type 'r'.")
        return None
    else:
        print("Price data loaded successfully.")

    # Process other columns
    for col in data.columns:
        if col in ['id', 'price']:
            continue

        col_type = data.iloc[0][col].lower()
        if col_type in ['n', 'nat', 'natural']:
            if data[col].dtype != np.int64:
                print(f"Error: The column '{col}' is not of type 'n'.")
                return None
        elif col_type in ['r', 'real', 'f', 'float', 'float64']:
            if data[col].dtype != np.float64:
                print(f"Error: The column '{col}' is not of type 'r'.")
                return None
        elif col_type in ['b', 'bin', 'binary']:
            if not all(data[col].isin([0, 1])):
                print(f"Error: The column '{col}' is not of type 'b'.")
                return None
        else:
            print(f"Error: Unknown type '{col_type}' in column '{col}'.")
            return None

        print(f"Column '{col}' loaded successfully.")

    # Drop the second row (type row)
    data = data.drop(0).reset_index(drop=True)

    # Check for missing values
    if data.isnull().values.any():
        print("Error: The loaded data contains missing values.")
        return None

    # Final message
    n_observations = data.shape[0]
    k_variables = data.shape[1] - 2  # excluding 'id' and 'price'
    print(f"The loaded data has {n_observations} observations and {k_variables} variables. No missing values.")
    print("The uploaded data is suitable for processing.")

    return data
