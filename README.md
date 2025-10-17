# StudIP Calendar Export Batch Renamer

# Why?

StudIP uses the very verbose, actual lecture name for calendar entries. For example: "Introduction to Neurobiology" is `Vorlesung: Introduction to Neurobiology - mit benotetem Leistungsnachweis [Klausur] für Studierende der "Cognitive Science" und für Studenten mit Nebenfach Biologie [BIO-SK]`. It's a mess! And while you can manually edit the ICS file to batch rename events, it's a hassle! With this program, you can choose a new name which will be applied to all lecture events of a certain lecture, thereby simplifying your calendar significantly, bringing peace and calm into your otherwise messy life.

# Usage

1. Download your calendar export (German: StudIP -> Planer -> Kalender -> Termine exportieren -> Alle Termine, English: StudIP -> Planner -> Calendar -> Export Dates -> All Dates)
3. Make sure you have `uv` installed and in your PATH: `https://docs.astral.sh/uv/getting-started/installation/`
2. Run `git clone https://github.com/paraversal/StudIPCalendarExportRenamer && cd StudIPCalendarExportRenamer`
4. Run `uv run main.py <filepath to the downloaded .ics file>`

## Inside the application

- this program runs inside the terminal, and you use the keyboard to navigate around it. But don't be afraid, it's super simple!

For most lectures, you're going to see only a single entry in the table inside of the program. For these courses, you can do the following: 

- navigate to the event using the arrow keys, press `r`, enter the new desired name, press `enter`

However, some lectures have multiple unique event names (such as when some lectures are cancelled beforehand). For these cases, the program also contains a merge functionality. This can work in two ways:

1. Merge+rename events: navigate to the lectures and select them by pressing `m` (they will be highlighted in red). Once you have marked all events, `r` to rename the group, type in your desired name, and press `enter`
2. Merge events: navigate to the lectures and select them by pressing `m` (they will be highlighted in red). Once you have marked all events, press `M` (`shift+m`) to merge the events into a single event.

The first option is probably what you want.

Once you have renamed all your events and are happy with the names you chose, simply press `ctrl+q` to quit. The program will automatically export a file named `renamed_events.ics` inside the folder you cloned it into. This file can now be added to your calendar.