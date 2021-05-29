from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from bs4 import BeautifulSoup
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


class Submission:
    def __init__(self, type_of_submission, lang):
        self.type = type_of_submission
        self.lang = lang


# class Problem:
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name
#         self.submissions = []

#     def add_submission(self, sub):
#         self.submissions.append(sub)

#     def get_lang_submissions(self):
#         dict = {}
#         # for each submission:
#         #   if lang of submission exist in dict:
#         #       dict[lang]++
#         # else:
#         #   add in dict {lang : 1}
#         return dict

#     def get_type_of_submissions(self):
#         dict = {"AC": 0, "WA": 0, "RE": 0, "TLE": 0, "CE": 0}
#         # for each submission:
#         #   dict[type]++;
#         # else:
#         #    add in dict {lang : 1}
#         return dict


def index(request):
    return render(request, 'index.html')


@api_view(['GET', 'POST'])
def stats(request):
    print("stats is called")
    cf_handle = request.POST['handle']
    all_data = get_data(cf_handle)
    final_data = get_formatted_data(all_data)
    final_data["handle"] = cf_handle
    # return render(request, 'result.html', all_data)
    return Response(final_data)


def get_formatted_data(data):
    # info , rating , problems
    f_data = {}
    # done till here
    # print(data[""])
    f_data.update(data["info"])
    # f_data["problems"] = data["problems"]["problems"]
    # f_data["questions"] = data["problems"]["questions"]
    # f_data["lang_data"] = get_lang_data(data["problems"]["problems"])
    f_data["contests_list"] = data["ratings"]["ratings"]
    f_data["max_up"] = data["ratings"]["max_up"]
    f_data["max_down"] = data["ratings"]["max_down"]
    f_data["min_rank"] = data["ratings"]["min_rank"]
    f_data["max_rank"] = data["ratings"]["max_rank"]
    # print(f_data)
    return f_data

# f_data -> keys -> lang_data , contests_lists, max_up, max_down, min_rank, max_rank, proble


def get_lang_data(problems):
    lang_data = {}
    for key in problems:
        for sub in problems[key]:
            if sub.lang in lang_data:
                lang_data[sub.lang] += 1
            else:
                lang_data[sub.lang] = 1
    print(lang_data)
    return lang_data


def get_data(handle):

    info = get_info(handle)
    ratings = get_contest_ratings(handle)
    # problems = get_problems(handle)

    all_data = {
        "info": info,
        "ratings": ratings,
        # "problems": problems
    }
    return all_data


def get_info(handle):
    url = "https://codeforces.com/profile/" + handle
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    info = soup.find("div", {"class": "info"})
    user_title = info.find("div", {"class": "user-rank"}).text.strip()
    curr_rating = info.find(
        "span", {"style": "font-weight:bold;"}).text.strip()
    best_title_and_rating = info.find(
        "span", {"class": "smaller"}).text.strip()

    max_title = get_title(best_title_and_rating)
    max_rating = get_rating(best_title_and_rating)
    print(user_title, curr_rating, max_title, max_rating)
    data = {
        "user_title": user_title,
        "curr_rating": curr_rating,
        "max_title": max_title,
        "max_rating": max_rating
    }
    return data


def get_contest_ratings(handle):
    # and rating after each contest (value) in chronological order
    max_up = 0
    max_down = 0
    max_rank = 0
    min_rank = 1000000
    url = "https://codeforces.com/contests/with/" + handle
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    big_table = soup.find("div", {"class": "datatable"})
    curr_table = big_table.find("table").find("tbody").find_all("tr")

    data = {
        "ratings": {},
    }

    for row in curr_table:
        row_as_list = row.find_all("td")

        contest_name = row_as_list[1].text.strip()
        new_rating = int(row_as_list[6].text.strip())

        max_up = max(max_up, int(row_as_list[5].text.strip()))
        max_down = min(max_down, int(row_as_list[5].text.strip()))
        max_rank = max(max_rank, int(row_as_list[3].text.strip()))
        min_rank = min(min_rank, int(row_as_list[3].text.strip()))

        data["ratings"][contest_name] = new_rating

    data["max_up"] = max_up
    data["max_down"] = max_down
    data["min_rank"] = min_rank
    data["max_rank"] = max_rank
    return data


