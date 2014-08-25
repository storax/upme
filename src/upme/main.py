import pkg_resources


def get_required(dist):
    """Return a set with all distributions that are required of dist

    This also includes subdependencies and the given distribution.

    :param dist: the distribution to query. Can also be the name of the distribution
    :type dist: :class:`pkg_resources.Distribution` | str
    :returns: a list of distributions
    :rtype: set of :class:`pkg_resources.Distribution`
    :raises: None
    """
    d = pkg_resources.get_distribution(dist)
    reqs = set(d.requires())
    allds = set([d])
    while reqs:
        newreqs = set([])
        for r in reqs:
            dr = pkg_resources.get_distribution(r)
            allds.add(dr)
            newreqs = newreqs & set(dr.requires())
        reqs = newreqs - reqs
    return allds
