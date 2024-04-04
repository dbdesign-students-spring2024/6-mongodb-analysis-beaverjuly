# AirBnB MongoDB Analysis

A little assignment to practice importing and analyzing data within a MongoDB database.

# Data set details
## 1. Show original Dataset

| id | listing_url | scrape_id | last_scraped | source | name | description | neighborhood_overview | picture_url | host_id | host_url | host_name | host_since | host_location | host_about | host_response_time | host_response_rate | host_acceptance_rate | host_is_superhost | host_thumbnail_url | host_picture_url | host_neighbourhood | host_listings_count | host_total_listings_count | host_verifications | host_has_profile_pic | host_identity_verified | neighbourhood | neighbourhood_cleansed | neighbourhood_group_cleansed | latitude | longitude | property_type | room_type | accommodates | bathrooms | bathrooms_text | bedrooms | beds | amenities | price | minimum_nights | maximum_nights | minimum_minimum_nights | maximum_minimum_nights | minimum_maximum_nights | maximum_maximum_nights | minimum_nights_avg_ntm | maximum_nights_avg_ntm | calendar_updated | has_availability | availability_30 | availability_60 | availability_90 | availability_365 | calendar_last_scraped | number_of_reviews | number_of_reviews_ltm | number_of_reviews_l30d | first_review | last_review | review_scores_rating | review_scores_accuracy | review_scores_cleanliness | review_scores_checkin | review_scores_communication | review_scores_location | review_scores_value | license | instant_bookable | calculated_host_listings_count | calculated_host_listings_count_entire_homes | calculated_host_listings_count_private_rooms | calculated_host_listings_count_shared_rooms | reviews_per_month |
|----|-------------|-----------|--------------|--------|------|-------------|-----------------------|-------------|---------|----------|-----------|------------|---------------|------------|--------------------|-------------------|----------------------|------------------|-------------------|------------------|--------------------|--------------------|-------------------------|-------------------|----------------------|-----------------------|----------------|-----------------------|------------------------------|----------|-----------|---------------|-----------|--------------|-----------|----------------|----------|------|-----------|-------|----------------|---------------|-----------------------|-------------------------|-----------------------|-------------------------|----------------------|----------------------|----------------|-----------------|----------------|----------------|----------------|----------------|---------------------|------------------|---------------------|----------------------|--------------|------------|---------------------|----------------------|-------------------------|---------------------|-----------------------------|-----------------------|----------------------|---------|-----------------|------------------------------|--------------------------------------------|---------------------------------------|---------------------------------------|------------------|
| 3176 | https://www.airbnb.com/rooms/3176 | 20231218233220 | 2023-12-19 | previous scrape | Rental unit in Berlin · ★4.63 · 1 bedroom · 2 beds · 1 bath |  | "The neighbourhood is famous for its variety of international eateries, pubs, restaurants, cafés, galleries and little shops.<br />The bakery next door is open everyday from up 7 am, which makes warm croissants for breakfast very tempting.<br /><br />On Sundays don't miss the traditional flea markets on Arkonaplatz and in the nearby Mauerpark for special treats and souvenirs. <br /><br /><br />check out our  travel guide and please let us know what your highlights were so we can add them for future guests" | https://a0.muscache.com/pictures/243355/84afcff6_original.jpg | 3718 | https://www.airbnb.com/users/show/3718 | Britta | 2008-10-19 | "Coledale, Australia" | "We love to travel ourselves a lot and prefer to stay in apartments. Especially since we had a baby . " | within a day | 100% | 17% | f | https://a0.muscache.com/im/users/3718/profile_pic/1267053077/original.jpg?aki_policy=profile_small | https://a0.muscache.com/im/users/3718/profile_pic/1267053077/original.jpg?aki_policy=profile_x_medium | Prenzlauer Berg | 1 | 1 | "['email', 'phone']" | t | t | "Berlin, Germany" | Prenzlauer Berg Südwest | Pankow | 52.53471 | 13.4181 | Entire rental unit | Entire home/apt | 4 |  | 1 bath |  | 2 | [] | $83.00 | 63 | 184 | 63 | 63 | 184 | 184 | 63.0 | 184.0 |  | t | 0 | 0 | 0 | 15 | 2023-12-19 | 148 | 1 | 0 | 2009-06-20 | 2023-05-25 | 4.63 | 4.67 | 4.52 | 4.64 | 4.69 | 4.92 | 4.62 | "First name and Last name: Nicolas Krotz <br/> Contact address: bouchestr. , 12435, berlin, berlin <br/>Listing address: Bouchestr. , 12435, Berlin , Germany " | f | 1 | 1 | 0 | 0 | 0.84 |

