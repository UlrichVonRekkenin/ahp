import json
import numpy as np
from statistics import geometric_mean
import argparse
import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('config', type=str, help='Path to file')
args = parser.parse_args()

with open(args.config, 'r', encoding='utf-8') as file:
    obj = json.load(file)

    if len(obj['criteria']) != len(obj['alts']):
        print(f'Criteria number {len(obj["criteria"])=} must be equal to {len(obj["alts"])=}')
        quit(1)

    if not all([len(obj['alts'][i]) == len(obj['names']) for i in range(len(obj['alts']))]):
        print(f'The lengths of all `alts` configurations must be equal to {len(obj["names"])}')
        quit(2)

criteria = list(obj['criteria'].values())
criteria_len_range = range(len(criteria))
weighted_criteria = [[c / criteria[i] for c in criteria] for i in criteria_len_range]
geometric_means = [geometric_mean(np.array(weighted_criteria)[:, i]) for i in criteria_len_range]
weighted_geometric_means = [g / sum(geometric_means) for g in geometric_means]

alts = obj['alts']
alts_len_range = range(len(alts[0]))
C = [[[[alts[k][i] / alts[k][j] for i in alts_len_range] for j in alts_len_range] for k in criteria_len_range]]
AC = [[geometric_mean(np.array(C[0][j])[:, i]) for i in alts_len_range] for j in criteria_len_range]
WaCi = [[AC[j][i] / sum(AC[j]) for i in alts_len_range] for j in criteria_len_range]

result = [sum(np.array(WaCi)[:, i] * weighted_geometric_means) for i in alts_len_range]

table = tabulate.tabulate(
    [[obj['names'][i]] + list(np.array(alts)[:, i]) + [result[i]] for i in alts_len_range],
    headers=['criteria\\importance|alts'] + [f'{z[0]}\\{z[1]}' for z in obj['criteria'].items()] + ['result'],
    showindex='always',
    tablefmt='fancy_grid',
    numalign='center',
)
print(table)

best_match = obj["names"][result.index(max(result))]
print(f'\n\tBest match for alternative {best_match}')
