import os
import sys

import pip
import pkg_resources


def get_required(dist):
    """Return a set with all distributions that are required of dist

    This also includes subdependencies and the given distribution.

    :param dist: the distribution to query. Can also be the name of the distribution
    :type dist: :class:`pkg_resources.Distribution` | str
    :returns: a list of distributions that are required including the given one
    :rtype: set of :class:`pkg_resources.Distribution`
    :raises: class:`pkg_resources.DistributionNotFound`
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


def is_outdated(dist, dep=False):
    """Return a dict with outdated distributions

    If the given distribution has dependencies, they are checked as well.

    :param dist: a distribution to check
    :type dist: :class:`pkg_resources.Distribution` | str
    :param dep: If True, also return all outdated dependencies. If False, only check given dist.
    :type dep:
    :returns: dictionary of all distributions that are outdated and are either dependencies
              of the given distribution or the distribution itself.
              Keys are the outdated distributions
              and values are the newest parsed versions.
    :rtype: dict of :class:`pkg_resources.Distribution`
    :raises: class:`pkg_resources.DistributionNotFound`
    """
    if dep:
        required = get_required(dist)
    else:
        required = set([dist])
    ListCommand = pip.commands['list']
    lc = ListCommand()
    options, args = lc.parse_args(['--outdated'])
    outdated = {}
    for d, raw_ver, parsed_ver in lc.find_packages_latests_versions(options):
        for r in required:
            if d.project_name == r.project_name and parsed_ver > r.parsed_version:
                outdated[r] = parsed_ver
    return outdated


def update(dist, args=None):
    """Update the given distribution and all of its dependencies

    :param dist: the distribution to check
    :type dist: :class:`pkg_resources.Distribution` | str
    :param args: extra arguments for the install command.
                 this is somewhat equivalent to: pip install -U <dist> args
    :type args: list
    :returns: None
    :rtype: None
    :raises: class:`pkg_resources.DistributionNotFound`
    """
    dist = pkg_resources.get_distribution(dist)
    InstallCommand = pip.commands['install']
    ic = InstallCommand()
    iargs = ['-U', dist.project_name]
    if args:
        iargs.extend(args)
    ic.main(iargs)


def restart():
    """Restart the application the same way it was started

    :returns: None
    :rtype: None
    :raises: SystemExit
    """
    python = sys.executable
    os.execl(python, python, * sys.argv)
