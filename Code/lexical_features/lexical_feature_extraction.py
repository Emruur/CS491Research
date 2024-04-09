import csv
import re

# Function to read the CSV file and return a dictionary of categories and their words
def read_categories(csv_file):
    categories = {}
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            category = row[0]
            words = row[1:]
            categories[category] = words
    return categories

# Function to check if a word matches the word or stem in the category
def match_word_in_category(word, category_words):
    for category_word in category_words:
        if category_word.endswith('*'):
            stem = category_word[:-1]
            if word.lower().startswith(stem.lower()):
                return True
        elif word.lower() == category_word.lower():
            return True
    return False

# Function to count occurrences of words from each category in the given text
def count_words_in_text(text, categories):
    word_counts = {category: 0 for category in categories}
    words = re.findall(r'\b\w+(?:\'\w+)?\b', text)  # Tokenize the text preserving contractions
    for word in words:
        for category, category_words in categories.items():
            if match_word_in_category(word, category_words):
                word_counts[category] += 1
    return word_counts

# Function to process texts from input CSV file and write results to output CSV file
def process_texts(input_csv_file, output_csv_file, categories):
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['Text ID'] + list(categories.keys()))  # Header row
        for row in reader:
            text_id, text = row
            print("Processing text with id: ", text_id)
            word_counts = count_words_in_text(text, categories)
            writer.writerow([text_id] + list(word_counts.values()))

# Path to your CSV file containing categories and words
csv_file_path = "liwc2007.csv"
# Path to your input CSV file containing text IDs and text
input_csv_file_path = "interviewee_answers.csv"
# Path to the output CSV file to write the results
output_csv_file_path = "output_results.csv"

# Read categories from the CSV file
categories = read_categories(csv_file_path)

# Process texts from the input CSV file and write results to the output CSV file
process_texts(input_csv_file_path, output_csv_file_path, categories)

print("Processing complete. Results written to", output_csv_file_path)
