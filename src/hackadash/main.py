from textual.app import App
from hackadash.screens.onboarding import OnboardingScreen
from hackadash.screens.dashboard import DashboardScreen
from pathlib import Path


class Hackadash(App):
    
    CSS_PATH = "styles.tcss"

    SCREENS = {
        "onboarding": OnboardingScreen,
        "dashboard": DashboardScreen}

    def on_mount(self) -> None:
        if Path("settings.cfg").is_file():
            self.push_screen("dashboard")
        else:
            self.push_screen("onboarding")


def main():
    app = Hackadash()
    app.run()

if __name__ == "__main__":
    main()