from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Label, Placeholder, Input, Button
import configparser
from pathlib import Path

class OnboardingScreen(Screen):
    """Onboarding Screen to collected needed info for API"""

    api_key : str
    api_url : str

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("\nSETUP", id="title")
        with Horizontal():
            with Vertical(classes="OBpanel"):
                with Container(classes="top"):
                    yield Label("Use Wakatime Config", classes="header")
                yield Button("Search for Wakatime.cfg", id="searchCfg")
                yield Label("", id="searchResult")
                with Container(classes="bottom"):
                    yield Button("Continue", disabled=True, id="continueCfg")
            with Vertical(classes="OBpanel"):
                with Container(classes="top"):
                    yield Label("Use API Key", classes="header")
                yield Label("Hackatime API Key")
                yield Input(placeholder="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX", id="keyInput")
                with Container(classes="bottom"):
                    yield Button("Save and Continue", id="saveKey", disabled=True)    
        yield Footer()

    @on(Input.Submitted, "#keyInput")
    def handle_submit(self, event: Input.Submitted) -> None:
        user_key : str = event.value
        if bool(user_key):
            self.query_one("#saveKey", Button).disabled = False
        else:
            self.query_one("#saveKey", Button).disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "searchCfg":
            config_file = Path.home() / ".wakatime.cfg"
            
            if config_file.is_file():
                config = configparser.ConfigParser()

                try:
                    config.read(config_file)
                    self.api_key = config.get("settings", "api_key", fallback=None)
                    self.api_url = config.get("settings", "api_url", fallback=None)

                    self.query_one("#searchResult", Label).update("Config file found!")
                    self.query_one("#continueCfg", Button).disabled = False
                except Exception as e:
                    print(f"Error reading the configuration file: {e}")
                    self.query_one("#searchResult", Label).update(f"Error reading the configuration file: {e}")
            else:
                self.query_one("#searchResult", Label).update(f"Could not find wakatime config at: {str(config_file)}")

        elif button_id == "continueCfg":
            self.create_config_file(
                self.api_key,
                self.api_url,
                "wakatime.cfg"
            )
            
        elif button_id == "saveKey":
            self.create_config_file(
                self.query_one("#keyInput", Input).value,
                "https://hackatime.hackclub.com/api/hackatime/v1",
                )


    def create_config_file(self, api_key:str, api_url:str, mode:str = "manual"):
        config = configparser.ConfigParser()
        
        config["General"] = {
            "version": "1.0.0",
            "environment" : "development"
        }

        config["API Key"] = {
            "mode": mode,
            "api_url": api_url,
            "api_key": api_key,
        }

        with open("settings.cfg", "w") as configfile:
            config.write(configfile)