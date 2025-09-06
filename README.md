# Hourly Reminder
*README.md under construction*

Hourly Reminder is a quick, little Python program I wrote that automatically sends notifications for each new hour, complete with a different icon and sound each time. It is intended to be similar to a cuckoo clock. I created it as an aid for ADHD, one of its major symptoms being time blindness, so I could be reminded of time passing and be more productive as the result.

It is Windows-only for now.

<img width="553" height="277" alt="Hourly Reminder notification screenshot" src="https://github.com/user-attachments/assets/5681ad84-0f5c-4a48-abaa-8c338494e761" />

*You may be wondering, "Why Sonic the Hedgehog?" Well, Sonic the Hedgehog is my favorite franchise of all time, and I originally created this program specifically for that autistic special interest. However, when I considered publishing it on GitHub, my thoughts turned to allowing customization of the program. I could've drawn my own Sonic art, but this is supposed to be a minor project and thus quick, so I reused [Sega's Sonic the Hedgehog](https://sonic.fandom.com/wiki/Sega%27s_Sonic_the_Sketchog) digital sticker images that I already used for my Rainmeter time skin (seen partially in screenshot above). There are also clips of various songs from the Sonic games, which honestly took a long time to find to match with hours' intended moods.*

## How to use
### The program itself
1. Go to the [releases page](https://github.com/PrincessPandaSource/Hourly-Reminder/releases/) and download the ZIP file.
2. Unzip and put the folder somewhere on your computer.
3. Go into the folder and click on `main.exe`.
4. The executable's icon should appear in the system tray (the arrow/chevron in the toolbar).
5. To stop the program, right-click the icon and select "Quit".

<img width="327" height="263" alt="Hourly Reminder in system tray screenshot" src="https://github.com/user-attachments/assets/1055d3ad-f1f2-4b0a-8bcb-cfe14387c417" />

*If you're wondering why I decided to use Sonic as the program's icon, it's because of the Sonic theme, and yes, you can customize it (see below, but with a caveat).*

Those who want the program to run the automatically on startup should make and copy a shortcut of the executable, go to "shell:startup" in the File Explorer path bar, and paste the shortcut there.

#### Customizing
Text on the reminders can be customized by editing the `reminders_data.json`. Each hour has `title` and `description` details. `title` stores what's written in the first and wholly black text line of the notification, while `description` stores what's written in the second text line, which is also in slightly lighter color.

Icons and sounds can be replaced in the `images` and `sounds` folder respectively.

### Its source code
Those who want to further tweak and modify the program with code can download the source code and run and build it on their own machine.

Not only must you have Python installed (can be downloaded [here](https://www.python.org/downloads/), but the following Python libraries are required:
* [windows_toasts](https://pypi.org/project/Windows-Toasts/)
* [schedule](https://pypi.org/project/schedule/)
* [pycaw](https://pypi.org/project/pycaw/)
* [pywin32](https://pypi.org/project/pywin32/)
* [pystray](https://pypi.org/project/pystray/)
* [pyinstaller](https://pypi.org/project/pyinstaller/)

Building the program with an executable can be done by executing `.\build.bat`, which also bundles the executable with the assets folder and JSON file.

### Commands

# Miscellaneous notes
I currently have no idea how to make it so that the notification shows Hourly Reminder is the program it's from, not Command Prompt. I used the custom script from the windows_toasts library that registers a custom app ID, but I couldn't get it to work.

In the future, I could not only update this program with my own art, but have the default assets be freely licensed icons and clips of royalty-free music instead of *Sonic* icons and song clips. (Previous assets used could still be stored in a separate folder.)

# Credits
