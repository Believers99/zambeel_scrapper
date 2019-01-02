Zambeel Scrapper
===================

This is a very rudimentary web scraping tool built to extract course timing and location information from my university portal and add these as events in my Google calendar. 

The Selenium code is pretty janky adn the calendar event code has hard coded lists for the number of courses I had in the semester I made this. Needless to say this is not the programming standard anyone should aspire to.

##### Requirements

- `chromedriver.exe` should be in the root directory (or any other place which selenium can detect)
- `keys.py` should be in the root directory and look something like this
``` python
user_id = 'XXXXX'
password = 'XXXXXX'
CALENDAR_KEY = 'XXXXXXXX@group.calendar.google.com'
```
