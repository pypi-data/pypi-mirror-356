"""
@Author: 虾仁 (chocolate)
@Email: neihanshenshou@163.com
@File: CleanDependence.py
@Time: 2024/3/25 21:29
"""
from __future__ import print_function

import optparse
import subprocess
import sys

from pkg_resources import working_set, get_distribution, VersionConflict, DistributionNotFound

__version__ = "0.0.5"

# 不允许卸载
WHITELIST = ["pip", "pip3", "setuptools", "SteamedBun-Uninstall"]


def auto_remove(names, yes=False):
    dead = list_dead(names)
    names = [d.project_name for d in dead]
    print(f"你要卸载的三方库及其子依赖: {names}")
    if dead and (yes or confirm("Uninstall (Y/N) or (y/n)? ")):
        remove_dists(dead)


def list_dead(names):
    start = set()
    for name in names:
        try:

            start.add(get_distribution(name))
        except DistributionNotFound:
            print("未在pip 模块下找到 %s , 跳过" % name, file=sys.stderr)
        except VersionConflict:
            print("%s is not the currently installed version, skipping" % name, file=sys.stderr)
    graph = get_graph()
    dead = exclude_whitelist(find_all_dead(graph, start))
    for d in start:
        show_tree(d, dead)
    return dead


def exclude_whitelist(dists):
    return set(dist for dist in dists if dist.project_name not in WHITELIST)


def show_tree(dist, dead, indent=0, visited=None):
    if visited is None:
        visited = set()
    if dist in visited:
        return
    visited.add(dist)
    print(" " * 4 * indent, end="")
    show_dist(dist)
    for req in requires(dist):
        if req in dead:
            show_tree(req, dead, indent + 1, visited)


def find_all_dead(graph, start):
    return fixed_point(lambda d: find_dead(graph, d), start)


def find_dead(graph, dead):
    def is_killed_by_us(node):
        succ = graph[node]
        return succ and not (succ - dead)

    return dead | set(filter(is_killed_by_us, graph))


def fixed_point(f, x):
    while True:
        y = f(x)
        if y == x:
            return x
        x = y


def confirm(prompt):
    return input(prompt).lower() == "y"


def show_dist(dist):
    print("%s %s (%s)" % (dist.project_name, dist.version, dist.location))


def show_freeze(dist):
    print(dist.as_requirement())


def remove_dists(dists):
    if sys.executable:
        pip_cmd = [sys.executable, "-m", "pip"]
    else:
        pip_cmd = ["pip"]
    subprocess.check_call(pip_cmd + ["uninstall", "-y"] + [d.project_name for d in dists])


def get_graph():
    g = dict((dist, set()) for dist in working_set)
    for dist in working_set:
        for req in requires(dist):
            g[req].add(dist)
    return g


def requires(dist):
    required = []
    for pkg in dist.requires():
        try:
            required.append(get_distribution(pkg))
        except VersionConflict as e:
            print(e.report(), file=sys.stderr)
            print("请重新输入需要卸载的包名...(Redoing requirement with just package name...)", file=sys.stderr)
            required.append(get_distribution(pkg.project_name))
        except DistributionNotFound as e:
            print(e.report(), file=sys.stderr)
            print("跳过...(Skipping) %s" % pkg.project_name, file=sys.stderr)
    return required


def _start_remove(argv=None):
    parser = create_parser()
    (opts, args) = parser.parse_args(argv)
    if opts.leaves or opts.freeze:
        list_leaves(opts.freeze)
    elif opts.list:
        list_dead(args)
    elif len(args) == 0:
        parser.print_help()
    else:
        auto_remove(args, yes=opts.yes)


def get_leaves(graph):
    def is_leaf(node):
        return not graph[node]

    return filter(is_leaf, graph)


def list_leaves(freeze=False):
    graph = get_graph()
    for node in get_leaves(graph):
        if freeze:
            show_freeze(node)
        else:
            show_dist(node)


def create_parser():
    parser = optparse.OptionParser(
        usage="usage: %prog [OPTION]... [NAME]...",
        version="%prog " + __version__,
    )

    parser.add_option(
        "-l", "--list", action="store_true", default=False,
        help="查看指定包的依赖项, 但不会卸载...【list unused dependencies, but don't uninstall them.】")
    parser.add_option(
        '-L', '--leaves', action='store_true', default=False,
        help="查看未被其它使用的依赖...【list leaves (packages which are not used by any others).】")
    parser.add_option(
        '-y', '--yes', action='store_true', default=False,
        help="删除依赖前不会再主动询问...【don't ask for confirmation of uninstall deletions.】")
    parser.add_option(
        '-f', '--freeze', action='store_true', default=False,
        help=("将要卸载的依赖 以txt的类型文件导出..."
              "【list leaves (packages which are not used by any others) in requirements.txt format】"))
    return parser


if __name__ == '__main__':
    _start_remove()