## Note
Due to the length of each line of data, I'm only showing one row here.

## 2. Description of problems
1. Missing data is being represented by both empty cells and "NA" strings; this can be misinterpreted during data analysis

2. Include columns that contain redundant information

3. Include columns that contain data that will not be analyzed but significantly slows down my laptop due to its huge length, such as complete sentences of reviews

# Scrubbing

1. **Parse and Add New Columns:**
   - The original column `name` includes multiple values that are redundant, so i intend to parse it into new columns.
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
   - Some columns contain urls and full sentence descriptions that are not likely to be analyzed subsequently.
   - I identified columns to remove based on substrings (`url`, `about`, `overview`):
    ```python
    def should_remove_column(column_name):
    lower_col = column_name.lower()
    return 'url' in lower_col or 'about' in lower_col or 'overview' in lower_col
    ```
    - Others contain information that overlapps with other columns, so I deleted them based on explicit names: 
     ```python
    columns_to_remove = ['name', 'description', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'license'] + \
                        [col for col in reader.fieldnames if should_remove_column(col)]
     ```
   - Then remove these columns from each row:
     ```python
     for column in columns_to_remove:
         row.pop(column, None)
     ```

3. **Dealing with N/A Values:**
   - I also checked each value in a row and replaced empty cells or cells containing the `N/A`string with `None`, to avoid confusing them with actual values later on during anaysis:
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

# Mongo Shell Queries

## 1. Retrieve the first two documents from the `listings` collection.

   ```mongodb
   db.listings.find().limit(2)
   ```

## 2. Retrieve the first ten documents from the `listings` collection in a readable format using `pretty()`.

   ```mongodb
   db.listings.find().limit(10).pretty()
   ```
### Result
One of the document being returned (It appears that the results in my Mongo Shell are formatted with or without the “pretty()” command.).

```json
[
  {
    "_id": ObjectId("6605db3b6a8dda9c913f7725"),
    "id": 9991,
    "scrape_id": Long("20231218233220"),
    "last_scraped": "2023-12-19",
    "source": "city scrape",
    "host_id": 33852,
    "host_name": "Philipp",
    "host_since": "2009-08-25",
    "host_location": "Berlin, Germany",
    "host_response_time": "within a day",
    "host_response_rate": "100%",
    "host_acceptance_rate": "",
    "host_is_superhost": "f",
    "host_neighbourhood": "Prenzlauer Berg",
    "host_listings_count": 1,
    "host_total_listings_count": 1,
    "host_verifications": "['email', 'phone']",
    "host_has_profile_pic": "t",
    "host_identity_verified": "t",
    "neighbourhood": "Berlin, Germany",
    "neighbourhood_cleansed": "Prenzlauer Berg Südwest",
    "neighbourhood_group_cleansed": "Pankow",
    "latitude": 52.53269,
    "longitude": 13.41805,
    "property_type": "Entire rental unit",
    "room_type": "Entire home/apt",
    "accommodates": 7,
    "price": "$180.00",
    "minimum_nights": 6,
    "maximum_nights": 14,
    "minimum_minimum_nights": 6,
    "maximum_minimum_nights": 6,
    "minimum_maximum_nights": 14,
    "maximum_maximum_nights": 14,
    "minimum_nights_avg_ntm": 6,
    "maximum_nights_avg_ntm": 14,
    "calendar_updated": "",
    "has_availability": "t",
    "availability_30": 0,
    "availability_60": 0,
    "availability_90": 0,
    "availability_365": 47,
    "calendar_last_scraped": "2023-12-19",
    "number_of_reviews": 7,
    "number_of_reviews_ltm": 0,
    "number_of_reviews_l30d": 0,
    "first_review": "2015-08-09",
    "last_review": "2020-01-04",
    "review_scores_rating": 5,
    "review_scores_accuracy": 5,
    "review_scores_cleanliness": 5,
    "review_scores_checkin": 5,
    "review_scores_communication": 5,
    "review_scores_location": 4.86,
    "review_scores_value": 4.86,
    "instant_bookable": "f",
    "calculated_host_listings_count": 1,
    "calculated_host_listings_count_entire_homes": 1,
    "calculated_host_listings_count_private_rooms": 0,
    "calculated_host_listings_count_shared_rooms": 0,
    "reviews_per_month": 0.07,
    "unit_type": "Rental unit",
    "num_bedroom": 4,
    "num_bed": 7,
    "num_bath": 2.5
  }
  // Additional documents follow the same structure...
]
```
## 3. Retrieve all listings from two specific superhosts, showing only selected fields.

   ```mongodb
   db.listings.find(
     { 
       $or: [
         {host_id: 956350, host_is_superhost: 't'}, 
         {host_id: 163384, host_is_superhost: 't'}
       ] 
     }, 
     {
       name: 1, 
       price: 1, 
       neighbourhood: 1, 
       host_name: 1, 
       host_is_superhost: 1
     }
   )
   ```
