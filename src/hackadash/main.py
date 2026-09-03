from textual.app import App
from hackadash.screens.onboarding import OnboardingScreen


class Hackadash(App):
    
    CSS_PATH = "styles.tcss"

    SCREENS = {"onboarding": OnboardingScreen}

    def on_mount(self) -> None:
        self.push_screen("onboarding")


def main():
    app = Hackadash()
    app.run()

if __name__ == "__main__":
    main()