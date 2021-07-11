# CF-Scraper

A Codeforces Scraper that visually represents your codeforces submissions and contests data.


## How to run:

Clone or download the repo.
Make sure you have python installed and then run the following commanding to install all the dependencies

```pip install -r requirements.txt```

Change directory to the main project folder 'CF_Scraper' and run the following command:

```python manage.py runserver```

## Tech Stack:

* Django Framework
* *django.sqlite3* Database
* HTML, CSS and Bootstrap for frontend
* Ajax used to asynchronously call the API views created using Django-Rest Framework
* beautifulsoup4 for scraping codeforces.com
* chart.js for generating the graphs/charts

## Future Work:

* Add more data regarding problems and topics
* Use the submissions data to predict topics that need more work
* Add data regarding other platforms to further improve our predictions
