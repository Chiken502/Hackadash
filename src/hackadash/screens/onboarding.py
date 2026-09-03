from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label

class OnboardingScreen(Screen):
    """Onboarding Screen to collected needed info for API"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Onboarding")
        yield Footer()