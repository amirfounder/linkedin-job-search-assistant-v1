from threading import Thread

from flask import Flask, request, make_response
from flask_cors import CORS
from .helpers import (
    create_linkedin_profile_html_filename,
    create_linkedin_search_results_html_filename,
    is_url_profile,
    is_url_search_results,
    save_html_contents,
)


app = Flask(__name__)
CORS(app)


@app.route('/save_html', methods=["POST"])
def save_html_controller():
    data = request.json

    url = data['url']
    html = data['html']
    seconds_since_loaded = data['seconds_since_loaded']

    if is_url_search_results(url):
        filename = create_linkedin_search_results_html_filename(url, seconds_since_loaded)
        save_html_contents(html, filename)
    if is_url_profile(url):
        filename = create_linkedin_profile_html_filename(url, seconds_since_loaded)
        save_html_contents(html, filename)

    return {'status': 'GOOD'}, 201


def run_server():
    app.run(port=8080)


def run_server_in_thread(start=True, join=False):
    thread = Thread(target=run_server, daemon=True)
    if not start:
        return thread

    thread.start()
    if not join:
        return thread

    thread.join()
    return thread
