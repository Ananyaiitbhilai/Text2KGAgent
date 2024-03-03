import json
import logging
import os

# Assuming the datasets library is still used for other purposes


# Define your dataset paths
dataset_paths = {
    "train": "/Users/ananyahooda/Desktop/Text2kg/data/datasets/docred/train.json",
    "dev": "/Users/ananyahooda/Desktop/Text2kg/data/datasets/docred/dev.json",
    "test": "/Users/ananyahooda/Desktop/Text2kg/data/datasets/docred/test.json", 
}

# Define your output paths
output_paths = {
    "train": "/Users/ananyahooda/Desktop/Text2kg/data/extracted_data/docred/train_triples.json",
    "dev": "/Users/ananyahooda/Desktop/Text2kg/data/extracted_data/docred/dev_triples.json",
    "test": "/Users/ananyahooda/Desktop/Text2kg/data/extracted_data/docred/test_triples.json",
}

mapping_types = {'LOC': '<loc>', 'MISC': '<misc>', 'PER': '<per>', 'NUM': '<num>', 'TIME': '<time>', 'ORG': '<org>'}




def generate_triples(filepath, output_path):
    triples_data = []
    relations_file = {"P6": "head of government", "P17": "country", "P19": "place of birth", "P20": "place of death", "P22": "father", "P25": "mother", "P26": "spouse", "P27": "country of citizenship", "P30": "continent", "P31": "instance of", "P35": "head of state", "P36": "capital", "P37": "official language", "P39": "position held", "P40": "child", "P50": "author", "P54": "member of sports team", "P57": "director", "P58": "screenwriter", "P69": "educated at", "P86": "composer", "P102": "member of political party", "P108": "employer", "P112": "founded by", "P118": "league", "P123": "publisher", "P127": "owned by", "P131": "located in the administrative territorial entity", "P136": "genre", "P137": "operator", "P140": "religion", "P150": "contains administrative territorial entity", "P155": "follows", "P156": "followed by", "P159": "headquarters location", "P161": "cast member", "P162": "producer", "P166": "award received", "P170": "creator", "P171": "parent taxon", "P172": "ethnic group", "P175": "performer", "P176": "manufacturer", "P178": "developer", "P179": "series", "P190": "sister city", "P194": "legislative body", "P205": "basin country", "P206": "located in or next to body of water", "P241": "military branch", "P264": "record label", "P272": "production company", "P276": "location", "P279": "subclass of", "P355": "subsidiary", "P361": "part of", "P364": "original language of work", "P400": "platform", "P403": "mouth of the watercourse", "P449": "original network", "P463": "member of", "P488": "chairperson", "P495": "country of origin", "P527": "has part", "P551": "residence", "P569": "date of birth", "P570": "date of death", "P571": "inception", "P576": "dissolved, abolished or demolished", "P577": "publication date", "P580": "start time", "P582": "end time", "P585": "point in time", "P607": "conflict", "P674": "characters", "P676": "lyrics by", "P706": "located on terrain feature", "P710": "participant", "P737": "influenced by", "P740": "location of formation", "P749": "parent organization", "P800": "notable work", "P807": "separated from", "P840": "narrative location", "P937": "work location", "P1001": "applies to jurisdiction", "P1056": "product or material produced", "P1198": "unemployment rate", "P1336": "territory claimed by", "P1344": "participant of", "P1365": "replaces", "P1366": "replaced by", "P1376": "capital of", "P1412": "languages spoken, written or signed", "P1441": "present in work", "P3373": "sibling"}
    with open(filepath) as json_file:
        f = json.load(json_file)
        for id_, row in enumerate(f):
            triplets = ''
            triplets_extracted = []  # Initialize the list to store extracted triplets
            prev_head = None
            relations_sorted = sorted(row['labels'], key=lambda tup: tup['h'])
            for relation in relations_sorted:
                # Create a dictionary for the current relation
                triplet_extracted = {
                    'head': row['vertexSet'][relation['h']][0]['name'],
                    'type': relations_file[relation['r']],
                    'tail': row['vertexSet'][relation['t']][0]['name']
                }
                # Append the dictionary to the list of extracted triplets
                triplets_extracted.append(triplet_extracted)

                if prev_head == relation['h']:
                    triplets += f' {mapping_types[row["vertexSet"][relation["h"]][0]["type"]]} ' + row['vertexSet'][relation['t']][0]['name'] + f' {mapping_types[row["vertexSet"][relation["t"]][0]["type"]]} ' + relations_file[relation['r']]
                elif prev_head == None:
                    triplets += '<triplet> ' + row['vertexSet'][relation['h']][0]['name'] + f' {mapping_types[row["vertexSet"][relation["h"]][0]["type"]]} ' + row['vertexSet'][relation['t']][0]['name'] + f' {mapping_types[row["vertexSet"][relation["t"]][0]["type"]]} ' + relations_file[relation['r']]
                    prev_head = relation['h']
                else:
                    triplets += ' <triplet> ' + row['vertexSet'][relation['h']][0]['name'] + f' {mapping_types[row["vertexSet"][relation["h"]][0]["type"]]} ' + row['vertexSet'][relation['t']][0]['name'] + f' {mapping_types[row["vertexSet"][relation["t"]][0]["type"]]} ' + relations_file[relation['r']]
                    prev_head = relation['h']

                
                triples_data.append({
                    "title": str(id_),
                    "context":  ' '.join([word for sentence in row['sents'] for word in sentence]),
                    "id": str(id_),
                    "triplets_sentence": triplets,
                    "triplets": triplets_extracted,  # Add the list of triplet dictionaries
                })

    # Save the generated triples to the specified output path
    with open(output_path, 'w') as outfile:
        json.dump(triples_data, outfile, indent=4)

# Generate and save triples for each dataset split
for split in ['train', 'dev', 'test']:
    generate_triples(dataset_paths[split], output_paths[split])