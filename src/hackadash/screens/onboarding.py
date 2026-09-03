from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Label, Placeholder, Input, Button

class OnboardingScreen(Screen):
    """Onboarding Screen to collected needed info for API"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("\nSETUP", id="title")
        with Horizontal():
            with Vertical(classes="OBpanel"):
                with Container(classes="top"):
                    yield Label("Use Wakatime Config", classes="header")
                yield Label("", id="result")
                yield Button("Search for Wakatime.cfg")
                with Container(classes="bottom"):
                    yield Button("Continue", disabled=True)
            with Vertical(classes="OBpanel"):
                with Container(classes="top"):
                    yield Label("Use API Key", classes="header")
                yield Label("Hackatime API Key")
                yield Input(placeholder="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX")
                with Container(classes="bottom"):
                    yield Button("Save and Continue")    
        yield Footer()

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted) -> None:
        """Runs when the user presses Enter inside the input field."""
        chosen_path = Path(event.value)

        status = ""
        
        if not chosen_path.exists():
            status = f"File {chosen_path} does not exist"
            
        self.query_one("#result", Label).update(status)