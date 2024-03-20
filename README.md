# Overview
The goal of this project is to find a DPS appointment using a bot, so I don't have to manually refresh the page for a newer appointment. The bot will send an email whenever a new appointment is available, to which I can then get on the DPS website and schedule an appointment with. This was done using Selenium, BeautifulSoup, and Python.


### The Process
  - The bot fills in the required information using fake information.
  - It then navigates the website and clicks buttons until it gets to the location page
  - It then fills in the requested zip code and clicks the next button
  - After filling in the zip code, it will compare the date with the current date set by the user.
  - If the date is earlier, then it will email the user with the earlier date and the first time slot available for that day
  - After emailing a user, it will sleep for 5 minutes before running again to see if there is an earlier date 
