from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.widgets import Header, Footer, Label, Digits
from textual import work
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
        yield Label("")
        yield Label("Total Time:", id="totalAllTimeLabel")
        yield Digits("00:00:00", id="totalAllTime")
        yield Label("Time past 7 days: ...", id="totalWeekTime")
        yield Label("Daily avg past 7 days: ...", id="dailyAvgTime")
        yield Label("")
        yield Label("Daily Leaderboard Rank: ...", id="dailyLeaderboardRank")
        yield Label("Weekly Leaderboard Rank: ...", id="weeklyLeaderboardRank")
        yield Footer()

    def _on_mount(self, event):
        self.fetch_data()

    def action_refresh(self) -> None:
        self.query_one("#totalAllTime", Digits).update("00:00:00")
        self.query_one("#totalWeekTime", Label).update("Time past 7 days: ...")
        self.query_one("#dailyAvgTime", Label).update("Daily avg past 7 days: ...")
        self.query_one("#dailyLeaderboardRank", Label).update("Daily Leaderboard Rank: ...")
        self.query_one("#weeklyLeaderboardRank", Label).update("Weekly Leaderboard Rank: ...")

        self.fetch_data()

    @work(exclusive=True, thread=True)
    async def fetch_data(self):
        self.fetch_cfg_data()
        self.fetch_user_data()

        self.fetch_total_stats()
        self.fetch_weekly_stats()
        self.fetch_daily_leaderboard_data()
        self.fetch_weekly_leaderboard_data()

    def fetch_cfg_data(self):
        settings_path = Path("settings.cfg")
        if settings_path.is_file():
            config = configparser.ConfigParser()
            config.read("settings.cfg")

            self.api_key = config["API Key"]["api_key"]
            self.api_url = config["API Key"]["api_url"]
        else:
            self.app.switch_screen("onboarding")
    
    def fetch_user_data(self):
        conn = http.client.HTTPSConnection("hackatime.hackclub.com", timeout=30)
                
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        conn.request(
            "GET",
            "/api/hackatime/v1/users/current",
            headers=headers
        )

        response = conn.getresponse().read().decode("utf-8")
        data_dict = json.loads(response)

        self.display_name = data_dict["data"]["display_name"]
        self.user_id = data_dict["data"]["id"]
        self.user_photo = data_dict["data"]["photo"]

        self.query_one("#displayName", Label).update(f"Name: {self.display_name}")
        self.query_one("#userId", Label).update(f"ID: {self.user_id}")

        conn.close()

    @work()
    async def fetch_daily_leaderboard_data(self):
        conn = conn = http.client.HTTPSConnection("hackatime.hackclub.com", timeout=30)

        conn.request(
            "GET",
            "/api/v1/leaderboard/daily",
        )
        response = conn.getresponse().read().decode("utf-8")
        data_dict = json.loads(response)

        self.daily_leaderboard_rank = -1
        for i in data_dict["entries"]:
            if str(i["user"]["id"]) == str(self.user_id):
                self.daily_leaderboard_rank = i["rank"]
                break

        self.daily_leaderboard_last_update = data_dict["generated_at"]

        self.query_one("#dailyLeaderboardRank", Label).update(f"Daily Leaderboard Rank: {self.daily_leaderboard_rank}")

        conn.close()

    @work()
    async def fetch_weekly_leaderboard_data(self):
        conn = conn = http.client.HTTPSConnection("hackatime.hackclub.com", timeout=30)

        conn.request(
            "GET",
            "/api/v1/leaderboard/weekly",
        )
        response = conn.getresponse().read().decode("utf-8")
        data_dict = json.loads(response)

        self.weekly_leaderboard_rank = -1
        for i in data_dict["entries"]:
            if str(i["user"]["id"]) == str(self.user_id):
                self.weekly_leaderboard_rank = i["rank"]
                break

        self.weekly_leaderboard_last_update = data_dict["generated_at"]

        self.query_one("#weeklyLeaderboardRank", Label).update(f"Weekly Leaderboard Rank: {self.weekly_leaderboard_rank}")

        conn.close()

    @work()
    async def fetch_weekly_stats(self):
        conn = http.client.HTTPSConnection("hackatime.hackclub.com", timeout=30)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        conn.request(
            "GET",
            f"/api/v1/users/my/stats?start_date={(datetime.now(timezone.utc) - timedelta(days=7)).isoformat(timespec='seconds')}&end_date=&limit=1&features=languages,projects&filter_by_project=&filter_by_category=&boundary_aware=true&total_seconds=false&no_ai_coding=true&test_param=true",
            headers=headers
        )

        response = conn.getresponse().read().decode("utf-8")
        data_dict = json.loads(response)

        self.total_week_readable = data_dict["data"]["human_readable_total"]
        self.daily_avg_week_readable = data_dict["data"]["human_readable_daily_average"]
        self.projects_week = data_dict["data"]["projects"]
        self.languages_week = data_dict["data"]["languages"]

        self.query_one("#totalWeekTime", Label).update(f"Time past 7 days: {self.total_week_readable}")
        self.query_one("#dailyAvgTime", Label).update(f"Daily avg past 7 days: {self.daily_avg_week_readable}")

        conn.close()

    @work()
    async def fetch_total_stats(self):
        conn = http.client.HTTPSConnection("hackatime.hackclub.com", timeout=30)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        conn.request(
            "GET",
            "/api/v1/users/my/stats?start_date=&end_date=&limit=1&features=languages,projects&filter_by_project=&filter_by_category=&boundary_aware=true&total_seconds=false&no_ai_coding=true&test_param=true",
            headers=headers
        )

        response = conn.getresponse().read().decode("utf-8")
        data_dict = json.loads(response)

        self.total_seconds = data_dict["data"]["total_seconds"]
        self.streak = data_dict["data"]["streak"]
        self.projects = data_dict["data"]["projects"]
        self.languages = data_dict["data"]["languages"]

        self.query_one("#totalAllTime", Digits).update(self.getDigitFormat(self.total_seconds))

        conn.close()

    def getDigitFormat(self, seconds: int) -> str:
        hours = int(seconds/60.0/60.0)
        minutes = int((seconds - (hours*60*60)) /60.0)
        remaning_seconds = seconds - (hours*60*60) - (minutes * 60)

        return f"{hours:02}:{minutes:02}:{remaning_seconds:02}"