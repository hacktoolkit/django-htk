# Third Party (PyPI) Imports
import numpy


def levenshtein_distance(w1, w2):
    """The Levenshtein distance algorithm that compares two words

    https://en.wikipedia.org/wiki/Levenshtein_distance

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
                insertion_cost = edit_distance[x][y - 1] + 1
                deletion_cost = edit_distance[x - 1][y] + 1
                substitution_cost = edit_distance[x - 1][y - 1] + 1

                edit_distance[x][y] = min(
                    deletion_cost,
                    insertion_cost,
                    substitution_cost
                )

    result = edit_distance[len(w1)][len(w2)]
    return result


def get_closest_dict_words(word, dict_words, num_results=20):
    """Uses the Levenshtein distance for Word Autocompletion and Autocorrection

    https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
    """
    dict_word_distances = []
    distances = []
    greatest_distance_allowed = None

    for dict_word in dict_words:
        word_distance = levenshtein_distance(word, dict_word)

        if greatest_distance_allowed is not None and word_distance > greatest_distance_allowed:
            # skip this word, because it cannot be among the closest words
            pass
        else:
            dict_word_distances.append((word_distance, dict_word, ))

            distances.append(word_distance)
            distances.sort()
            if len(distances) >= num_results:
                distances = distances[:num_results]
                greatest_distance_allowed = distances[-1]

    dict_word_distances.sort(key=lambda x: x[0])

    closest_words = [
        dict_word_distances[i][1]
        for i in range(num_results)
        if greatest_distance_allowed is None or dict_word_distances[i][0] <= greatest_distance_allowed
    ]

    return closest_words
