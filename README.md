
# DiGA and Study Data Extraction and Processing

This repository contains scripts for extracting, processing, and crawling data related to DiGA (Digitale Gesundheitsanwendung) and study data. The scripts are:

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/suriija/digaCrawler.git
    cd diga-study-data-extraction
    ```

2. Install the required dependencies:
    ```bash
    pip install pandas  
	pip install sqlite3
	pip install selenium 
	pip install pandas
	pip install sqlite
	pip install webdriver-manager
    ```

## Usage

### study_data_extraction_and_transformation.py

This script is used for extracting and transforming study data from Excel files.

1. Ensure your Excel files are named and formatted correctly.
2. Modify the `excel_file_path` and `sheet_name` variables in the script to match your file and sheet names.
3. Run the script:
    ```bash
    python study_data_extraction_and_transformation.py
    ```

### diga_data_extraction_and_processing.py

This script is used for extracting and processing DiGA data and importing it into an SQLite database.

1. Ensure your Excel files are named and formatted correctly.
2. Modify the `excel_file`, `sheet_name`, `database_file`, and other relevant variables in the script to match your files and database.
3. Run the script:
    ```bash
    python diga_data_extraction_and_processing.py
    ```

### Crawling-selenium-version2.ipynb

This script is designed to scrape information from a DiGA (Digitale Gesundheitsanwendung) website using Selenium. It extracts data related to various health apps and their details.

#### Overview

The script navigates through the DiGA website, retrieves essential app information, and extracts answers to specific questions about each app.

#### Requirements

- Python 3.x
- Selenium
- pandas
- webdriver_manager
- Jupyter Notebook

You can install the required packages using the following commands:
```bash
pip install selenium 
pip install pandas
pip install sqlite
pip install webdriver-manager
```

#### Chrome and ChromeDriver Issues

The Chrome and Chromedriver versions have to be compatible for Selenium to operate without errors. You need to find a driver version in `latest_release_url`, which is available at 'https://github.com/GoogleChromeLabs/chrome-for-testing#json-api-endpoints', that is compatible with your current Chrome version, then specify the `latest_release_url` and `driver_version` parameters in:
```python
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(
    latest_release_url='https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json',
    driver_version='124.0.6367.91').install()), options=options)
```
Here, the driver version chosen is 124.0.6367.91.


#### How to Run in Jupyter Notebook

1. Download the Jupyter Notebook file to your local machine.
2. Open the notebook using Jupyter Notebook or Jupyter Lab.
3. Run each cell in the notebook sequentially. You can do this by clicking the "Run" button or using the shortcut Shift + Enter.
4. The notebook will extract information from the DiGA website and display the results in the output of the respective cells. The extracted data will also be saved as a DataFrame in a CSV file.


## Database Schema

The SQLite database contains the following tables: