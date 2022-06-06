import json
import time
import webbrowser
from abc import ABC
from enum import Enum
from threading import Thread
from typing import Generator
from urllib.parse import quote_plus

from flask import Flask, request
from flask_cors import CORS


class GlobalScraperState:
    class States(Enum):
        ScrapingProfiles = 'scraping_profiles'
        ScrapingSearchResults = 'scraping_search_results'
    
    def __init__(self):
        self.current_state = None
    
    def activate(self, state: States):
        self.current_state = state
    
    def is_active(self, state: States):
        return self.current_state == state


global_state = GlobalScraperState()


def read_json(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


def save_dict(path, dict_obj):
    json_obj = json.dumps(dict_obj, indent=4)
    save_json(path, json_obj)


def save_json(path, json_obj):
    with open(path, 'w') as f:
        f.write(json_obj)


def open_browser_tab(url: str):
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open_new(url)


class Model(ABC):
    keys = []

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.keys:
                setattr(self, k, v)

    @classmethod
    def from_dict(cls, params):
        return cls(**params)

    def to_dict(self):
        return {k: getattr(self, k, None) for k in self.keys}


class Recruiter(Model):
    keys = read_json('disk/models.json')['recruiter']['keys']


class Company(Model):
    keys = read_json('disk/models.json')['company']['keys']


class ScrapedSearchResultsIndex:
    def __init__(self):
        self.index = {}

    def has_company_position_seconds_since_loaded(self, company, position, seconds_since_loaded):
        return seconds_since_loaded in self.index.get(company, {}).get(position, {})

    def add_company_position_seconds_since_loaded(self, company, position, seconds_since_loaded):
        if company not in self.index:
            self.index[company] = {}
        if position not in self.index[company]:
            self.index[company][position] = {}
        self.index[company][position][seconds_since_loaded] = True


class CMS:
    def __init__(self):
        self.recruiter_search_templates = read_json('disk/recruiter_search_templates.json')
        self.companies = [Company.from_dict(c) for c in read_json('disk/cms_data_companies.json')]
        self.recruiters = [Recruiter.from_dict(r) for r in read_json('disk/cms_data_recruiters.json')]

    @staticmethod
    def build_search_results_page_url(template, company, page):
        keywords = quote_plus(template.format(company=company))
        base = 'https://www.linkedin.com/search/results/people/'
        params = '?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&page={page}'.format(keywords=keywords, page=page)
        return base + params

    def get_next_search_results_page_urls(self) -> Generator[str, None, None]:
        for company in self.companies:
            for name, template in self.recruiter_search_templates:
                if getattr(company, f'{name}_search_template_used'):
                    for page in range(1, 4):
                        yield self.build_search_results_page_url(template, company, page)

    def get_next_profile_page_urls(self) -> Generator[str, None, None]:
        pass
    
    def get_next_urls(self) -> Generator[str, None, None]:
        _map = {
            GlobalScraperState.States.ScrapingSearchResults: self.get_next_search_results_page_urls,
            GlobalScraperState.States.ScrapingProfiles: self.get_next_profile_page_urls
        }
        
        yield _map[global_state.current_state]
    

def scrape_search_results():
    global_state.activate(GlobalScraperState.States.ScrapingSearchResults)
    idx = ScrapedSearchResultsIndex()
    cms = CMS()
    app = Flask(__name__)
    CORS(app)

    @app.route('/save-html', methods=["POST"])
    def save_html():
        data = request.json

        url = data['url']
        html = data['html']
        seconds_since_loaded = data['seconds_since_loaded']

        company, position, seconds_since_loaded = get_args_from_url(url)
        idx.add_company_position_seconds_since_loaded(company, position, seconds_since_loaded)

    thread = Thread(target=lambda: app.run(port=8080))
    thread.start()

    for next_url in cms.get_next_urls():
        open_browser_tab(next_url)
        time.sleep(5)

    thread.join()
