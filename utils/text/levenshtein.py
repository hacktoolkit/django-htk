# Third Party (PyPI) Imports
import numpy


def levenshtein(w1, w2):
    """The Levenshtein distance algorithm that compares two words

    https://en.wikipedia.org/wiki/Levenshtein_distance

    Returns an `int` representing the edit distance between two words
    """
    a = 0
    b = 0
    c = 0
    edit_distance = numpy.zeros((len(w1) + 1, len(w2) + 1))

    for x in range(len(w1) + 1):
        edit_distance[x][0] = x

    for y in range(len(w2) + 1):
        edit_distance[0][y] = y

    for x in range(1, len(w1) + 1):
        for y in range(1, len(w2) + 1):
            if (w1[x-1] == w2[y-1]):
                edit_distance[x][y] = edit_distance[x - 1][y - 1]
            else:
                a = edit_distance[x][y - 1]
                b = edit_distance[x - 1][y]
                c = edit_distance[x - 1][y - 1]

                if (a <= b and a <= c):
                    edit_distance[x][y] = a + 1
                elif (b <= a and b <= c):
                    edit_distance[x][y] = b + 1
                else:
                    edit_distance[x][y] = c + 1

    return edit_distance[len(w1)][len(w2)]
