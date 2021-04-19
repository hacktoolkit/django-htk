# Third Party (PyPI) Imports
import numpy


EXTRACTED_JOB_TITLES_FILE_PATH = 'zippy/ml/data/job_titles.json'
MAX_MATCHED_TITLES = 5


def normalize_job_title(job_title):
    normalized_job_title = get_job_title_matches(job_title)
    return normalized_job_title


def get_job_title_matches(job_title):
    job_titles_list = []
    matched_job_titles_list = []

    with open(EXTRACTED_JOB_TITLES_FILE_PATH) as f:
        job_titles = f.readlines()

    for title in job_titles:
        job_title_distance = getLevenshteinDistance(job_title, title.strip())
        if job_title_distance >= 10:
            job_title_distance = 9
        job_titles_list.append(str(int(job_title_distance)) + "-" + title.strip())
    job_titles_list.sort()

    for i in range(MAX_MATCHED_TITLES):
        matched_job_titles_list.append(job_titles_list[i].split("-")[1])
    return matched_job_titles_list[0]


def getLevenshteinDistance(job_title, title_from_json):
    a = 0
    b = 0
    c = 0
    title_distance = numpy.zeros((len(job_title) + 1, len(title_from_json) + 1))

    for x in range(len(job_title) + 1):
        title_distance[x][0] = x

    for y in range(len(title_from_json) + 1):
        title_distance[0][y] = y

    for x in range(1, len(job_title) + 1):
        for y in range(1, len(title_from_json) + 1):
            if (job_title[x-1] == title_from_json[y-1]):
                title_distance[x][y] = title_distance[x - 1][y - 1]
            else:
                a = title_distance[x][y - 1]
                b = title_distance[x - 1][y]
                c = title_distance[x - 1][y - 1]

                if (a <= b and a <= c):
                    title_distance[x][y] = a + 1
                elif (b <= a and b <= c):
                    title_distance[x][y] = b + 1
                else:
                    title_distance[x][y] = c + 1

    return title_distance[len(job_title)][len(title_from_json)]
