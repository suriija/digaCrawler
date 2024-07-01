import regex as re
import pandas as pd
import csv

# List of abbreviations
abbreviation_list = [
    ["1-Minute Sit-to-Stand Test", "1-MSTS"],
    ["COPD Assessment Test", "CAT"],
    ["Chronic respiratory disease questionnaire", "CRQ"],
    ["Veterans RAND 12 Item Health Survey", "VR-12"],
    ["Endometriosis Health Profile-5", "EHP-5"],
    ["Fatigue Severity Scale", "FSS"],
    ["Fragebogen zur Erfassung der schmerzspezifischen Selbstwirksamkeit", "FESS"],
    ["Pain Disability Index", "PDI"],
    ["Depression Anxiety and Stress Scale-21", "DASS-21"],
    ["International Index of Erectile Function-5", "IIEF-5"],
    ["Quality of Life Measure for Men with Erection Difficulties", "QoL-Med"],
    ["Patient Activation Measure-13", "PAM-13"],
    ["International Prostate Symptom Score", "IPSS"],
    ["Overactive Bladder Questionnaire Short Form", "OAB-q SF"],
    ["6-Minute-Walk-Test", "6MWT"],
    ["Kansas City Cardiomyopathy Questionnaire", "KCCQ"],
    ["9-item European Heart Failure Self-care Behaviour Scale", "9-EHFScBS"],
    ["Atlanta Heart Failure Knowledge Test", "AHFKT"],
    ["New-York-Heart-Association-Klassifikation", "NYHA-Klassifikation"],
    ["European Quality of Life 5 Dimensions 5 Level Version", "EQ-5D-5L"],
    ["Shared Decision-Making Questionnaire-9", "SDM-Q-9"],
    ["Short Form 12 Health Survey", "SF-12"],
    ["Morisky Medication Adherence Scale, 8 items", "MMAS-8"],
    ["WHO-5-Wohlbefindens-Index", "WHO-5"],
    ["WHOQOL-BREF", "WHOQOL-BREF"],
    ["HbA1c-Wert", "HbA1c"],
    ["Summary of Diabetes Self-care Activities Measure", "SDSCA"],
    ["Problem Areas in Diabetes Scale", "PAID"],
    ["Allgemeiner Selbstwirksamkeit Kurzskala", "ASKU"],
    ["International Physical Activity Questionnaire-Short Form", "IPAQ-SF"],
    ["Resilienzskala-13", "RS-13"],
    ["European Health Literacy Survey Questionnaire-16", "HLS-EU-Q16"],
    ["EORTC Core Quality of Life Questionnaire", "EORTC-QLQ-C30"],
    ["Functional Assessment of Chronic Illness Therapy-Fatigue", "FACIT-F-Score"],
    ["Brief Fatigue Inventory", "BFI"],
    ["Functional Assessment of Cancer Therapy-General", "FACT-G-Score"],
    ["Hospital Anxiety and Depression Scale", "HADS"],
    ["National Comprehensive Cancer Network Distress Thermometer", "NCCN-DT"],
    ["Assessment of Quality of Life-8D", "AQoL-8D"],
    ["Numerical Pain Rating Scale", "NPRS"],
    ["Kujala Score", "Kujala"],
    ["West Haven-Yale Multidimensional Pain Inventory", "MPI"],
    ["Knee injury and Osteoarthritis Outcome Score", "KOOS"],
    ["Brief Pain Inventory", "BPI"],
    ["Fragebogen zur Erfassung der Schmerzverarbeitung", "FESV"],
    ["Chronic Pain Acceptance Questionnaire", "CPAQ"],
    ["Pain Self-Efficacy Questionnaire", "PSEQ"],
    ["Visuelle Analogskala", "VAS"],
    ["Chalder Fatigue Scale", "Chalder"],
    ["Insomnia Severity Index", "ISI"],
    ["Hamburg Quality of Life Questionnaire for Multiple Sclerosis", "HALEMS"],
    ["Frenchay Activities Index", "Frenchay"],
    ["Health Literacy Questionnaire", "HLQ"],
    ["Cognitive Failure Questionnaire", "CFQ"],
    ["Health-49", "Health-49"],
    ["Neurological Assessment Battery", "NAB"],
    ["Tinnitusfragebogen nach Göbel und Hiller", "Tinnitusfragebogen"],
    ["Mini-Tinnitus-Fragebogen", "Mini-TF-12"],
    ["Bochumer Veränderungsbogen 2000", "BVB-2000"],
    ["Depression Literacy Questionnaire", "D-Lit"],
    ["World Health Organization Quality Of Life", "WHOQOL-BREF"],
    ["Brief Illness Perception Questionnaire", "B-IPQ"],
    ["Generalized Anxiety Disorder 7-item scale", "GAD-7"],
    ["Beck Depression Inventory-II", "BDI-II"],
    ["Hamilton Anxiety Scale", "HAM-A"],
    ["Agoraphobic Cognitions Questionnaire", "ACQ"],
    ["Body Sensations Questionnaire", "BSQ"],
    ["Primary Endpoint Questionnaire", "PEQ"],
    ["Beck Anxiety Inventory", "BAI"],
    ["Liebowitz Social Anxiety Scale", "LSAS"],
    ["Sheehan-Disability-Skala", "SDS"],
    ["Angst-Kontroll-Fragebogen", "AKF"],
    ["Allgemeinen Depressionsskala", "ADS"],
    ["7-Tage-Punktprävalenz, selbstberichtet", "selbstberichtete Rauchabstinenzquote"],
    ["Cotinin-Test", "objektiven sekundären Endpunkt"],
    ["Cotinin-Test", "selbstberichtete Abstinenzquote"],
    ["Short Form-36", "SF-36"],
    ["Maslach Burnout Inventory", "MBI-EE"]
]