**Results:**

```json
[
  {
    "_id": ObjectId("6605db3b6a8dda9c913f7760"),
    "host_name": "Arne",
    "host_is_superhost": "t",
    "neighbourhood": "Berlin, Germany",
    "price": "$51.00"
  },
  {
    "_id": ObjectId("6605db3b6a8dda9c913f7761"),
    "host_name": "Alan & Kasia StayBearlin",
    "host_is_superhost": "t",
    "neighbourhood": "Berlin, Germany",
    "price": "$83.00"
  },
  {
    "_id": ObjectId("6605db3b6a8dda9c913f77e1"),
    "host_name": "Alan & Kasia StayBearlin",
    "host_is_superhost": "t",
    "neighbourhood": "Berlin, Germany",
    "price": "$86.00"
  },
]
```
## 4. Find all unique `host_name` values in the `listings` collection.

   ```mongodb
   db.listings.distinct("host_name")
   ```
### Results
```json
[
  "",
  "1a Apartment",
  "A",
  "A&H",
  "A.",
  "Aaron",
  "Abby",
  "Abdallah",
  "Abdel",
  "Abdullah",
  "Abe",
  "Abed",
  "Abhishek",
  "Abi",
  "Abie",
  "Abigail",
  "Abudi",
  "Achim",
  "Acora Berlin Living The City",
  "Ada",
  "Adam",
  "Adania",
  "Addison",
  "Ade",
  "Adediran",
  "Adele",
  "Adelina",
  "Adeline",
  "Adi",
  "Adiam",
  "Adnan",
  "Adnis",
  "Adriaan",
  "Adrian",
  "Adrian + Uli + Leeloo",
  "Adriana",
  "Adrianna",
  "Adriano",
  "Adrienne",
  "Adrián",
  "Adryan",
  "Agata",
  "Agathe",
  "Aggi",
  "Aglaja",
  "Agnes",
  "Agnessa",
  "Agnieszka",
  "Agung And Indri",
  "Agustin",
  "Aharon",
  "Ahmad",
  "Ahmed",
  "Ahmed & Fatima",
  "Ahmed M.",
  "Aida",
  "Aigulia",
  "Aiko",
  "Aileen",
  "Ailon+Naama",
  "Aina",
  "Aisha",
  "Aishah A",
  "Aisling",
  "Aj",
  "Akintokunb",
  "Akiva",
  "Akribis",
  "Akwasi",
  "Al",
  "Alaa",
  "Alain",
  "Alan",
  "Alan & Kasia StayBearlin",
  "Alana",
  "Alban",
  "Albert",
  "Alberto",
  "Albrecht",
  "Aldona",
  "Ale & Ana",
  "Alejandra",
  "Alejandro",
  "Aleks",
  "Aleksan",
  "Aleksandra",
  "Alena",
  "Alessa",
  "Alessandra",
  "Alessandro",
  "Alessia",
  "Alessio",
  "Alex",
  "Alexa",
  "Alexander",
  "Alexander W F",
  "Alexandr",
  "Alexandra",
  "Alexandre",
  "Alexandros",
  ... 3654 more items
]
```
## 5. Find all places with more than 2 beds in a neighborhood, order by`review_scores_rating` descending
I additionally excluded listings with missing review scores, otherwise these would be presented at the top of the descending list.
   ```mongodb
   db.listings.find({ review_scores_rating: { $exists: true, $ne: null, $ne: '' } })
              .sort({ review_scores_rating: -1 })
```
## Result
```json
[
  {
    "_id": ObjectId("6605db3b6a8dda9c913f78cc"),
    "price": "",
    "review_scores_rating": 5
  },
  {
    "_id": ObjectId("6605db3b6a8dda9c913f7ab4"),
    "price": "$150.00",
    "review_scores_rating": 5
  },
  {
    "_id": ObjectId("6605db446a8dda9c913f863c"),
    "price": "$55.00",
    "review_scores_rating": 5
  },
  {
    "_id": ObjectId("6605db516a8dda9c913f9b7a"),
    "price": "$122.00",
    "review_scores_rating": 5
  },
  {
    "_id": ObjectId("6605db3b6a8dda9c913f7947"),
    "price": "$275.00",
    "review_scores_rating": 4.96
  },
  {
    "_id": ObjectId("6605db3b6a8dda9c913f779b"),
    "price": "$200.00",
    "review_scores_rating": 4.88
  },
  {
    "_id": ObjectId("6605db3e6a8dda9c913f7c53"),
    "price": "$129.00",
    "review_scores_rating": 4.86
  },
  {
    "_id": ObjectId("6605db446a8dda9c913f85f3"),
    "price": "$170.00",
    "review_scores_rating": 4.86
  }
]
Type "it" for more
```
## 6. Aggregate listings to count the number of listings each host has.

  I utilized MongoDB's aggregation framework to group documents in the `listings` collection by `host_id` and count the number of listings each host has.

   ```mongodb
   db.listings.aggregate([
     { $group: { _id: "$host_id", count: { $sum: 1 } } }
   ])
   ```
