from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from bs4 import BeautifulSoup
import requests


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


def stats(request):
    print("stats is called")
    cf_handle = request.POST['handle']
    all_data = get_data(cf_handle)
    return render(request, 'result.html', all_data)


def get_data(handle):
    all_data = {}

    # info = get_info(handle)
    # ratings = get_contest_ratings(handle)
    # problems = get_problems(handle)
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
        print(new_rating,  contest_name)

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
    problems = {}

    n = 0  # number of submission
    for i in range(1, total_pages+1):
        curr_url = url + "/page/" + str(i)
        print(curr_url)
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
            bigId = row_as_list[3].find("a")['href']
            lang = row_as_list[4].text.strip()
            sub = row_as_list[4].text.strip()
            l = 0
            qId = get_qId(bigId)
            tos = get_tos(sub[0])  # type of submission

            print(qId + " " + tos + " " + lang)
            s = Submission(tos, lang)
            n += 1
            if qId in problems:
                problems[qId].append(s)
            else:
                problems[qId] = [s]

            # table.append(s)
    print("Total number of submissions : " + str(n) +
          "\nTotal number of problems attempted : " + str(problems.__len__()))
    return problems


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
    bigId = bigId.strip()
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
