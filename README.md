<p align="center">
    <h1 align="center"> Hackadash </h1>
</p>

<p align="center">
A customizable dash board for hackatime in your terminal! Built with <a href="https://github.com/Textualize/textual">Textual</a>, an amazing TUI framework!
</p>

![Hackadash Dashboard image](https://github.com/Chiken502/Hackadash/blob/main/images/exampleImg1.png?raw=true)

## Installation & Running

Follow these steps to set up and run the application locally:

### 1. Clone the repository
```bash
git clone https://github.com/Chiken502/Hackadash
cd hackadash
```

### 2. Set up a virtual environment
```bash
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install the package
Install the repository locally in editable mode so your CLI shortcut is registered:
```bash
pip install -e .
```

### 4. Run the app
Now you can start the application from anywhere in your terminal by running:
```bash
hackadash
```
**Note**: You still have to be in the virtual environment that you installed hackadash inside of in step 3. If you want to run hackadash from anywhere skip step 2.

### 5. Enter Hackatime API Key
![Hackadash Setup Screen](https://github.com/Chiken502/Hackadash/blob/main/images/exampleImg2.png?raw=true)

Select one of the two given options to continue. This step gets your hackatime API Key so that Hackadash can send API requests for the data it displays. On this screen you are presented with two options.

- **Option 1: Use Wakatime Config (recomended)**
  - Hackadash will then look for the `.wakatime.cfg`, that all hackatime applications use, in your home directory. If it finds the file, then it will read the API Key from it and your good to go. If it can't find the `.wakatime.cfg` file then you will have to use option 2.
- **Option 2: Manualy Input API Key**
  - Find your API Key in [Hackatime settings](https://hackatime.hackclub.com/my/settings/setup). Then copy paste the key into the text box, and hit save and continue.

## Features
- Manual api_key input or automatic search for `.wakatime.cfg`
- Total Coding Time
- Weekly and Daily Leaderbaord placements
- Average coding time in the last 7 days
- Top 3 projects and the respective times
- Top 3 languages and the respective times
- Data Refreshing
- Time range switching to veiw times, projects, and languages for time ranges of total, weekly or today.
- Hackatime username and ID
- Customizable Themes! (Just comes with Textual! use `^p` or `cmd + p` to open the menu)

## Hackadash Bindings
![Bindings](https://github.com/Chiken502/Hackadash/blob/main/images/bindingsImg.png?raw=true)
Bindings are keys that you can press to do something

- r: Refresh the API data
- s: Switch the time frame. Cycles through total, weekly, today
- c: Close Hackadash