import pandas as pd
import re

# Load the Excel file
excel_file_path = 'Studien werte Liste.xlsx'
study_df = pd.read_excel(excel_file_path)

# Define the regex patterns
regex_patterns = {
    # Patterns to recognize various statistical terms and values
    "95-%-Konfidenzintervall": r"95-%-Konfidenzintervall\s*\(?KI\)?\s*[:=]\s*([-+]?\d+,\d+\s*[-–]\s*[-+]?\d+,\d+)",
    "95-%-KI": r"95-%-KI\s*[:=]\s*([-+]?\d+,\d+\s*[-–]\s*[-+]?\d+,\d+)",
    "p-Wert": r"(?:p-Wert\s*[:=]\s*|p\s*[:<=>]\s*)([-+]?\d+,\d+)",
    "Cohens d": r"Cohens d\s*[:=]\s*([-+]?\d+,\d+)|Cohen’s d\s*[:=]\s*([-+]?\d+,\d+)",
    "Beschreibung": r"adjustierte Differenz\s*[:=]\s*([-+]?\d+,\d+)|MWD\s*[:=]\s*([-+]?\d+,\d+)|MWD in der Änderung von Baseline zu \d+ Wochen\s*[:=]\s*([-+]?\d+,\d+)|Differenz\s*[:=]\s*([-+]?\d+,\d+)|Differenz zu \d+ (Tagen|Monaten)\s*[:=]\s*([-+]?\d+,\d+)|Veränderung\s*[:=]\s*([-+]?\d+,\d+)|Veränderung zu T\d+\s*[:=]\s*([-+]?\d+,\d+)|normierter Beta-Koeffizient\s*\(\ß-norm\)\s*[:=]\s*([-+]?\d+,\d+)",
    "Odds Ratio": r"Odds Ratio\s*[:=]\s*([-+]?\d+,\d+)",
    "Hedges g": r"Hedges g\s*[:=]\s*([-+]?\d+,\d+)|Hedges´ g\s*[:=]\s*([-+]?\d+,\d+)",
    "partielles eta2": r"partielles eta2\s*[:=]\s*([-+]?\d+,\d+)",
    "PAS": r"PAS nach \d+ Wochen: MD im Gruppenunterschied\s*[:=]\s*([-+]?\d+,\d+)"
}

# Function to transform pattern data
def transform_pattern_data(pattern):
    # Check if the pattern is empty
    if pd.isna(pattern):
        return (None, None)
    try:
         # Evaluate the pattern (if it is a list or tuple)
        pattern = eval(pattern)
        keys = []
        values = []
        for item in pattern:
            key = item[0]
            value = item[1][0][0]
            keys.append(key)
            values.append(value)
        return (", ".join(keys), ", ".join(values))
    except Exception as e:
        print(f"Error processing pattern: {pattern} with error {e}")
        return (None, None)

# Function to extract data using regex patterns
def extract_data(text, patterns):
    extracted_data = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            if isinstance(matches[0], tuple):
                extracted_data[key] = matches[0][0] if matches[0][0] else matches[0][1]
            else:
                extracted_data[key] = matches[0]
    return extracted_data

# Function to determine the title based on the extracted data
def determine_title(text):
    if any(keyword in text for keyword in ["MWD", "Mittelwertsdifferenz"]):
        title = "MWD"
    elif "adjustierte Differenz" in text:
        title = "adjustierte Differenz"
    elif "Differenz" in text:
        title = "Differenz"
    else:
        title = "Veränderung"

    if "Baseline" in text:
        title += " (Baseline)"
    else:
        match = re.search(r"(\d+ Wochen|\d+ Monaten|T\d+)", text)
        if match:
            title += f" ({match.group(1)})"
    return title

# Function to split values and create separate columns
def split_values_to_columns(values):
    if pd.isna(values):
        return {}
    try:
        # Extract the first part before ';' for description and keep only the numeric value
        first_part = re.split(';', values)[0]
        if "=" in first_part:
            description_values = first_part.split('=')[-1].strip()
        else:
            description_values = first_part.split(':')[-1].strip()
        
        description_values = description_values.replace(")", "").replace("(", "")
        extracted_data = extract_data(values, regex_patterns)
        title = determine_title(values)

        result = {key: val for key, val in extracted_data.items()}
        result['Title'] = title
        result['Beschreibung'] = description_values
        return result
    except Exception as e:
        print(f"Error splitting values: {values} with error {e}")
        return {}

# Apply transformation to relevant columns and create separate columns for keys and values
for i in range(1, 6):
    col_name = f"pattern such {i}"
    study_df[f"pattern_{i}_keys"], study_df[f"pattern_{i}_values"] = zip(*study_df[col_name].apply(transform_pattern_data))

# Combine keys from all pattern columns into a single column
study_df['keys'] = study_df[[f"pattern_{i}_keys" for i in range(1, 6)]].apply(lambda x: '; '.join(x.dropna().astype(str)), axis=1)

# Split pattern values into separate columns
for i in range(1, 6):
    value_col_name = f"pattern_{i}_values"
    split_values_df = study_df[value_col_name].apply(split_values_to_columns).apply(pd.Series)
    study_df = pd.concat([study_df, split_values_df.add_prefix(f"pattern_{i}_")], axis=1)

# Function to parse percentage values
def parse_percentage(value):
    if isinstance(value, str) and '%' in value:
        value = value.replace('%', '').replace(',', '.').strip()
        return float(value) / 100 if ',' in value else float(value)
    return value

# Function to split values
def split_values(column):
    if pd.isna(column):
        return None, None
    try:
        if isinstance(column, str):
            column = eval(column)
        if isinstance(column, list) and len(column) == 1:
            column = column[0]
        if isinstance(column, tuple) and len(column) == 2:
            ig, ik = column
            ig = parse_percentage(ig)
            ik = parse_percentage(ik)
            return ig, ik
        if isinstance(column, (int, float)):
            return None, column
        return None, None
    except Exception as e:
        print(f"Error processing column: {column} with error {e}")
        return None, None

# Apply function to the columns "IG und IK" and "Drop-out IG und IK"
study_df['IG'], study_df['IK'] = zip(*study_df['IG und IK'].apply(split_values))

# Fehlende Werte mit 0 füllen und in ganze Zahlen konvertieren
study_df['IG'] = study_df['IG'].fillna(0).replace(",", "").astype(int)
study_df['IK'] = study_df['IK'].fillna(0).replace(",", "").astype(int)

# Remove unnecessary columns
study_df.drop(columns=[
    "app_type", "bewertungsentscheidung", "pattern_1_values", "pattern_2_values", 
    "pattern_3_values", "pattern_4_keys", "pattern_4_values", "pattern_5_keys", 
    "pattern_5_values", "pattern such 1", "pattern such 2", "pattern such 3", 
    "pattern such 4", "pattern such 5", "vergleich pattern such 6", 
    "IG und IK", "Drop-out IG und IK"], inplace=True)

# Copy the DataFrame for the final result
combined_df = study_df.copy()

# Save the results to a new Excel file
output_file_path = 'Transformed.xlsx'
combined_df.to_excel(output_file_path, index=False)

print(f"Transformed data saved to {output_file_path}")
