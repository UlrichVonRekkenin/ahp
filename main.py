import json
import numpy as np
from statistics import geometric_mean

with open('example.json', 'r', encoding='utf-8') as file:
    obj = json.load(file)

criteria = list(obj['criteria'].values())
criteria_len = len(criteria)
weighted_criteria = [[c / criteria[i] for c in criteria] for i in range(criteria_len)]
geometric_means = [geometric_mean(np.array(weighted_criteria)[:, i]) for i in range(criteria_len)]
weighted_geometric_means = [g / sum(geometric_means) for g in geometric_means]

alts = obj['alts']
alts_len_range = range(len(alts[0]))
C = [[[[alts[k][i] / alts[k][j] for i in alts_len_range] for j in alts_len_range] for k in range(criteria_len)]]
AC = [[geometric_mean(np.array(C[0][j])[:, i]) for i in alts_len_range] for j in range(criteria_len)]
WaCi = [[AC[j][i] / sum(AC[j]) for i in alts_len_range] for j in range(criteria_len)]

result = [sum(np.array(WaCi)[:, i] * weighted_geometric_means) for i in alts_len_range]

print(obj['names'][result.index(max(result))])
