import json
import logging
import os

# Assuming the datasets library is still used for other purposes


# Define your dataset paths
dataset_paths = {
    "train": "/Users/ananyahooda/Desktop/Text2kg/data/datasets/nyt/train.json",
    "dev": "/Users/ananyahooda/Desktop/Text2kg/data/datasets/nyt/dev.json",
    "test": "/Users/ananyahooda/Desktop/Text2kg/data/datasets/nyt/test.json", 
}

# Define your output paths
output_paths = {
    "train": "/Users/ananyahooda/Desktop/Text2kg/data/extracted_data/nyt/train_triples.json",
    "dev": "/Users/ananyahooda/Desktop/Text2kg/data/extracted_data/nyt/dev_triples.json",
    "test": "/Users/ananyahooda/Desktop/Text2kg/data/extracted_data/nyt/test_triples.json",
}

mapping = {'/people/person/nationality': 'country of citizenship', '/sports/sports_team/location': 'headquarters location', 
            '/location/country/administrative_divisions': 'contains administrative territorial entity', '/business/company/major_shareholders': 'shareholders', 
            '/people/ethnicity/people': 'country of origin', '/people/ethnicity/geographic_distribution': 'denonym', 
            '/business/company_shareholder/major_shareholder_of': 'major shareholder', '/location/location/contains': 'location',
            '/business/company/founders': 'founded by', '/business/person/company': 'employer', '/business/company/advisors': 'advisors', 
            '/people/deceased_person/place_of_death': 'place of death', '/business/company/industry': 'industry', 
            '/people/person/ethnicity': 'ethnicity', '/people/person/place_of_birth': 'place of birth', 
            '/location/administrative_division/country': 'country', '/people/person/place_lived': 'residence', 
            '/sports/sports_team_location/teams': 'member of sports team', '/people/person/children': 'child', 
            '/people/person/religion': 'religion', '/location/neighborhood/neighborhood_of': 'neighborhood of', 
            '/location/country/capital': 'capital', '/business/company/place_founded': 'location of formation', 
            '/people/person/profession': 'occupation'}

mapping_types = {'LOCATION': '<loc>', 'ORGANIZATION': '<org>', 'PERSON': '<per>'}




def generate_triples(filepath, output_path):
    triples_data = []
    with open(filepath) as json_file:
        f = json.load(json_file)
        for id_, row in enumerate(f):
            triplets_sentence = ''
            triplets_list = []  # List to hold the triplets dictionaries
            prev_head = None
            list_relations = zip(row['spo_list'], row['spo_details'])
            relations_sorted = sorted(list_relations, key=lambda tup: tup[1][0])
            for relation, details in relations_sorted:
                # Create a triplet dictionary for each relation
                triplet_dict = {'head': relation[0], 'type': mapping[relation[1]], 'tail': relation[2]}
                triplets_list.append(triplet_dict)

                if prev_head == relation[0]:
                    triplets_sentence += f' {mapping_types[details[2]]} ' + relation[2] + f' {mapping_types[details[-1]]} ' + mapping[relation[1]]
                elif prev_head is None:
                    triplets_sentence += '<triplet> ' + relation[0] + f' {mapping_types[details[2]]}  ' + relation[2] + f' {mapping_types[details[-1]]} ' + mapping[relation[1]]
                    prev_head = relation[0]
                else:
                    triplets_sentence += ' <triplet> ' + relation[0] + f' {mapping_types[details[2]]}  ' + relation[2] + f' {mapping_types[details[-1]]} ' + mapping[relation[1]]
                    prev_head = relation[0]
            text = ' '.join(row['tokens'])
            triples_data.append({
                "title": str(id_),
                "context": text,
                "id": str(id_),
                "triplets_sentence": triplets_sentence,
                "triplets": triplets_list,  # Add the list of triplet dictionaries
            })

    # Save the generated triples to the specified output path
    with open(output_path, 'w') as outfile:
        json.dump(triples_data, outfile, indent=4)

# Generate and save triples for each dataset split
for split in ['train', 'dev', 'test']:
    generate_triples(dataset_paths[split], output_paths[split])