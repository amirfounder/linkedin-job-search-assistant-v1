import time
from threading import Thread

from src.cms import CMS, Recruiter
from src.helpers import open_browser_tab
from src.server import run_server_in_thread


if __name__ == '__main__':
    server_thread = run_server_in_thread()
    server_thread.join()

    cms = CMS()
    cms.load()
    cms.add(Recruiter(name='test'))
    recruits = cms.query({'name': 'test'})
    for recruit in recruits:
        print(recruit)
