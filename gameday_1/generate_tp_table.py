#!/usr/bin/env python3
"""
Generate TPTable.csv and r.csv for the QLearning example.

TPTable.csv format: s,a,s_next,p
Each (s,a) row will have probabilities over s_next that sum to 1.

r.csv format: one reward mean per line for each state (index 0..5)
"""
import csv
import random

MAX_NUM_STATES = 6
MAX_NUM_ACTIONS = 6

def generate_tp_table(path='TPTable.csv'):
    rows = []
    for s in range(MAX_NUM_STATES):
        for a in range(MAX_NUM_ACTIONS):
            # create a probability distribution over next states
            probs = [random.random() for _ in range(MAX_NUM_STATES)]
            total = sum(probs)
            probs = [p/total for p in probs]
            for s_next, p in enumerate(probs):
                # write row s,a,s_next,p
                rows.append((s,a,s_next,round(p,6)))

    with open(path,'w',newline='') as f:
        writer = csv.writer(f)
        for r in rows:
            writer.writerow(r)

# def generate_r_csv(path='r.csv'):  # NOTE: just manually create arbitrary rewards
#     # simple base rewards per state (e.g., increasing with state index)
#     rewards = [round(1.0 + 0.5*i + random.uniform(-0.2,0.2),3) for i in range(MAX_NUM_STATES)]
#     with open(path,'w',newline='') as f:
#         writer = csv.writer(f)
#         for r in rewards:
#             writer.writerow([r])

def main():
    generate_tp_table()
    # generate_r_csv()
    print('Wrote TPTable.csv and r.csv')

if __name__ == '__main__':
    main()