# Function to extract abbreviations from a text
def extract_abbreviations(text): 
    pattern = r'\b(?:' + '|'.join(map(re.escape, [abbr[1] for abbr in abbreviation_list])) + r')\b'
    matches = re.findall(pattern, text)
    return matches

# Function to find sentences with brackets and semicolons
def find_sentences_with_brackets(text):
    pattern = re.compile(r'[^.]*[\(\[][^)\]]*;[^)\]]*[\)\]][^.]*[.!?]', re.MULTILINE)
    matches = pattern.findall(text)
    return matches

# Function to find sentences with brackets with special characters
def find_sentences_with_brackets_and_special_chars(text):
    pattern = re.compile(r'[^.]*[\(\[][^)\]]*[^a-zA-Z0-9\s][^)\]]*[\)\]][^.!?]*[.!?]', re.MULTILINE)
    matches = pattern.findall(text)
    return matches


# Function to extract IG and KG values from a text
def extract_ig_kg_values(text):
    # Pattern for Drop-out values
    if "Drop-out" in text:
        pattern = re.compile(r'\(IG:\s*([\d,.]+\s*%)?;\s*KG:\s*([\d,.]+\s*%)?\)')
        matches = pattern.findall(text)
        values = []
        if matches:
            for match in matches:
                if match[0] and match[1]:
                    values.append((match[0], match[1]))
            return ["Drop-out IG und IK", values]
        else:
            return [] 
    else: 
        pattern = re.compile(r'\(IG[:\s]*([\d,.%]+)[;\s]+KG[:\s]*([\d,.%]+)\)|\(?([\d,.%]+)\s*IG[;\s]+([\d,.%]+)\s*KG\)?') 
        matches = pattern.findall(text)
        if matches:
            if "ingesamt" in text or "eingeschlossen" in text or "randomisiert" in text or "umfasste" in text:
                values = []
                for match in matches:
                    if match[0] and match[1]:
                        values.append((match[0], match[1]))
                    elif match[2] and match[3]:
                        values.append((match[2], match[3]))
                return ["IG und IK", values]
            else: 
                return []

# Function to extract results from a text
def extract_results(text):
    results = []
    sentences = find_sentences_with_brackets(text)
    for abbr in abbreviation_list:
        for sentence in sentences:
            if abbr[1] in sentence:
                pattern = re.compile(r'\s*[\(\[]([^()\[\]]*)[\)\]]')
                matches = pattern.findall(sentence)
                for match in matches:
                    if len(match) > 3 and match.count(",") > 1:
                        results.append([abbr[1], match, text])
    return results

# Function to count occurrences of abbreviations in a text
def count_abbreviation_occurrences(text):
    results = []
    for abbr in abbreviation_list:
        if abbr[1] in text:
            results.append([abbr[1], text.count(abbr[1]), text])
    return results

# List of keywords to be removed
delete_keywords = [
    "SE", "ARR", "RCT", "KI", "ITT-Population", "95-%-KI", "OR", "NNT", 
    "ß-norm", "MBI-EE", "ADS", "MD"
]

# List of keywords for result selection
keywords_for_results = [
    "adjustierte", "adjustierte Differenz", "p", "Mittelwertsdifferenz", "MWD",
    "Differenz", "adjustierte Mittelwertsdifferenz (MWD)", "Veränderung",
    "Insomnie Schweregrad Index", "Cohen"
]

