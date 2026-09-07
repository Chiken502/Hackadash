from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.widgets import Header, Footer, Label, Digits
import http.client
import configparser
from pathlib import Path
import json



class DashboardScreen(Screen):
    """Dashboard Screen to display info from hackatime api calls"""

    BINDINGS = [("r", "refresh", "Refresh Dashboard")]

    display_name = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Name: ...", id="displayName")
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
                "/api/hackatime/v1/users/%7Bid%7D?api_key=YOUR_SECRET_TOKEN",
                headers=headers
            )

            response = conn.getresponse()
            raw_data = response.read().decode("utf-8")
            data_dict = json.loads(raw_data)

            self.display_name = data_dict["data"]["display_name"]

            conn.close()


            self.query_one("#displayName", Label).update("Name : " + self.display_name)
        else:
            self.app.switch_screen("onboarding")
