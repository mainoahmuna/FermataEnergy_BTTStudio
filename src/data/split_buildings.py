import json
import pandas as pd
from sklearn.model_selection import train_test_split

PATH = 'UserPath to metadata_removed_lost_l_and_w.csv'

def population_split_buildings(PATH):
    # Load metadata
    md = pd.read_csv(PATH)

    # Extract the building IDs and group by building type
    train_ids = []
    test_ids = []

    # Group by 'in.comstock_building_type_group' to ensure balanced distribution
    for _, group in md.groupby('in.comstock_building_type_group'):
        bldg_ids = group['bldg_id']
        
        # Split 80% train, 20% test within each group
        train, test = train_test_split(bldg_ids, test_size=0.2, random_state=42)
        
        # Append '.csv' to each ID and add to the lists
        train_ids.extend(train.astype(str) + '.csv')
        test_ids.extend(test.astype(str) + '.csv')

    # Convert to JSON format
    split_data = {
        "train_bldg_ids": train_ids,
        "test_bldg_ids": test_ids
    }

    # Save to JSON file
    with open('data.json', 'w') as json_file:
        json.dump(split_data, json_file, indent=4)

    print("Building IDs split with '.csv' appended and saved to building_ids_split.json")

    