# Function to clean the text by removing certain keywords
def clean_text(text):
    result = text
    for keyword in delete_keywords:
        result = result.replace("[" + keyword + "]", "&" + keyword + "&").replace("(" + keyword + ")", "&" + keyword + "&")
    return result.replace("(KI", "KI&")

# Function to find matching brackets in the text
def find_matching_brackets(text):
    stack = []
    results = []
    i = 0
    while i < len(text):
        if text[i] == '(' or text[i] == '[':
            stack.append((text[i], i))
        elif text[i] == ')' or text[i] == ']':
            if stack:
                start_char, start_idx = stack.pop()
                if (start_char == '(' and text[i] == ')') or (start_char == '[' and text[i] == ']'):
                    content = text[start_idx:i+1]
                    if any(keyword in content for keyword in keywords_for_results) and ';' in content:
                        results.append(content)
        i += 1
    if not results:
        stack = []
        results = []
        i = 0
        while i < len(text):
            if text[i] == '(' or text[i] == '[':
                stack.append((text[i], i))
            elif text[i] == ')' or text[i] == ']':
                if stack:
                    start_char, start_idx = stack.pop()
                    if (start_char == '(' and text[i] == ')') or (start_char == '[' and text[i] == ']'):
                        content = text[start_idx:i+1]
                        if any(keyword in content for keyword in [abbr[1] for abbr in abbreviation_list]) and ';' in content:
                            results.append(content)
            i += 1
    return results

# Function to process the texts and extract the results
def process_texts(texts):
    results = []
    for text in texts:
        abbreviations = extract_abbreviations(text[2])
        matching_brackets = find_matching_brackets(clean_text(text[2]))
        if matching_brackets:
            results.append([matching_brackets])
        else:
            pattern = r'(\[.*?\]|\(.*?\))'
            matches = re.findall(pattern, clean_text(text[2]))
            if matches:
                for match in matches:
                    if re.search(r'(Mittelwertsdifferenz|adjustierte Differenz|b:|Standardfehler|Differenz|MWD)', match):
                        results.append([match])
        combined_results = [[a, b] for a, b in zip(abbreviations, results)]
    return combined_results

# Main function to read the CSV file and extract the data
def main():
    input_file_path = "F_diga_verzeichnis_2024_06_02.csv"
    output_file_path_csv = "Liste.csv"
    output_file_path_excel = "Liste.xlsx"
    
    data = []
    with open(input_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';', lineterminator='\n')
        for row in reader:
            record = {}
            bfarm = row[49]
            record["diga_id"] = row[0]
            record["app_type"] = row[5]
            record["app_name"] = row[3]

            sentences_with_brackets = find_sentences_with_brackets(bfarm)

            if sentences_with_brackets:
                count = 0
                result_count = 0
                for sentence in sentences_with_brackets:
                    count += 1
                    ig_kg_values = extract_ig_kg_values(sentence)
                    abbreviation_counts = count_abbreviation_occurrences(sentence)
                    
                    if abbreviation_counts:
                        result_count += 1
                        #record["results_with_abbr_" + str(result_count)] = abbreviation_counts
                        record["attern such " + str(result_count)] = process_texts(abbreviation_counts)

                    if ig_kg_values:
                        record[ig_kg_values[0]] = ig_kg_values[1]
                    #record["sentence_with_brackets_" + str(count)] = sentence
            else:
                sentences_with_brackets_and_special_chars = find_sentences_with_brackets_and_special_chars(bfarm)
                count = 0
                result_count = 0
                for sentence in sentences_with_brackets_and_special_chars:
                    count += 1
                    #record["sentence_with_special_chars_" + str(count)] = sentence
                    abbreviation_counts = count_abbreviation_occurrences(sentence)
                    if abbreviation_counts:
                        result_count += 1
                        #record["results_with_abbr_" + str(result_count)] = abbreviation_counts
                        record["pattern such " + str(result_count)] = process_texts(abbreviation_counts)
                    ig_kg_values = extract_ig_kg_values(sentence)
                    if ig_kg_values:
                        record[ig_kg_values[0]] = ig_kg_values[1]

            record["bewertungsentscheidung"] = bfarm
            data.append(record)
    
    df = pd.DataFrame(data)
    df.to_csv(output_file_path_csv, encoding='utf-8-sig', index=False, sep=';')
    df.to_excel(output_file_path_excel, index=False)

if __name__ == "__main__":
    main()
