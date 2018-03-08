"""
    Tim Coutinho
    Prof. Rhodes
    Implementation of the quicksort algorithm in Python, along with
    an algorithm to find the closest set of points in 1-D space.
"""

from random import randrange, uniform


def quicksort(l, pivot=0):
    """Basic quicksort implementation. Sorts a list around a pivot, which
       is the first value in the list by default. O(nlogn), but technically
       O((2n)logn) due to the way the less than and greater than values are
       found."""
    if not l:  # List is empty, done recursing
        return []
    less = [i for i in l[1:] if i <= l[pivot]]
    greater = [i for i in l[1:] if i > l[pivot]]
    # print(l, '->', less, greater)  # Uncomment to show intermediate steps
    # Sort all values less or greater than the pivot
    less = quicksort(less)
    # Sort all values greater than the pivot
    greater = quicksort(greater)
    # Unpacks each list, placing all values into the final ordered list
    return [*less, l[pivot], *greater]
    # vvv Uncomment for nifty one liner version instead
    # return [] if not l else [*quicksort([i for i in l[1:] if i <= l[pivot]]), l[pivot], *quicksort([i for i in l[1:] if i > l[pivot]])]


def closest_pair(l):
    """ Finds the closest pair of points in 1-D space via a divide and conquer
        method. List is sorted prior to calling initial function. O(nlogn)."""
    if len(l) == 1:
        return (l[0], l[0], 1)
    if len(l) == 2:
        return (l[1] - l[0], (l[0], l[1]), 1)
    left = l[:len(l)//2]
    right = l[len(l)//2:]
    left_v = closest_pair(l[:len(l)//2])
    right_v = closest_pair(l[len(l)//2:])
    # Pretty ugly, but just finds the distance between the rightmost left
    # value and the leftmost right value, this is where the presorting helps
    this = (right[0] - left[len(left)-1],
            (left[len(left) - 1], right[0]), left_v[2] + right_v[2])
    smallest = min(left_v[0], right_v[0], this[0])
    # Use the smallest of the three as the return value, can't just return
    # based on min due to needing to compare and return different things
    if smallest == left_v[0]:
        return (left_v[0], left_v[1], this[2])
    elif smallest == right_v[0]:
        return (right_v[0], right_v[1], this[2])
    else:
        return this


def closest_pair_naive(l):
    """A version of closest pair that instead simply iterates through the
       list pairwise and compares differences. Also O(nlogn) due to sorting."""
    l = quicksort(l)[0]  # Sorting done again here just to be explicit
    ret = ()
    smallest = ((), 100)
    for pair in zip(l, l[1:]):
        dif = pair[1] - pair[0]
        if dif < smallest[1]:
            smallest = (pair, dif)
    return smallest[0]


def main():
    # Various different lengths/types of lists
    l10 = [randrange(101) for i in range(10)]
    l10f = [uniform(0, 100) for i in range(10)]
    l20 = [randrange(101) for i in range(20)]
    l100 = [randrange(101) for i in range(100)]
    l100f = [uniform(0, 100) for i in range(100)]

    l = l10f  # Change to desired list to use
    qsl = quicksort(l)
    print(l, '->', qsl)
    closest = closest_pair(quicksort(l))
    print(f'Closest pair: {closest[1]}\nTotal calls: {closest[2]}')


if __name__ == '__main__':
    main()