def get_problems(handle):
    # returns a dictionary of problems solved where each
    # key is question_id and each
    # value is an array of submissions of that problem

    url = "https://codeforces.com/submissions/" + handle
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.findAll("span", {"class": "page-index"})

    total_pages = int(pages[len(pages) - 1].text)
    questions = {
        "ACquestions": 0,
        "REquestions": 0,
        "TLEquestions": 0,
        "CEquestions": 0,
        "WAquestions": 0
    }
    problems = {}
    n = 0  # number of submission
    for i in range(1, total_pages+1):
        curr_url = url + "/page/" + str(i)
        response = requests.get(curr_url)
        soup = BeautifulSoup(response.text, 'lxml')
        big_table = soup.find("div", {"class": "datatable"})
        curr_table = big_table.find("table").find_all("tr")
        i = 0
        for row in curr_table:
            # index  3 ,4 ,5 define a submission
            i += 1
            if i == 1:
                continue
            j = 0
            row_as_list = row.find_all("td")
            bigId = row_as_list[3].find("a")['href'].strip()
            lang = row_as_list[4].text.strip()
            sub = row_as_list[5].text.strip()
            l = 0
            qId = get_qId(bigId)
            tos = get_tos(sub[0])  # type of submission

            s = Submission(tos, lang)
            n += 1
            if qId in problems:
                problems[qId].append(s)
            else:
                problems[qId] = [s]
            # print(tos)
            question = tos + "questions"
            questions[question] += 1
            # table.append(s)
    print(questions["ACquestions"], questions["REquestions"],
          questions["TLEquestions"], questions["CEquestions"], questions["WAquestions"],)
    print("Total number of submissions : " + str(n) +
          "\nTotal number of problems attempted : " + str(problems.__len__()))
    data = {
        "problems": problems,
        "questions": questions
    }
    return data


# problems = {
#     "question_id 1": [
#         Submission1, Submission2, Submission3, Submission4
#     ],
#     "question_id 1": [
#         Submission1, Submission2, Submission3, Submission4
#     ],
#     "question_id 3": [
#         Submission1, Submission2, Submission3, Submission4
#     ]
# }
#
# Submission.type = {WA, AC, RE, TLE, CE}
# Submission.lang = {Java, C++, Python}

def get_qId(bigId):
    bigId = bigId[9:]
    l = 0
    for c in bigId:
        if c.isalnum():
            l += 1
        else:
            break
    qId = bigId[0:l] + " " + bigId[l+9:]
    return qId


def get_tos(c):
    if(c == 'A'):
        tos = "AC"
    elif(c == 'T'):
        tos = "TLE"
    elif(c == 'R'):
        tos = "RE"
    elif(c == 'W'):
        tos = "WA"
    else:
        tos = "CE"
    return tos


def get_title(title_and_rating):
    idx = 0
    for i in range(6, len(title_and_rating)):
        if not (title_and_rating[i].isalpha()):
            idx = i
            break

    title = title_and_rating[6: int(idx)].capitalize()
    return title


def get_rating(title_and_rating):
    idx = 0
    for i in range(6, len(title_and_rating)):
        if not (title_and_rating[i].isalpha()):
            idx = i
            break

    rating = title_and_rating[idx+3: -1]
    return rating

# data = {
#     "problems" : {
#         "question_id 1": [
#             Submission1, Submission2, Submission3, Submission4
#         ],
#         "question_id 1": [
#             Submission1, Submission2, Submission3, Submission4
#         ],
#         "question_id 3": [
#             Submission1, Submission2, Submission3, Submission4
#         ]
#     },
#     "key 2" : int1
# }


# @api_view()
# def hello_world(request, data):
#     return Response(data)
