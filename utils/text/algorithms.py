# Python Standard Library Imports
from typing import Iterable, List, Optional, Tuple

# Third Party (PyPI) Imports
import numpy


def levenshtein_distance(w1: str, w2: str) -> int:
    """Return the Levenshtein edit distance between two strings.

    The distance is the minimum number of insertions, deletions, or
    substitutions needed to change ``w1`` into ``w2``.

    See: https://en.wikipedia.org/wiki/Levenshtein_distance
    See: https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
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
            if w1[x - 1] == w2[y - 1]:
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

    result = int(edit_distance[len(w1)][len(w2)])
    return result


def get_closest_dict_words(
    word: str,
    dict_words: Iterable[str],
    num_results: int = 20,
) -> List[str]:
    """Uses the Levenshtein distance for Word Autocompletion and Autocorrection

    https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
    """
    dict_word_distances: List[Tuple[int, str]] = []
    distances: List[int] = []
    greatest_distance_allowed: Optional[int] = None

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
        dict_word
        for distance, dict_word
        in dict_word_distances[:num_results]
    ]

    return closest_words
