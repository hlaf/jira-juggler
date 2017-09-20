"""
Filename: matchfuncs.py
Author: Yoshiasa Ogawa
LastModified: 29/10/2015

Functions for matching algorithms.
"""
from __future__ import division
import numpy as np
import itertools
import gambit
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

def DA(prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None):
    """
    Deffered Acceptance Algorithm

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
      Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
      Preference of respondants
    prop_caps : list
      Capacity of proposers
    resp_caps : list
      Capacity of respondants

    Returns
    ---
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_indptr : ndarray(int, ndim=1)
        Index Pointer for proposers
    resp_indptr : ndarray(int, ndim=1)
        Index Pointer for respondants

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_matched = np.zeros(sum(prop_caps), dtype=int) + prop_unmatched
    resp_matched = np.zeros(sum(resp_caps), dtype=int) + resp_unmatched
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    propcaps_rest = [i for i in prop_caps]
    respcaps_rest = [i for i in resp_caps]
    prop_single = range(prop_num)
    prop_counter = [0 for i in range(prop_num)]
    if list_length is None:
        l_length = prop_prefs.shape[1]
    else:
        l_length = list_length

    while len(prop_single) >= 1:
        prop_single_roop = [i for i in prop_single]
        for prop_id in prop_single_roop:
            if prop_counter[prop_id] == l_length:
                prop_single.remove(prop_id)
                break
            resp_id = prop_prefs[prop_id][prop_counter[prop_id]]
            prop_counter[prop_id] += 1
            if resp_id == prop_unmatched:
                prop_single.remove(prop_id)
            elif respcaps_rest[resp_id] >= 1:
                propcaps_rest[prop_id] -= 1
                respcaps_rest[resp_id] -= 1
                prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                if propcaps_rest[prop_id] == 0:
                    prop_single.remove(prop_id)
            else:
                deffered = resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]]
                max_rank = max([resp_ranks[resp_id][i] for i in deffered])
                max_id = resp_prefs[resp_id][max_rank]
                if resp_ranks[resp_id][prop_id] < max_rank:
                    if max_id not in prop_single:
                        prop_single.append(max_id)
                    propcaps_rest[max_id] += 1
                    propcaps_rest[prop_id] -= 1
                    prop_matched[np.where(prop_matched[prop_indptr[max_id]:prop_indptr[max_id+1]] == resp_id)[0][0] + prop_indptr[max_id]] = prop_unmatched
                    prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                    resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == max_id)[0][0] + resp_indptr[resp_id]] = prop_id
                    if propcaps_rest[prop_id] == 0:
                        prop_single.remove(prop_id)

    if switch == 0:
        return prop_matched, resp_matched
    elif switch == 1:
        return prop_matched, resp_matched, resp_indptr
    else:
        return prop_matched, resp_matched, prop_indptr, resp_indptr

def BOS(prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None, interview=None):
    """
    Boston School Algorithm

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants

    Returns
    ---
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_indptr : ndarray(int, ndim=1)
        Index Pointer for proposers
    resp_indptr : ndarray(int, ndim=1)
        Index Pointer for respondants

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_matched = np.zeros(sum(prop_caps), dtype=int) + prop_unmatched
    resp_matched = np.zeros(sum(resp_caps), dtype=int) + resp_unmatched
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    propcaps_rest = [i for i in prop_caps]
    respcaps_rest = [i for i in resp_caps]
    prop_single = range(prop_num)
    prop_prefsptr = [0 for i in range(prop_num)]
    prop_counter = [0 for i in range(prop_num)]
    if list_length is None:
        l_length = prop_prefs.shape[1]
    else:
        l_length = list_length
    interview_num = 0

    while len(prop_single) >= 1:
        prop_single_copy = [i for i in prop_single]
        approach = np.zeros(resp_num)
        for prop_id in prop_single_copy:
            if prop_counter[prop_id] == l_length:
                prop_single.remove(prop_id)
                continue
            if prop_prefsptr[prop_id] == prop_prefs.shape[1]:
                prop_single.remove(prop_id)
                continue
            resp_id = prop_prefs[prop_id][prop_prefsptr[prop_id]]
            if resp_id == prop_unmatched:
                prop_single.remove(prop_id)
                continue
            while respcaps_rest[resp_id] == 0:
                prop_prefsptr[prop_id] += 1
                if prop_prefsptr[prop_id] == prop_prefs.shape[1]:
                    resp_id = prop_unmatched
                    prop_single.remove(prop_id)
                    break
                resp_id = prop_prefs[prop_id][prop_prefsptr[prop_id]]
                if resp_id == prop_unmatched:
                    prop_single.remove(prop_id)
                    break
            if resp_id != prop_unmatched:
                prop_counter[prop_id] += 1
                prop_prefsptr[prop_id] += 1
                approach[resp_id] += 1
                interview_num += 1
        prop_single_copy = [i for i in prop_single]
        for resp_id in range(resp_num):
            if respcaps_rest[resp_id] >= approach[resp_id]:
                for prop_id in prop_single_copy:
                    if prop_prefs[prop_id][prop_prefsptr[prop_id]-1] == resp_id:
                        propcaps_rest[prop_id] -= 1
                        respcaps_rest[resp_id] -= 1
                        prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                        resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                        if propcaps_rest[prop_id] == 0:
                            prop_single.remove(prop_id)
            elif respcaps_rest[resp_id] != 0:
                applicants = []
                for prop_id in prop_single_copy:
                    if prop_prefs[prop_id][prop_prefsptr[prop_id]-1] == resp_id:
                        applicants.append(prop_id)
                for k in range(resp_prefs.shape[1]):
                    prop_id = resp_prefs[resp_id][k]
                    if prop_id in applicants:
                        propcaps_rest[prop_id] -= 1
                        respcaps_rest[resp_id] -= 1
                        prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                        resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                        if propcaps_rest[prop_id] == 0:
                            prop_single.remove(prop_id)
                    if respcaps_rest[resp_id] == 0:
                        break
    if interview is not None:
        return interview_num
    if switch == 0:
        return prop_matched, resp_matched
    elif switch == 1:
        return prop_matched, resp_matched, resp_indptr
    else:
        return prop_matched, resp_matched, prop_indptr, resp_indptr

