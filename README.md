# Transportation Trip Tracker

https://youtu.be/CV11jQIZomU

#### Description:

Transportation Trip Tracker is a Python program that helps a driver organize trips and keep track of basic transportation records. I chose this project because transportation is something I have experience with, and I wanted to build a program that connects to a real task. Keeping trip information in different places can make it difficult to find a passenger's destination or calculate how much money completed trips brought in. This program brings that information together in one simple menu.

The program allows the user to add a trip with a date, passenger name or alias, destination, mileage, and fare. Each new trip receives its own identification number and starts with a Scheduled status. The user can view all trips, search for a passenger or destination, and change a trip to Scheduled, Completed, or Cancelled. Search is not case sensitive, so typing a name in lowercase still finds a record entered with capital letters. Trips are displayed in date order to make the list easier to follow.

Another feature is the summary report. It shows the total number of trips and how many are in each status. It also calculates the mileage and revenue for completed trips. Scheduled and cancelled trips are excluded from those totals because their fares should not be counted as completed work. When completed mileage is greater than zero, the program calculates revenue per mile. This figure is revenue, rather than profit, because the program does not subtract fuel, maintenance, insurance, or other expenses.

## Running the project

Install Python 3.10 or newer, extract this folder, and open a terminal in the folder containing TermProject.py. On Windows, enter:

```text
py TermProject.py
```

On systems where Python is available as python3, enter:

```text
python3 TermProject.py
```

Choose a menu option from 1 through 7 and follow the prompts. No package installation is needed. Use option 7 to save and exit. The program also saves after adding a trip or updating a status. Use fictional passenger information when demonstrating the project for class.

## Project files

- **TermProject.py** contains the application, including the Trip class, main function, input validation, menu actions, calculations, and file operations.
- **requirements.txt** states that no third-party packages are required. All imported modules come with Python.
- **README.md** explains the purpose, setup, features, files, and design decisions.
- **VIDEO_GUIDE.md** provides an introduction template, a timed demonstration outline, and a submission checklist. It is a preparation guide, not a finished recording.
- **Video_Link.md** is the document where the actual video URL must be entered after uploading the recording.
- **test_project.py** contains automated checks for saving and loading records, invalid stored data, summary calculations, and CSV output. Run it with `py -m unittest test_project.py` or `python3 -m unittest test_project.py`.
- **trips.json** is created when the program saves. It stores trip records between sessions. It is intentionally not included with personal or sample records.
- **trip_report.csv** is created when the user selects Export CSV. It contains the current records in a format that spreadsheet programs can open.

## Design decisions and course skills

I used a text menu because it keeps the program easy to run and lets me focus on the Python concepts from this course. The main function controls the menu, while separate functions handle tasks such as adding trips, searching records, saving data, and showing summaries. These functions are defined at the same indentation level as main. This structure makes the code easier to read and helps keep each function focused on one job.

The Trip class applies object-oriented programming by combining a trip's information with behavior. Its complete method changes a trip to Completed, and its validation checks the values used to create an object. A list holds the Trip objects while the application is running. Loops repeat the menu and process records, while conditional statements decide which action to perform and which trips belong in a report.

For error handling, the program rejects blank required fields, invalid dates, negative numbers, and nonnumeric entries. It handles invalid menu options without closing. File errors produce a message so the user can understand what happened. If an existing JSON file is unreadable or contains invalid records, the program stops rather than overwriting that file with empty data. Saving writes to a temporary file first and then replaces the original, reducing the chance of leaving a partially written data file.

I used json for persistent storage, csv for exporting reports, datetime for checking dates, pathlib for file paths, dataclasses for the Trip object, and decimal for money calculations. Decimal avoids the small binary floating-point differences that can occur when adding currency values. Saving beside the Python file also makes the data location predictable. This is a classroom application for one user, so it does not include authentication, encryption, multiple-user access, route mapping, or automatic backups. Those would be possible improvements after the core features are working.
