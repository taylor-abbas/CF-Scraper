from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from bs4 import BeautifulSoup
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

user_name = "taylor_abbas"


def index(request):
    return render(request, 'index.html')


def stats(request):
    print("stats is called")
    cf_handle = request.POST['handle']
    global user_name
    user_name = cf_handle
    info = get_info(cf_handle)
    return render(request, 'result.html', info)
    # return Response(final_data)


@api_view(['GET', 'POST'])
def create_info_api_view(request):
    dict = get_info(user_name)
    return Response(dict)


@api_view(['GET', 'POST'])
def create_contests_api_view(request):
    dict = get_contest_ratings(user_name)["ratings"]
    labels = list(dict.keys())
    print(labels[0])
    labels.reverse()
    print(labels[0])
    vals = list(dict.values())
    vals.reverse()
    data = {
        "labels": labels,
        "values": vals
    }
    return Response(data)


@api_view(['GET', 'POST'])
def create_submissions_api_view(request):
    dict = get_submissions_data(user_name)["submissions"]
    data = {
        "labels": list(dict.keys()),
        "values": list(dict.values())
    }
    return Response(data)


@api_view(['GET', 'POST'])
def create_languages_api_view(request):
    dict = get_submissions_data(user_name)["lang_data"]
    data = {
        "labels": list(dict.keys()),
        "values": list(dict.values())
    }
    return Response(data)


@api_view(['GET', 'POST'])
def create_problems_api_view(request):
    dict = get_submissions_data(user_name)["unsolved"]
    labels = list(dict.keys())
    labels.reverse()
    vals = list(dict.values())
    data = {
        "labels": labels,
        "values": vals
    }
    return Response(data)


# def charts(request):
#     print("charts is called")
#     # cf_handle = request.POST['handle']
#     global handle
#     cf_handle = handle
#     # all_data = get_data(cf_handle)
#     return render(request, 'result.html')
#     # return Response(final_data)


# def get_formatted_data(data):
#     # info , rating , problems
#     f_data = {}
#     # done till here
#     # print(data[""])
#     f_data.update(data["info"])
#     f_data["problems"] = data["problems"]["problems"]
#     f_data["questions"] = data["problems"]["questions"]
#     f_data["contests_list"] = data["ratings"]["ratings"]
#     f_data["max_up"] = data["ratings"]["max_up"]
#     f_data["max_down"] = data["ratings"]["max_down"]
#     f_data["min_rank"] = data["ratings"]["min_rank"]
#     f_data["max_rank"] = data["ratings"]["max_rank"]
#     # print(f_data)
#     return f_data

# f_data -> keys -> lang_data , contests_lists, max_up, max_down, min_rank, max_rank, proble


# def get_data(handle):

#     # basic info of the user
#     info = get_info(handle)

#     # dict of contest : new_rating
#     ratings = get_contest_ratings(handle)

#     submissions_data = get_submissions_data(handle)
#     submissions = submissions_data["submissions"]
#     lang_data = submissions_data["lang_data"]
#     unsolved = submissions_data["unsolved"]

#     pass


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
        "max_rating": max_rating,
        "handle": handle
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
        contest_name = contest_name.replace("Codeforces Round", "CF")
        contest_name = contest_name.replace("Educational", "Edu")
        contest_name = contest_name.replace("Rated for", "")

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


def get_submissions_data(cf_handle):
    # returns a dictionary of problems solved where each
    # key is question_id and each
    # value is an array of submissions of that problem

    url = "https://codeforces.com/submissions/" + cf_handle
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.findAll("span", {"class": "page-index"})
    print(type(pages), len(pages))
    total_pages = int(pages[len(pages) - 1].text)
    submissions = {
        "AC": 0,
        "RE": 0,
        "TLE": 0,
        "CE": 0,
        "WA": 0
    }
    lang_data = {}
    unsolved_problems = {}
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
            idx = get_idx(sub[0])
            n += 1

            if lang in lang_data:
                lang_data[lang] += 1
            else:
                lang_data[lang] = 1

            if qId in unsolved_problems:
                unsolved_problems[qId][idx] += 1
            else:
                unsolved_problems[qId] = [0, 0, 0, 0, 0]
                unsolved_problems[qId][idx] += 1

            submissions[tos] += 1

    problems = {}
    for key in unsolved_problems:
        if unsolved_problems[key][0] == 0:
            problems[key] = 1
    print("Total number of submissions : " + str(n))
    data = {
        "unsolved": problems,
        "submissions": submissions,
        "lang_data": lang_data
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


def get_idx(c):
    if(c == 'A'):
        idx = 0
    elif(c == 'W'):
        idx = 1
    elif(c == 'R'):
        idx = 2
    elif(c == 'T'):
        idx = 3
    else:
        idx = 4
    return idx


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
        if (title_and_rating[i] == ','):
            idx = i
            break

    title = title_and_rating[6: int(idx)].capitalize()
    return title


def get_rating(title_and_rating):
    idx = 0
    for i in range(6, len(title_and_rating)):
        if (title_and_rating[i] == ','):
            idx = i
            break

    rating = title_and_rating[idx+3: -1]
    return rating
