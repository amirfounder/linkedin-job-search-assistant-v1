from __future__ import annotations

from src.terminal.v2.terminal import Terminal
from src.services.terminal import *


def run_terminal_in_thread():
    pools = {
        'linkedin_setup_tasks': [
            'open_linkedin', open_linkedin,
            'confirm_linkedin_signin', confirm_linkedin_signin
        ],
        'linkedin_outreach': [
            'scan_search_results_page', scan_search_results_page,
            'create_outreach_messages', create_outreach_message,
        ],
        'linkedin_nurturing': [
            'create_post_connection_follow_up_message', create_post_connection_follow_up_message,
            'follow_up_with_recruiter_after_x_days', follow_up_with_recruiter_after_x_days,
            'update_recruiter_cms_data', update_recruiter_cms_data
        ]
    }

    terminal = Terminal()
    entrypoint = terminal.create_entrypoint()

    for pool in pools:
        taskpool = entrypoint.create_pool(name=pool)
        for task in pools[pool]:
            name, fn = task
            task = taskpool.create_task(name=name)
            task.create_executor(fn=fn)

    return terminal.run_in_thread()
