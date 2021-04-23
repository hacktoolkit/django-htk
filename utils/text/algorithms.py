# Third Party (PyPI) Imports
import numpy


def levenshtein_distance(w1, w2):
    """The Levenshtein distance algorithm that compares two words

    https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

    Returns an `int` representing the edit distance between two words
    """
    insertion_cost = 0
    deletion_cost = 0
    substitution_cost = 0
    edit_distance = numpy.zeros((len(w1) + 1, len(w2) + 1))

    for x in range(len(w1) + 1):
        edit_distance[x][0] = x

    for y in range(len(w2) + 1):
        edit_distance[0][y] = y

    for x in range(1, len(w1) + 1):
        for y in range(1, len(w2) + 1):
            if (w1[x - 1] == w2[y - 1]):
                edit_distance[x][y] = edit_distance[x - 1][y - 1]
            else:
                insertion_cost = edit_distance[x][y - 1]
                deletion_cost = edit_distance[x - 1][y]
                substitution_cost = edit_distance[x - 1][y - 1]

                min_cost = min(deletion_cost, insertion_cost, substitution_cost)
                edit_distance[x][y] = min_cost + 1

    result = edit_distance[len(w1)][len(w2)]
    return result
