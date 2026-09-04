from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.widgets import Header, Footer, Label, Digits




class DashboardScreen(Screen):
    """Dashboard Screen to display info from hackatime api calls"""

    BINDINGS = [("r", "refresh", "Refresh Dashboard")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()