from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.widgets import Header, Footer, Label, Digits
import http.client
import configparser
from pathlib import Path
import json
from datetime import datetime, timedelta, timezone



class DashboardScreen(Screen):
    """Dashboard Screen to display info from hackatime api calls"""

    BINDINGS = [("r", "refresh", "Refresh Dashboard")]

    display_name = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Name: ...", id="displayName")
        yield Label("ID: ...", id="userId")
        yield Label("Total Time: ...", id="totalAllTime")
        yield Label("Time past 7 days: ...", id="totalWeekTime")
        yield Label("Daily avg past 7 days: ...", id="dailyAvgTime")
        yield Footer()

    def _on_mount(self, event):
        self.fetch_data()

    def action_refresh(self) -> None:
        self.fetch_data()


    def fetch_data(self):
        settings_path = Path("settings.cfg")
        if settings_path.is_file():
            config = configparser.ConfigParser()
            config.read("settings.cfg")

            api_key = config["API Key"]["api_key"]
            api_url = config["API Key"]["api_url"]

            conn = http.client.HTTPSConnection("hackatime.hackclub.com")

            headers = {
                "Authorization": f"Bearer {api_key}"
            }

            conn.request(
                "GET",
                "/api/v1/users/my/stats?start_date=&end_date=&limit=1&features=languages,projects&filter_by_project=&filter_by_category=&boundary_aware=true&total_seconds=false&no_ai_coding=true&test_param=true",
                headers=headers
            )
            response = conn.getresponse().read().decode("utf-8")
            data_dict = json.loads(response)
            self.display_name = data_dict["data"]["username"]
            self.user_id = data_dict["data"]["user_id"]
            self.total_seconds_readable = data_dict["data"]["human_readable_total"]

            conn.request(
                "GET",
                f"/api/v1/users/my/stats?start_date={(datetime.now(timezone.utc) - timedelta(days=7)).isoformat(timespec='seconds')}&end_date=&limit=1&features=languages,projects&filter_by_project=&filter_by_category=&boundary_aware=true&total_seconds=false&no_ai_coding=true&test_param=true",
                headers=headers
            )
            response = conn.getresponse().read().decode("utf-8")
            data_dict = json.loads(response)
            self.total_week_readable = data_dict["data"]["human_readable_total"]
            self.daily_avg_week_readable = data_dict["data"]["human_readable_daily_average"]


            conn.close()

            self.query_one("#displayName", Label).update(f"Name: {self.display_name}")
            self.query_one("#userId", Label).update(f"ID: {self.user_id}")
            self.query_one("#totalWeekTime", Label).update(f"Time past 7 days: {self.total_week_readable}")
            self.query_one("#dailyAvgTime", Label).update(f"Daily avg past 7 days: {self.daily_avg_week_readable}")
            self.query_one("#totalAllTime", Label).update(f"Total Time: {self.total_seconds_readable}")
        else:
            self.app.switch_screen("onboarding")
