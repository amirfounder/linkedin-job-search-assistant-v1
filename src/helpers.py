import json
from os import listdir
from os.path import isfile
from urllib.parse import unquote


def get_json_from_directory(path: str):
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


def get_params_from_url(url: str):
    params = [param.split('=') for param in url.split('?')[1].split('&')]
    params = {k: v for k, v in params}
    params['page'] = params.get('page', 0)
    params['keywords'] = unquote(params.get('keywords', '')).replace(' ', '_')

    return params


def create_linkedin_search_results_html_filename(url: str, seconds_since_loaded: int):
    params = get_params_from_url(url)

    return 'type=search_results&keywords={}&page={}&seconds_since_loaded={}'.format(
        params['keywords'],
        params['page'],
        seconds_since_loaded
    )


def create_linkedin_profile_html_filename(url: str, seconds_since_loaded: int):
    profile_slug = url.split('linkedin.com/in/')[1]

    return 'type=profile&profile_slug={}&seconds_since_loaded={}'.format(
        profile_slug,
        seconds_since_loaded
    )


def is_url_profile(url: str):
    return 'linkedin.com/in/' in url


def is_url_search_results(url: str):
    return 'linkedin.com/search/results/' in url


def save_html_contents(html: str, filename: str):
    path = 'data/scraped/' + filename.removeprefix('/')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


for query in create_linkedin_search_queries():
    print(query)
