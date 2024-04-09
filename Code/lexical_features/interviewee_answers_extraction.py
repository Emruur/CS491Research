import csv

def extract_interviewee_answers(csv_file, output_file):
    interviewee_answers = []

    with open(csv_file, 'r', encoding='cp1252') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            interview_number = row[0].split(",")[0]
            interviewee_answer = ""
            for item in row[1:]:
                if item.startswith('Interviewee:'):
                    interviewee_answer += item.split(':')[1].strip() + " "
            interviewee_answers.append([interview_number, interviewee_answer.strip()])

    # Write interviewee answers to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for answer in interviewee_answers:
            writer.writerow(answer)

# Example usage
input_csv_file = 'interview_transcripts_by_turkers.csv'  # Update with your CSV file path
output_csv_file = 'interviewee_answers.csv'  # Path for the new CSV file
extract_interviewee_answers(input_csv_file, output_csv_file)
print(f"Interviewee answers have been written to '{output_csv_file}'.")
