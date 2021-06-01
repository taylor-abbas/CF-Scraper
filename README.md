# CF-Crawler

A very basic Codeforces Crawler that visually represents your codeforces submissions and contests data.


## How to run:

Clone or download the repo.
Make sure you have python installed and then run the following commanding to install all the dependencies

```pip install -r requirements.txt```

Change directory to the main project folder 'CF_Crawler' and run the following command:

```python manage.py runserver```

## Tech Stack:

* Django Framework
* HTML, CSS and Bootstrap for frontend
* Ajax used to asynchronously call the API views created using Django-Rest Framework
* beautifulsoup4 for scraping codeforces.com
* chart.js for generating the graphs/charts