def AddBOS(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps=None, prop_caps=None, interview=None):
    """
    Additional BOS Stage after the matching given by any mechanism.

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants

    Returns
    ---
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_indptr : ndarray(int, ndim=1)
        Index Pointer for proposers
    resp_indptr : ndarray(int, ndim=1)
        Index Pointer for respondants

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    prop_ranks = np.argsort(prop_prefs)
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    propcaps_rest = [i for i in prop_caps]
    respcaps_rest = [i for i in resp_caps]
    add_prop = []
    add_resp = []
    for prop_id in range(prop_num):
        pairs = prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]]
        for pair in pairs:
            if pair != resp_num:
                propcaps_rest[prop_id] -= 1
        if propcaps_rest[prop_id] != 0:
            add_prop.append(prop_id)
    for resp_id in range(resp_num):
        pairs = resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]]
        for pair in pairs:
            if pair != prop_num:
                respcaps_rest[resp_id] -= 1
        if respcaps_rest[resp_id] != 0:
            add_resp.append(resp_id)
    add_prop_prefs = np.argsort(prop_ranks[:, add_resp])
    add_resp_prefs = np.argsort(resp_ranks[:, add_prop])

    if len(add_resp) != 0 and len(add_prop) != 0:
        approach = defaultdict()
        for prop_id in add_prop:
            counter = 0
            resp_id = add_resp[add_prop_prefs[prop_id][counter]]
            while resp_id in prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]]:
                counter += 1
                if counter == add_prop_prefs.shape[1]:
                    resp_id = resp_num
                    break
                resp_id = add_resp[add_prop_prefs[prop_id][counter]]
            approach[prop_id] = resp_id

        for resp_id in add_resp:
            applicants = [i for i in add_prop if approach[i] == resp_id]
            if respcaps_rest[resp_id] >= len(applicants):
                for prop_id in applicants:
                    propcaps_rest[prop_id] -= 1
                    respcaps_rest[resp_id] -= 1
                    prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                    resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
            else:
                for k in add_resp_prefs[resp_id]:
                    prop_id = add_prop[k]
                    if prop_id in applicants:
                        propcaps_rest[prop_id] -= 1
                        respcaps_rest[resp_id] -= 1
                        prop_matched[np.where(prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]] == prop_unmatched)[0][0] + prop_indptr[prop_id]] = resp_id
                        resp_matched[np.where(resp_matched[resp_indptr[resp_id]:resp_indptr[resp_id+1]] == resp_unmatched)[0][0] + resp_indptr[resp_id]] = prop_id
                    if respcaps_rest[resp_id] == 0:
                        break
    if interview is not None:
        return len(add_prop)
    if switch == 0:
        return prop_matched, resp_matched
    elif switch == 1:
        return prop_matched, resp_matched, resp_indptr
    else:
        return prop_matched, resp_matched, prop_indptr, resp_indptr

def Graph(prop_matched, resp_matched, prop_indptr=None, resp_indptr=None, prop_name=None, resp_name=None):
    """
    Print a graph about the matching pair made by match().
    Lables of male are blue and that of female are red.
    """
    if prop_indptr is None:
        prop_num = len(prop_matched)
        prop_caps = np.ones(prop_num)
        prop_indptr = np.zeros(prop_num+1, dtype=int)
        np.cumsum(prop_caps, out=prop_indptr[1:])
    else:
        prop_num = len(prop_indptr) - 1
    if resp_indptr is None:
        resp_num = len(resp_matched)
        resp_caps = np.ones(resp_num)
        resp_indptr = np.zeros(resp_num+1, dtype=int)
        np.cumsum(resp_caps, out=resp_indptr[1:])
    else:
        resp_num = len(resp_indptr) - 1
    if prop_name is None:
        prop_name = range(prop_num)
    if resp_name is None:
        resp_name = range(resp_num)
    vector = {}
    prop_vector = {}
    resp_vector = {}
    pos = {}
    prop_pos = {}
    resp_pos = {}
    height = max(prop_num, resp_num)
    for prop_id in range(prop_num):
        vector["m%s" % prop_id] = []
        prop_vector[prop_name[prop_id]] = []
        pos["m%s" % prop_id] = np.array([1, height-prop_id])
        prop_pos[prop_name[prop_id]] = np.array([1, height-prop_id])
        pairs = prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]]
        for pair in pairs:
            if pair != resp_num:
                vector["m%s" % prop_id].append("f%s" % pair)
    for resp_id in range(resp_num):
        vector["f%s" % resp_id] = []
        resp_vector[resp_name[resp_id]] = []
        pos["f%s" % resp_id] = np.array([2, height-resp_id])
        resp_pos[resp_name[resp_id]] = np.array([2, height-resp_id])
    graph = nx.Graph(vector)
    m_graph = nx.Graph(prop_vector)
    f_graph = nx.Graph(resp_vector)
    nx.draw_networkx_labels(m_graph, prop_pos, font_size=28, font_color="b")
    nx.draw_networkx_labels(f_graph, resp_pos, font_size=28, font_color="r")
    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color="w")
    nx.draw_networkx_edges(graph, pos, width=1)
    plt.xticks([])
    plt.yticks([])
    plt.show

def Nash(algo, prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None):
    """
    Nash equilibria in pure strategy.

    Parameters
    ---
    algo : string
        'DA'  : Deffered Acceptance Algorithm
        'BOS' : Boston School Choice
        'DAAdd' : DA + AddBOS
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants

    Returns
    ---
    Nash : ndarray(int, ndim=2)
        Nash equilibria in pure strategy

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_ranks = np.argsort(prop_prefs)
    iter_prefs = np.zeros((prop_num, resp_num), dtype=int)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    l = range(resp_num)
    behavior = defaultdict()
    counter = 0
    for element in itertools.permutations(l, len(l)):
        behavior[counter] = element
        counter += 1
    matrix = [counter for i in range(prop_num)]
    g = gambit.Game.new_table(matrix)
    for profile in g.contingencies:
        for prop_id, behave_num in zip(range(prop_num), profile):
            iter_prefs[prop_id] = behavior[behave_num]
        if algo == 'DA':
            if switch == 0:
                prop_matched, resp_matched = \
                    DA(iter_prefs, resp_prefs, None, None, list_length)
            elif switch == 1:
                prop_matched, resp_matched, resp_indptr = \
                    DA(iter_prefs, resp_prefs, resp_caps, None, list_length)
            elif switch == 2:
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    DA(iter_prefs, resp_prefs, resp_caps, prop_caps, list_length)
        elif algo == 'BOS':
            if switch == 0:
                prop_matched, resp_matched = \
                    BOS(iter_prefs, resp_prefs, None, None, list_length)
            elif switch == 1:
                prop_matched, resp_matched, resp_indptr = \
                    BOS(iter_prefs, resp_prefs, resp_caps, None, list_length)
            elif switch == 2:
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    BOS(iter_prefs, resp_prefs, resp_caps, prop_caps, list_length)
        elif algo == 'DAAdd':
            if switch == 0:
                prop_matched, resp_matched = \
                    DA(iter_prefs, resp_prefs, resp_caps, prop_caps, list_length-1)
                prop_matched, resp_matched = \
                    AddBOS(iter_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
            elif switch == 1:
                prop_matched, resp_matched, resp_indptr = \
                    DA(iter_prefs, resp_prefs, resp_caps, prop_caps, list_length-1)
                prop_matched, resp_matched, resp_indptr = \
                    AddBOS(iter_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
            elif switch == 2:
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    DA(iter_prefs, resp_prefs, resp_caps, prop_caps, list_length-1)
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    AddBOS(iter_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
        for prop_id in range(prop_num):
            payoff = 0
            pairs = prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]]
            for pair in pairs:
                if pair != resp_num:
                    payoff += resp_num - prop_ranks[prop_id][pair]
            g[profile][i] = payoff
    solver = gambit.nash.ExternalEnumPureSolver()
    nashs = solver.solve(g)
    return nashs, behavior

def SubPref(nash, behavior):
    """
    Make a submitted preference from one of the nash equilibria.

    Parameters
    ---
    nash : ndarray(ndim=1)
        one of the nash equilibria
    behavior : dict

    Returns
    ---
    submit_pref : ndarray(int, ndim=2)
        Submitted preference of proposers

    """
    nash = np.asarray(nash, dtype=int)
    comb = len(behavior)
    resp_num = len(behavior[0])
    prop_num = int(len(nash) / comb)
    nash = nash.reshape(prop_num, comb)
    submit_pref = np.zeros((prop_num, resp_num), dtype=int)
    for prop_id in range(prop_num):
        submit_pref[prop_id] = behavior[np.where(nash[prop_id] == 1)[0][0]]
    return submit_pref

def ConstNash(nashs, behavior, list_length):
    """
    Make the preferences under Nash equilibria

    Parameters
    ---
    nashs : ndarray(ndim=2)
        one of the nash equilibria
    behavior : dict

    Return
    ---
    nash_prefs : ndarray(ndim=2)

    """
    nash_prefs = []
    for nash in nashs:
        submit_pref = SubPref(nash, behavior)
        submit_pref = submit_pref[:, range(list_length)].tolist()
        if len(nash_prefs) == 0:
            nash_prefs.append(submit_pref)
        else:
            counter = 0
            for nash_pref in nash_prefs:
                if submit_pref == nash_pref:
                    counter = 1
                    break
            if counter == 0:
                nash_prefs.append(submit_pref)
    return nash_prefs

def Comp(algo, submit_prefs, prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None):
    """
    Comparison under the truth-telling circumstances
    """
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    if algo == 'DA':
        if switch == 0:
            prop_matched, resp_matched = \
                DA(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length)
        elif switch == 1:
            prop_matched, resp_matched, resp_indptr = \
                DA(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length)
        elif switch == 2:
            prop_matched, resp_matched, prop_indptr, resp_indptr = \
                DA(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length)
    elif algo == 'BOS':
        if switch == 0:
            prop_matched, resp_matched = \
                BOS(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length)
        elif switch == 1:
            prop_matched, resp_matched, resp_indptr = \
                BOS(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length)
        elif switch == 2:
            prop_matched, resp_matched, prop_indptr, resp_indptr = \
                BOS(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length)
    elif algo == 'DAAdd':
        if switch == 0:
            prop_matched, resp_matched = \
                DA(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length-1)
            prop_matched, resp_matched = \
                AddBOS(submit_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
        elif switch == 1:
            prop_matched, resp_matched, resp_indptr = \
                DA(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length-1)
            prop_matched, resp_matched, resp_indptr = \
                AddBOS(submit_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
        elif switch == 2:
            prop_matched, resp_matched, prop_indptr, resp_indptr = \
                DA(submit_prefs, resp_prefs, resp_caps, prop_caps, list_length-1)
            prop_matched, resp_matched, prop_indptr, resp_indptr = \
                AddBOS(submit_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
    JE_num = CountJE(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
    tt_num = CountTT(prop_prefs, submit_prefs, list_length)
    prop_eff, resp_eff = MeanEff(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
    prop_poor, resp_poor = CountPoor(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
    interview_num = CountInte(algo, prop_prefs, resp_prefs, resp_caps, prop_caps, list_length)
    return round(JE_num, 3), round(tt_num, 3), round(prop_eff, 3), round(resp_eff, 3), \
        round(prop_poor, 3), round(resp_poor, 3), round(interview_num, 3)

def NashComp(algo, prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None):
    """
    Nash Comparison
    """
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    JE_nums = []
    tt_nums = []
    prop_effs = []
    resp_effs = []
    prop_poors = []
    resp_poors = []
    interview_nums = []
    nashs, behavior = Nash(algo, prop_prefs, resp_prefs, resp_caps, prop_caps, list_length)
    for nash in nashs:
        submit_pref = SubPref(nash, behavior)
        if algo == 'DA':
            if switch == 0:
                prop_matched, resp_matched = \
                    DA(submit_pref, resp_prefs, resp_caps, prop_caps, list_length)
            elif switch == 1:
                prop_matched, resp_matched, resp_indptr = \
                    DA(submit_pref, resp_prefs, resp_caps, prop_caps, list_length)
            elif switch == 2:
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    DA(submit_pref, resp_prefs, resp_caps, prop_caps, list_length)
        elif algo == 'BOS':
            if switch == 0:
                prop_matched, resp_matched = \
                    BOS(submit_pref, resp_prefs, resp_caps, prop_caps, list_length)
            elif switch == 1:
                prop_matched, resp_matched, resp_indptr = \
                    BOS(submit_pref, resp_prefs, resp_caps, prop_caps, list_length)
            elif switch == 2:
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    BOS(submit_pref, resp_prefs, resp_caps, prop_caps, list_length)
        elif algo == 'DAAdd':
            if switch == 0:
                prop_matched, resp_matched = \
                    DA(submit_pref, resp_prefs, resp_caps, prop_caps, list_length-1)
                prop_matched, resp_matched = \
                    AddBOS(submit_pref, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
            elif switch == 1:
                prop_matched, resp_matched, resp_indptr = \
                    DA(submit_pref, resp_prefs, resp_caps, prop_caps, list_length-1)
                prop_matched, resp_matched, resp_indptr = \
                    AddBOS(submit_pref, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
            elif switch == 2:
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    DA(submit_pref, resp_prefs, resp_caps, prop_caps, list_length-1)
                prop_matched, resp_matched, prop_indptr, resp_indptr = \
                    AddBOS(submit_pref, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
        JE_num = CountJE(submit_pref, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
        tt_num = CountTT(submit_pref, prop_prefs, list_length)
        prop_eff, resp_eff = MeanEff(submit_pref, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
        prop_poor, resp_poor = CountPoor(submit_pref, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps)
        interview_num = CountInte(algo, submit_pref, resp_prefs, resp_caps, prop_caps, list_length)
        JE_nums.append(JE_num)
        tt_nums.append(tt_num)
        prop_effs.append(prop_eff)
        resp_effs.append(resp_eff)
        prop_poors.append(prop_poor)
        resp_poors.append(resp_poor)
        interview_nums.append(interview_num)
    nash_num = len(nashs)
    JE_nums_mean = np.mean(JE_nums)
    tt_nums_mean = np.mean(tt_nums)
    prop_effs_mean = np.mean(prop_effs)
    resp_effs_mean = np.mean(resp_effs)
    prop_poors_mean = np.mean(prop_poors)
    resp_poors_mean = np.mean(resp_poors)
    interview_nums_mean = np.mean(interview_nums)
    return nash_num, round(JE_nums_mean, 3), round(tt_nums_mean, 3), round(prop_effs_mean, 3), \
        round(resp_effs_mean, 3), round(prop_poors_mean, 3), round(resp_poors_mean, 3), round(interview_nums_mean, 3)

def MakeCVprefs(prop_num, resp_num, alpha=0.3, beta=0.3):
    """
    Make preferences based on Common-Value Model.

    Parameters
    ---
    prop_num : scalar(int)
        The number of proposers
    resp_num : scalar(int)
        The number of respondants
    alphs : scalar(int)
        Weight of the resp's Common-Value(ex.popularity)
    beta : scalar(int)
        Weight of the prop's Common-Valuegrade(ex.grade)

    Returns
    ---
    prop_prefs : ndarray(int, ndim=2)
      Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
      Preference of respondants

    """
    popularity = np.random.rand(resp_num, 1)
    grade = np.random.normal(50, 10, [prop_num, 1])
    popu_ranks = np.argsort(popularity.T[0])[::-1]

    prop_cv = np.dot(popularity, np.ones((1, prop_num))).T
    prop_pv = np.random.rand(prop_num, resp_num)
    prop_uti = alpha * prop_cv + (1 - alpha) * prop_pv
    prop_prefs = np.argsort(prop_uti)[:, ::-1]

    resp_cv = np.dot(grade, np.ones((1, resp_num))).T
    resp_pv = np.random.rand(resp_num, prop_num)
    resp_uti = beta * resp_cv + (1 - beta) * resp_pv
    resp_prefs = np.argsort(resp_uti)[:, ::-1]

    return prop_prefs, resp_prefs, popu_ranks, grade.T[0]

def CountJE(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps=None, prop_caps=None):
    """
    Count the number of proposers who have justified envy.

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    resp_caps : list
        Capacity of respondants
    prop_caps : list
        Capacity of proposers

    Returns
    ---
    JE_num : scalar(int)
        The number of students who have justified envy

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_prefs = np.c_[prop_prefs, np.ones((prop_num, 1))*resp_num]
    resp_prefs = np.c_[resp_prefs, np.ones((resp_num, 1))*prop_num]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    prop_ranks = np.argsort(prop_prefs)
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    resp_maxrank = [max(resp_ranks[i, resp_matched[resp_indptr[i]:resp_indptr[i+1]]]) for i in range(resp_num)]
    prop_maxrank = [max(prop_ranks[i, prop_matched[prop_indptr[i]:prop_indptr[i+1]]]) for i in range(prop_num)]
    JE_num = 0

    for prop_id in range(prop_num):
        for resp_id in range(resp_num):
            if resp_id not in prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]]:
                if prop_ranks[prop_id][resp_id] <= prop_maxrank[prop_id]:
                    if resp_ranks[resp_id][prop_id] <= resp_maxrank[resp_id]:
                        JE_num += 1
                        break
    return JE_num

def CountTT(prop_prefs, subprefs, list_length):
    """
    Count the number of truth-telling proposers.

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    subprefs : ndarray(int, ndim=2)
        Submitted Preference of proposers

    Returns
    ---
    tt_num : scalar(int)
        The number of truth-telling proposers
    """
    prop_prefs = np.asarray(prop_prefs)
    subprefs = np.asarray(subprefs)
    tt_num = 0
    for prop_id in range(prop_prefs.shape[0]):
        if subprefs[prop_id][1] == 4: # resp_num = 4
            if prop_prefs[prop_id][:1].tolist() == subprefs[prop_id][:1].tolist():
                tt_num += 1
        elif subprefs[prop_id][2] == 4: # resp_num = 4
            if prop_prefs[prop_id][:2].tolist() == subprefs[prop_id][:2].tolist():
                tt_num += 1
        else:
            if prop_prefs[prop_id][:list_length].tolist() == subprefs[prop_id][:list_length].tolist():
                tt_num += 1
    return tt_num

def MeanEff(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps=None, prop_caps=None):
    """
    Mean of the efficincy of proposers and respondants.

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants

    Returns
    ---
    prop_eff : scalar(int)
        Mean of the efficiency of proposers.
    resp_eff : scalar(int)
        Mean of the efficiency of respondants.

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_prefs = np.c_[prop_prefs, np.ones((prop_num, 1))*resp_num]
    resp_prefs = np.c_[resp_prefs, np.ones((resp_num, 1))*prop_num]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    prop_ranks = np.argsort(prop_prefs)
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    for i in range(prop_num):
        prop_pair = prop_matched[prop_indptr[i]:prop_indptr[i+1]].tolist()
        while resp_num in prop_pair:
            prop_pair.remove(resp_num)
        if len(prop_pair) > 0:
            prop_meanrank = [np.mean(prop_ranks[i, prop_pair])]
    for i in range(resp_num):
        resp_pair = resp_matched[resp_indptr[i]:resp_indptr[i+1]].tolist()
        while prop_num in resp_pair:
            resp_pair.remove(prop_num)
        if len(resp_pair) > 0:
            resp_meanrank = [np.mean(resp_ranks[i, resp_pair])]
    prop_eff = np.mean(prop_meanrank)
    resp_eff = np.mean(resp_meanrank)
    return round(prop_eff, 3), round(resp_eff, 3)

def CountPoor(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps=None, prop_caps=None):
    """
    Count the proposers that match with no respondants,
    and the vacant capacity of respondants.

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_matched : ndarray(int, ndim=1)
        Matching Pairs for proposers
    resp_matched : ndarray(int, ndim=1)
        Matching Pairs for respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants

    Returns
    ---
    prop_poor : scalar(int)
        The number of the proposers that match with no respondants
    resp_poor : scalar(int)
        The number of vacant capacity

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    prop_prefs = np.c_[prop_prefs, np.ones((prop_num, 1))*resp_num]
    resp_prefs = np.c_[resp_prefs, np.ones((resp_num, 1))*prop_num]
    prop_unmatched = resp_num
    resp_unmatched = prop_num
    prop_ranks = np.argsort(prop_prefs)
    resp_ranks = np.argsort(resp_prefs)
    switch = 2
    if prop_caps is None:
        switch = 1
        prop_caps = [1 for col in range(prop_num)]
    if resp_caps is None:
        switch = 0
        resp_caps = [1 for col in range(resp_num)]
    prop_indptr = np.zeros(prop_num+1, dtype=int)
    resp_indptr = np.zeros(resp_num+1, dtype=int)
    np.cumsum(prop_caps, out=prop_indptr[1:])
    np.cumsum(resp_caps, out=resp_indptr[1:])
    prop_poor = 0
    resp_poor = sum(resp_matched == prop_num)
    for prop_id in range(prop_num):
        if [resp_num for i in range(prop_caps[prop_id])] == prop_matched[prop_indptr[prop_id]:prop_indptr[prop_id+1]].tolist():
            prop_poor += 1
    return prop_poor, resp_poor

def CountInte(algo, prop_prefs, resp_prefs, resp_caps=None, prop_caps=None, list_length=None):
    """
    Count the number of interviews.

    Parameters
    ---
    prop_prefs : ndarray(int, ndim=2)
        Preference of proposers
    resp_prefs : ndarray(int, ndim=2)
        Preference of respondants
    prop_caps : list
        Capacity of proposers
    resp_caps : list
        Capacity of respondants

    Returns
    ---
    interview_num : scalar(int)
        The number of interviews

    """
    prop_prefs = np.asarray(prop_prefs)
    resp_prefs = np.asarray(resp_prefs)
    prop_num = prop_prefs.shape[0]
    resp_num = resp_prefs.shape[0]
    if list_length is None:
        list_length = resp_num
    if algo == 'BOS':
        interview_num = BOS(prop_prefs, resp_prefs, resp_caps, prop_caps, list_length, 1)
    elif algo == 'DA':
        interview_num = prop_num * list_length
    elif algo == 'DAAdd':
        prop_matched, resp_matched, prop_indptr, resp_indptr = \
            DA(prop_prefs, resp_prefs, resp_caps, prop_caps, list_length-1)
        interview_num = prop_num * (list_length-1) + AddBOS(prop_prefs, resp_prefs, prop_matched, resp_matched, resp_caps, prop_caps, 1)
    return interview_num
