import json
from os import listdir
from os.path import isfile


def get_json_from_directory(path):
    filenames = listdir(path)
    for filename in filenames:
        filepath = path + '/' + filename
        if isfile(filepath):
            with open(filepath, 'r') as f:
                yield json.loads(f.read())


def get_companies():
    for json_data in get_json_from_directory('data/top_tech_companies'):
        for result in json_data['results']:
            yield result


def get_linkedin_search_templates():
    with open('data/templates/linkedin_search.json', 'r') as f:
        for template in json.loads(f.read()):
            yield template


def create_linkedin_search_queries():
    for company in get_companies():
        for template in get_linkedin_search_templates():
            yield template.format(company=company)


for query in create_linkedin_search_queries():
    print(query)