## Result
```json
[
  { _id: 354783560, count: 3 },
  { _id: 15442470, count: 1 },
  { _id: 26244469, count: 1 },
  { _id: 22749471, count: 1 },
  { _id: 10141438, count: 1 },
  { _id: 38239738, count: 1 },
  { _id: 24536724, count: 1 },
  { _id: 311785674, count: 1 },
  { _id: 882944, count: 1 },
  { _id: 308535008, count: 1 },
  { _id: 9513237, count: 1 },
  { _id: 28135941, count: 1 },
  { _id: 74752664, count: 1 },
  { _id: 7498236, count: 1 },
  { _id: 8280699, count: 1 },
  { _id: 6873510, count: 1 },
  { _id: 182658486, count: 1 },
  { _id: 9362212, count: 1 },
  { _id: 31495845, count: 1 },
  { _id: 70487869, count: 1 }
]
Type "it" for more
```

## 7. Aggregate listings to calculate the average `review_scores_rating` for each neighborhood, filter to show only neighborhoods with an average rating of 4 or above, then sort in descending order by average rating.

   ```mongodb
   db.listings.aggregate([
     {$group: {_id: "$neighbourhood", averageRating: {$avg: "$review_scores_rating"}}},
     {$match: {averageRating: {$gte: 4}}},
     {$sort: {averageRating: -1}}
   ])
```
## Result
```json
[
  {
    _id: 'Schöneiche bei Berlin, Brandenburg, Germany',
    averageRating: 5
  },
  { _id: 'Berlin, SN, Germany', averageRating: 5 },
  { _id: 'Berlin, BE, Germany', averageRating: 5 },
  { _id: 'berlin, Berlin, Germany', averageRating: 5 },
  { _id: 'Berlin, Prenzlauer Berg, Germany', averageRating: 4.96 },
  {
    _id: 'Berlin- Charlottenburg, Berlin, Germany',
    averageRating: 4.94
  },
  {
    _id: 'Berlin Charlottenburg, Berlin, Germany',
    averageRating: 4.9366666666666665
  },
  { _id: 'Berlin-Kreuzberg, Berlin, Germany', averageRating: 4.92 },
  { _id: 'Alt Treptow, Berlin, Germany', averageRating: 4.9 },
  { _id: 'Berlin , Germany', averageRating: 4.89 },
  { _id: 'Berlin, Zehlendorf, Germany', averageRating: 4.89 },
  { _id: 'Berlin, Spandau, Germany', averageRating: 4.89 },
  { _id: 'Berlin - Mitte, Germany', averageRating: 4.873333333333334 },
  { _id: 'Mitte, Berlin, Germany', averageRating: 4.83 }
]
Type "it" for more
```

# Extra Credit: Set up a Python virtual environment
