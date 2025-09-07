# Hourly Reminder
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

Those who want the program to run the automatically on startup should make and copy a shortcut of the executable, go to "shell:startup" in the File Explorer path bar, and paste the shortcut there. To have it searchable in the Start Menu, go to "C:\ProgramData\Microsoft\Windows\Start Menu\Programs" and paste the shortcut there (you'll need administrator permissions).

#### Customizing
Text on the reminders can be customized by editing the `reminders_data.json`. Each hour has `title` and `description` details. `title` stores what's written in the first and wholly black text line of the notification, while `description` stores what's written in the second text line, which is also in slightly lighter color.

Icons and sounds can be replaced in the `images` and `sounds` folders, respectively.

Icons for the reminders themselves must be in the PNG file format and named only with numerical values according to their assigned hours (24-hour format, no leading zeroes). The icon for the app icon must be in the ICO file format and named "app_icon". Icons are recommended to be in square size to prevent them from having parts cropped out in the notifications. There are countless image editors and converter tools; I used [GIMP](https://www.gimp.org/) and would recommend it. (Custom app icon is supported for the system tray, but cannot be changed for the executable. You may want to create a shortcut and change its icon instead.)

Sounds must be in the WAV file format (only format supported by the winsound library used) and 6.25 seconds long at maximum. I used [Audacity](https://www.audacityteam.org/) to edit and convert the audio files, and I would recommend it.

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
The program comes with several commands to use in a command-line interface, such as Command Prompt or PowerShell on Windows. To use one, either set the current directory to the program file's directory and input the program file's name, or paste the path to the file, follow with the command's text (and its parameter if needed), and submit your command. Multiple commands can be used.

* `--test`, `-t`
  - Test the reminder at its current hour ("current", default value), a specific hour (number from 1-24), or all of them ("all", please don't hover over notifications or else syncing with audio will mess up). You may need to clean up your notifications afterwards.
* `--altaudio`, `-a`
  - Change the sound played by reminders from the preset sound to either the default Windows asterisk sound ("system") or none at all ("silence").
* `--ducking`, ``-d``
  - *This is experimental.* Enable ducking (lowering volume) of applications when the reminder's sound plays. Ducked volume can be specified from 0.0-1.0 (default is 0.35). *Because this is experimental, again, expect bugs, and it cannot restore volumes of apps closed during the sound's playing. The docking feature is more advanced and has required assistance from AI to implement quickly, and I don't have time to learn more about programming it. Please check the volume mixer if the audio on the computer sounds off.*
 
*If you are using the executable itself, because of how the pyinstaller library works, you cannot get printed statements in the console, nor use Ctrl+C to terminate it. (I tried implementing the latter and it was too hard, even with AI's assistance.) If you are testing all reminders, use Task Manager to terminate the program.*

# Giving feedback
If you have encountered a bug or would like to suggest an idea, please post in the [issues page](https://github.com/PrincessPandaSource/Hourly-Reminder/issues). Give as much detail as necessary, such as what exactly caused the bug or what you would exactly want. Since this is a minor project, bug reports, especially of critical ones, will have higher priority than suggestions.

If you have programming experience, you may consider cloning this repository onto your machine and making a pull request of your changes.

Considering potentially common feedback:
* I currently have no idea how to make it so that the notification shows Hourly Reminder is the program it's from, not Command Prompt. I used the custom script from the windows_toasts library that registers a custom app ID, but I couldn't get it to work.
* In the future, I could not only update this program with my own art, but have the default assets be freely licensed icons and clips of royalty-free music instead of *Sonic* icons and song clips. (Previous assets used could still be stored in a separate folder.)

# Credits and copyright
Source code is licensed under the [MIT License](https://github.com/PrincessPandaSource/Hourly-Reminder/blob/main/LICENSE).

While I wrote the code in my own words, the implementations of more advanced features, such as audio docking, multithreading with COM, and program optimization, were initially coded by the LLMs Claude Sonnet 4, Gemini 2.5 Pro, and GPT-5 via GitHub Copilot. (They were beyond my skill level, and I didn't have time to learn them by myself.)

The *Sonic the Hedgehog* icons (from the [Sega's Sonic the Hedgehog](https://sonic.fandom.com/wiki/Sega%27s_Sonic_the_Sketchog) digital sticker collection) and song clips (from various games) are owned and copyrighted by Sega.
