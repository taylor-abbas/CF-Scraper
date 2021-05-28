from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from bs4 import BeautifulSoup
import requests


class Submission:
    def __init__(self, id, type_of_submission, lang):
        self.question_id = id
        self.type = type_of_submission
        self.lang = lang


class Problem:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.submissions = []

    def add_submission(self, sub):
        self.submissions.append(sub)

    def get_lang_submissions(self):
        dict = {}
        # for each submission:
        #   if lang of submission exist in dict:
        #       dict[lang]++
        # else:
        #   add in dict {lang : 1}
        return dict

    def get_type_of_submissions(self):
        dict = {"AC": 0, "WA": 0, "RE": 0, "TLE": 0, "NOT_DEFINED": 0}
        # for each submission:
        #   dict[type]++;
        # else:
        #    add in dict {lang : 1}
        return dict


def index(request):
    return render(request, 'index.html')


def stats(request):
    print("stats is called")
    cf_handle = request.POST['handle']
    all_data = get_data(cf_handle)
    return render(request, 'result.html', all_data)


def get_data(handle):
    all_data = {}
    # get last 10 contest ratings
    # ratings = get_contest_ratings(handle)
    problems = get_problems(handle)
    return all_data


def get_contest_ratings(handle):
    # returns a dictionary of last 10 contests given (key)
    # and rating after each contest (value) in chronological order
    pass


def get_problems(handle):
    # returns an array of problems solved
    # where each element is an object of class - problem
    url = "https://codeforces.com/submissions/" + handle
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.findAll("span", {"class": "page-index"})
    # print("*********************")
    # print(str(pages))

    total_pages = 1

    for li in pages:
        num = li.text
        if(len(num) == 1):
            total_pages = int(num)

    problems = {}
    submissions = []
    table = []

    # completed till here

    for i in range(1, total_pages+1):
        curr_url = url + "/page/" + str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        curr_table = soup.find(
            "table", {"class": "status-frame-datatable"}).get("tbody")
        for i in range(1, curr_table.size()):
            # index  3 ,4 ,5 define a submission
            qId = curr_table[i][3].href
            sub = curr_table[i][5].text
            lang = curr_table[i][4].text
            tos = ""
            if(sub[0] == 'A'):
                tos = "AC"
            elif(sub[0] == 'T'):
                tos = "TLE"
            elif(sub[0] == 'R'):
                tos = "RE"
            elif(sub[0] == 'W'):
                tos = "WA"
            else:
                tos = "NOT_DEFINED"

            print(qId, tos, lang)
            s = Submission(qId, tos, lang)
            table.append(s)
    return problems
