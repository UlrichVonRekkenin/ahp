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

    if not all([len(obj['alternatives']) == len(c[1]) for c in obj['criteria'].values()]):
        print(f'Count of all alternatives in the `criteria` section must be equal to {len(obj["alternatives"])}.')
        quit(1)

criteria = [c[0] for c in list(obj['criteria'].values())]
criteria_len_range = range(len(criteria))
weighted_criteria = [[c / criteria[i] for c in criteria] for i in criteria_len_range]
geometric_means = [geometric_mean(np.array(weighted_criteria)[:, i]) for i in criteria_len_range]
weighted_geometric_means = [g / sum(geometric_means) for g in geometric_means]

alts = [c[1] for c in list(obj['criteria'].values())]
alts_len_range = range(len(alts[0]))
C = [[[[alts[k][i] / alts[k][j] for i in alts_len_range] for j in alts_len_range] for k in criteria_len_range]]
AC = [[geometric_mean(np.array(C[0][j])[:, i]) for i in alts_len_range] for j in criteria_len_range]
WaCi = [[AC[j][i] / sum(AC[j]) for i in alts_len_range] for j in criteria_len_range]
result = [sum(np.array(WaCi)[:, i] * weighted_geometric_means) for i in alts_len_range]

table = tabulate.tabulate(
    [[obj['alternatives'][i]] + list(np.array(alts)[:, i]) + [result[i]] for i in alts_len_range],
    headers=['criteria\\importance|alts'] + [f'{z[0]}\\{z[1][0]}' for z in obj['criteria'].items()] + ['result'],
    showindex='always',
    tablefmt='fancy_grid',
    numalign='center',
)
print(table)

check = [(sum(map(lambda z: z[0] * z[1],
                  zip(WaCi[j], [sum(C[0][j][i]) for i in alts_len_range])
                  )) - len(obj['alternatives'])) / (len(obj['alternatives']) - 1) / 1.12 for j in criteria_len_range]

if not all([abs(independence) < 10**(-9) for independence in check]):
    print(f'It seems to me that not all criteria index are independent: {check}.')

table = tabulate.tabulate(
    sorted(zip(obj['alternatives'], result), key=lambda x: x[1]),
    headers=['Alternative', 'Value'],
    tablefmt='fancy_grid',
    floatfmt='.2f',
    numalign='center'
)
print(f'Here is the sorted results\n{table}')

best_match = obj["alternatives"][result.index(max(result))]
print(f'\n\tBest match for alternative is `{best_match}`')
