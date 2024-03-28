import csv
import re

input_file_path = "data/listings.csv"
output_file_path = "data/listings_clean.csv"

def parse_name(name):
    pattern = r"(.+?) · .*?(\d+) bedroom.*? · (\d+) bed.*? · (\d+(?:\.\d+)?) bath"
    match = re.search(pattern, name)
    if match:
        unit_type = match.group(1).replace(' in Berlin', '')  # Remove ' in Berlin' from the unit type
        return unit_type, match.group(2), match.group(3), match.group(4)
    return None, None, None, None

#Remove columns containing urls and full sentence descriptions
def should_remove_column(column_name):
    lower_col = column_name.lower()
    return 'url' in lower_col or 'about' in lower_col or 'overview' in lower_col


parsed_data = []

# Open the input CSV file for reading
with open(input_file_path, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # List of columns to remove, including those with 'url' or 'about' in their names
    columns_to_remove = ['name', 'description', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'license'] + \
                        [col for col in reader.fieldnames if should_remove_column(col)]

    for row in reader:
        unit_type, num_bedroom, num_bed, num_bath = parse_name(row['name'])
        row.update({'unit_type': unit_type, 'num_bedroom': num_bedroom, 'num_bed': num_bed, 'num_bath': num_bath})
        
        # Remove the specified columns
        for column in columns_to_remove:
            row.pop(column, None)

        # Replace with None so that these values to null in MongoDB
        for key, value in row.items():
            if value == '' or value == 'N/A':
                row[key] = None 

        parsed_data.append(row)

output_fieldnames = [col for col in parsed_data[0].keys()]

# Open a new CSV file for writing the results
with open(output_file_path, mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output_fieldnames)
    writer.writeheader()
    writer.writerows(parsed_data)



