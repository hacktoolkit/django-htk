# Third Party (PyPI) Imports
import numpy


def getLevenshteinDistance(job_title, title_from_json):
    """The Levenshtein distance algorithm that compares two words.

    Returns a numeric value representing the distance between two words.
    """
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
