# GitHub Reminder Bot and Utilities

## Basic Usage

The main script, which can be run as a standalone, is `bots.py`.

Usage: `python bots.py -t YOURTOKEN -o YOURORGANIZATION`

## Scheduling

If you would like to run the GitHub reminder bot on a recurring basis, you have a couple of options:

1. Use the out of the box scheduler script and Hacktoolkit's scheduling system, `tasks.py`:
   Create a Python script that will execute in a loop, optionally using [Supervisor](http://supervisord.org/)

   ```
   import time
   
   while True:
       GitHubReminderTask().execute_batch()
       time.sleep(60 * 60)
   ```

2. Write a wrapper shell script that invokes `bots.py` with the correct arguments, schedule it with something like `crontab`
