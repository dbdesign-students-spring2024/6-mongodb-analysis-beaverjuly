# AirBnB MongoDB Analysis

A little assignment to practice importing and analyzing data within a MongoDB database.

# Scrubbing

1. **Parse and Add New Columns:**
   - I defined a `parse_name` function that uses a regular expression to extract specific information from the `name` column:
     ```python
     def parse_name(name):
         pattern = r"(.+?) · .*?(\d+)? bedroom.*? · (\d+)? bed.*? · (\d+(?:\.\d+)?)? bath"
         match = re.search(pattern, name)
         ...
     ```
   - This function is applied to each row's `name` field, extracting details and adding them as new columns to each row:
     ```python
     row.update(dict(zip(['unit_type', 'num_bedroom', 'num_bed', 'num_bath'], parse_name(row['name']))))
     ```

2. **Delete Columns That Are Unlikely to Be Used in Subsequent Data Manipulation:**
   - I identified columns to remove based on explicit names and substrings (`url`, `about`):
     ```python
     columns_to_remove = ['name', 'description', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds', 'amenities'] + \
                         [col for col in reader.fieldnames if should_remove_column(col)]
     ```
   - It then removes these columns from each row:
     ```python
     for column in columns_to_remove:
         row.pop(column, None)
     ```

3. **Dealing with N/A Values:**
   - I also checked each value in a row and replaced empty strings or `'N/A'` with `None`:
     ```python
     for key, value in row.items():
         if value == '' or value == 'N/A':
             row[key] = None
     ```

4. **Creating and Writing to a New CSV File:**
   - After processing, I wrote the cleaned data into a new CSV file, ready for MongoDB import:
     ```python
     with open(output_file_path, mode='w', encoding='utf-8', newline='') as csvfile:
         writer = csv.DictWriter(csvfile, fieldnames=output_fieldnames)
         writer.writeheader()
         writer.writerows(parsed_data)
     ```