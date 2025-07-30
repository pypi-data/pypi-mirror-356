#!/usr/bin/env python3
# coding: utf-8

import collections
import math


def compute_entropy(chars):
    n = len(chars)
    counter = collections.Counter(chars)
    probs = [ni / n for ni in counter.values()]
    return -sum([p * math.log2(p) for p in probs])
