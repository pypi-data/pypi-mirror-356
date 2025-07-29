import json
import os
from datetime import datetime, timezone
from tornado import gen, web
from jupyter_server.base.handlers import JupyterHandler, json_errors
from jupyter_activity_monitor_extension.docker_sidecar_check import (
    check_if_sidecars_idle,
)
from jupyter_activity_monitor_extension.idle_status_detector import (
    LocalFileActiveTimestampChecker,
)

ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fz"

first_request_time = None
activity_tracker = datetime.now(timezone.utc).strftime(ISO_DATETIME_FORMAT)


class IdleHandler(JupyterHandler):
    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self):
        # record the time when the request was first made to the endpoint
        global first_request_time, activity_tracker
        if first_request_time is None:
            first_request_time = datetime.now(timezone.utc).strftime(
                ISO_DATETIME_FORMAT
            )
        sm = self.settings["session_manager"]
        tm = self.terminal_manager
        sessions = yield sm.list_sessions()
        terminals = tm.list()
        largest_last_activity = self.get_last_active_timestamp(
            sessions, terminals, first_request_time
        )

        # check the timestamp from /tmp/.sagemaker-last-active-timestamp
        timestamp_from_local_file = (
            LocalFileActiveTimestampChecker().read_last_active_timestamp()
        )
        if timestamp_from_local_file:
            larger_timestamp = max(
                datetime.strptime(largest_last_activity, ISO_DATETIME_FORMAT),
                timestamp_from_local_file,
            )
            largest_last_activity = larger_timestamp.strftime(ISO_DATETIME_FORMAT)

        if datetime.strptime(activity_tracker, ISO_DATETIME_FORMAT) < datetime.strptime(
            largest_last_activity, ISO_DATETIME_FORMAT
        ):
            activity_tracker = largest_last_activity
        # check if any running sidecars are broadcasting as not idle
        all_sidecars_idle = check_if_sidecars_idle()
        current_time = datetime.now(timezone.utc).strftime(ISO_DATETIME_FORMAT)
        if (largest_last_activity is not None) and all_sidecars_idle:
            response = {"lastActiveTimestamp": activity_tracker}
        elif not all_sidecars_idle:
            response = {"lastActiveTimestamp": current_time}
        else:
            response = {}
        self.finish(json.dumps(response))

    def get_last_active_timestamp(self, sessions, terminals, first_request_time):
        session_last_activity_time = max(
            (
                datetime.strptime(
                    session["kernel"]["last_activity"], ISO_DATETIME_FORMAT
                )
                for session in sessions
            ),
            default=datetime.strptime(first_request_time, ISO_DATETIME_FORMAT),
        )
        terminals_last_activity_time = max(
            (
                datetime.strptime(terminal["last_activity"], ISO_DATETIME_FORMAT)
                for terminal in terminals
            ),
            default=datetime.strptime(first_request_time, ISO_DATETIME_FORMAT),
        )

        max_last_activity_time = max(
            session_last_activity_time, terminals_last_activity_time
        )

        return max_last_activity_time.strftime(ISO_DATETIME_FORMAT)
