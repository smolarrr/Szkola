import re
import csv

def parse_time(time_str):
    hours = minutes = seconds = 0
    match = re.match(r'(?:(\d+)\s*godz\.\s*)?(?:(\d+)\s*min\s*)?(?:(\d+)\s*s)?', time_str)
    if match:
        if match.group(1):
            hours = int(match.group(1))
        if match.group(2):
            minutes = int(match.group(2))
        if match.group(3):
            seconds = int(match.group(3))
    total_minutes = hours * 60 + minutes + seconds / 60
    return total_minutes

def clean_name(name):
    name = re.sub(r'\s*\(.*?\)', '', name).strip()
    parts = name.split()
    if not parts:
        first_name = ''
        surname = ''
    elif len(parts) == 1:
        first_name = ''
        surname = parts[0]
    else:
        first_name = ' '.join(parts[:-1])
        surname = parts[-1]
    return first_name, surname

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-16') as file:
        lines = file.readlines()

    participants = []
    data_section = False
    headers = []

    for line in lines:
        line = line.strip()
        if line.startswith('2. Uczestnicy'):
            data_section = True
            continue
        elif line.startswith('3. Działania podczas spotkania'):
            data_section = False
            break

        if data_section:
            if not headers and 'Imię i nazwisko' in line:
                headers = line.split('\t')
                headers = [header.strip() for header in headers]
                continue
            elif headers:
                if not line or not any(field.strip() for field in line.split('\t')):
                    continue
                fields = line.split('\t')
                while len(fields) < len(headers):
                    fields.append('')
                participant = dict(zip(headers, fields))

                if ('Imię i nazwisko' in participant and participant['Imię i nazwisko'].strip() and
                    'Czas udziału w spotkaniu' in participant and participant['Czas udziału w spotkaniu'].strip()):
                    first_name, surname = clean_name(participant['Imię i nazwisko'])
                    total_minutes = parse_time(participant['Czas udziału w spotkaniu'])
                    eligible = total_minutes >= 60

                    participant['Imię'] = first_name
                    participant['Nazwisko'] = surname
                    participant['Łączny czas (min)'] = round(total_minutes, 2)
                    participant['Kwalifikacja'] = 'Tak' if eligible else 'Nie'

                    participants.append(participant)
                else:
                    print(f"Warning: Skipping line due to missing data: {line}")
                    continue

    participants.sort(key=lambda x: x['Nazwisko'])
    output_headers = ['Nazwisko', 'Imię', 'Kwalifikacja', 'Łączny czas (min)']

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output_headers)
        writer.writeheader()
        for participant in participants:
            row = {key: participant.get(key, '') for key in output_headers}
            writer.writerow(row)

input_file = '5TP_Zadanie programistyczne pod INF.04 - Raport obecności 6-09-24 (5TP).csv'
output_file = '5TP_Zadanie-INF04.csv'
process_file(input_file, output_file)