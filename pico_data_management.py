import pandas as pd
import sqlite3

# File and table information
# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
excel_file = 'comparison_results_with_intervals.xlsx'
sheet_name = 'Sheet1'  
database_file = 'dashboard/newdigaDB.db'
excel_werte = "Transformed.xlsx"
excel_score = 'abbreviations_descriptions.xlsx'
excel_des =  'F_diga_verzeichniss_2024_06_16.xlsx' 
excel_kategorie =  'kategorie_diga.xlsx' 

# Select only the desired columns
columns_to_import = [
    "diga_id",
    "app_name",
    "app_owner",
    "app_type",
    "patientengruppe",
    "geeignete_altersgruppen",
    "geeignete_geschlechter",
    "platform",
    "min_application_duration",
    "max_application_duration",
    "available_languages",
    "bewertungsentscheidung_des_bfarm",
    "patientengruppe_prefix",
    "patientengruppe_name"
]

columns_to_import_des = [
    "diga_id",
    "app_summary",

]

columns_to_import_kategorie = [
    "diga_id",
    "kategorie",

]
columns_to_import_score = [
    "abk",
    "name",
    "short_des",
    "short_long",
    "source"
]
columns_to_import_patient = [
    "diga_id",
    "app_name",
    "patientengruppe",
    "geeignete_altersgruppen",
    "geeignete_geschlechter",
    "patientengruppe_prefix",
    "patientengruppe_name"
]

columns_to_import_patient_werte = [
    "diga_id",
    "IG",
    "IK",
    "sum_patients",
    "drop_out_ig",
    "drop_out_ik"
]

# SQL queries to create tables in the SQLite database
create_table_query_score = '''
CREATE TABLE IF NOT EXISTS score (
    abk TEXT,
    name TEXT,
    short_des TEXT,
    short_long TEXT,
    source TEXT
)
'''

create_table_query = '''
CREATE TABLE IF NOT EXISTS diga (
    diga_id TEXT,
    app_name TEXT,
    app_owner TEXT,
    app_type TEXT,
    kategorie TEXT,
    patientengruppe TEXT,
    geeignete_altersgruppen TEXT,
    geeignete_geschlechter TEXT,
    platform TEXT,
    min_application_duration TEXT,
    max_application_duration TEXT,
    available_languages TEXT,
    bewertungsentscheidung_des_bfarm TEXT,
    patientengruppe_prefix TEXT,
    patientengruppe_name TEXT,
    diga_description TEXT
)
'''


create_table_query_patient = '''
CREATE TABLE IF NOT EXISTS patiente (
    diga_id TEXT,
    app_name TEXT,
    patientengruppe TEXT,
    geeignete_altersgruppen TEXT,
    geeignete_geschlechter TEXT,
    patientengruppe_prefix TEXT,
    patientengruppe_name TEXT,
    ig INTEGER,
    ik INTEGER,
    sum_patients INTEGER,
    drop_out_ig REAL,
    drop_out_ik REAL
)
'''
# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
# Function to transform DiGA data from an Excel file
def umformen_diga(excel_file, sheet_name):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df = df[columns_to_import]
    df['patientengruppe'] = df['patientengruppe'].apply(lambda x: ';'.join(str(x).split('\n')))
    df['geeignete_altersgruppen'] = df['geeignete_altersgruppen'].apply(lambda x: ';'.join(str(x).split('\n')))
    df['geeignete_geschlechter'] = df['geeignete_geschlechter'].apply(lambda x: ';'.join(str(x).split('\n')))
    df['available_languages'] = df['available_languages'].apply(lambda x: ';'.join(str(x).split('\n')))
    return df

# Function to transform data from an Excel file
def umformen(excel_file, sheet_name, columns_to_import):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df = df[columns_to_import]
    return df

# Function to import data into the SQLite database
def importdata(database_file, create_table_query, table_name, df):
    # Create the SQLite database and the new table
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute(create_table_query)
    conn.commit()

    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
    print("Daten erfolgreich in die SQLite-Datenbank importiert.")

# Function to update existing data in the SQLite database
def update_existing_data(database_file, df, table_name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(f'''
            UPDATE {table_name}
            SET ig = ?,
                ik = ?,
                sum_patients = ?,
                drop_out_ig = ?,
                drop_out_ik = ?
            WHERE diga_id = ?
        ''', (row['IG'], str(row['diga_id']).replace(".0","")))
        print(row['diga_id'])
        
    conn.commit()
    conn.close()
    print("Bestehende Daten erfolgreich aktualisiert.")

# Function to update the description in the SQLite database
def update_existing_data_des(database_file, df, table_name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        diga_id = str(row['diga_id'])
        if diga_id[:3] == "000":
            diga_id == row['diga_id'][3:]
        elif diga_id[:2] == "00":
            diga_id == row['diga_id'][2:]
        elif diga_id[:1] == "00":
            diga_id == row['diga_id'][1:]
        cursor.execute(f'''
            UPDATE {table_name}
            SET diga_description = ?

            WHERE diga_id = ?
        ''', (row['app_summary'], str(diga_id).replace(".0","")))
        print(diga_id)
        
    conn.commit()
    conn.close()
    print("Bestehende Daten erfolgreich aktualisiert.")

# Function to update the category in the SQLite database
def update_existing_data_des(database_file, df, table_name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        diga_id = str(row['diga_id'])
        if diga_id[:3] == "000":
            diga_id == row['diga_id'][3:]
        elif diga_id[:2] == "00":
            diga_id == row['diga_id'][2:]
        elif diga_id[:1] == "00":
            diga_id == row['diga_id'][1:]
        cursor.execute(f'''
            UPDATE {table_name}
            SET kategorie = ?

            WHERE diga_id = ?
        ''', (row['kategorie'], str(diga_id).replace(".0","")))
        print(diga_id)
        
    conn.commit() 
    conn.close()
    print("Bestehende Daten erfolgreich aktualisiert.")




# -------------------------------------------------------------------------------------------------------------------------------
# Import and create the Diga Basis table
#df_diga = umformen_diga(excel_file, sheet_name)
#importdata(database_file, create_table_query, "diga", df_diga)
# -------------------------------------------------------------------------------------------------------------------------------
# Import and create the Score table
#df_score = umformen(excel_score, sheet_name,columns_to_import_score)
#importdata(database_file, create_table_query_score, "score", df_score)
# -------------------------------------------------------------------------------------------------------------------------------
# Update the Patiente table
#df_patiente = umformen(excel_werte, sheet_name, columns_to_import_patient_werte)
#update_existing_data(database_file, df_patiente, "patiente")
# -------------------------------------------------------------------------------------------------------------------------------
# Update the Diga description table
#df_diga = umformen(excel_des, sheet_name, columns_to_import_des)
#update_existing_data_des(database_file, df_diga, "diga")
# -------------------------------------------------------------------------------------------------------------------------------

# Update the Diga category table
df_diga = umformen(excel_kategorie, sheet_name, columns_to_import_kategorie)
update_existing_data_des(database_file, df_diga, "diga")