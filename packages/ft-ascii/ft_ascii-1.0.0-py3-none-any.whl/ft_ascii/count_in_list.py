#!/usr/bin/env python3.10

def count_in_list(lst: list, element):
    """
Return how many times 'element' appears in 'lst'.
Only here as an example function to be called by other scripts.
    """

    result = 0
    for i in lst:
        if i == element:
            result += 1
    return result
