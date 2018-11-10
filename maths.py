def binomialTheorem (n, k):
    """Returns n choose k"""
    if k == 0:
        return 1
    if n == k:
        return 1
    else:
        return binomialTheorem(n-1, k-1) + binomialTheorem(n-1, k)


def percent(a, b):
    """Returns a% of b"""
    return a/100 * b

