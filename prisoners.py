from calendar import c
from random import choices, sample, shuffle
import numpy as np
import pandas as pd
import copy
import matplotlib.pyplot as plt
from collections import Counter

v = 1.96
generations = 100
width = 100
height = 100
# cooperate = 0, defect = 1 
strategies = ['0', '1']
next_cells = {}
temp = [0.2, 0.8]
payoffs = np.array([[1, 0], [1 + v, 0]])
rpm = pd.DataFrame(payoffs, columns=['0', '1'])
rpm.index = ['0', '1']
cpm = rpm.T
output2 = []

for x in range(width):
	for y in range(height):
		if (x == width/2) and (y == height/2):
			strat = '1'
		else:
			strat = '0'
		next_cells[(x, y)] = {
			'strategy': strat, 
			'prev_strat': None, 
			'score': 0, 
			'neighbours': [((x + 1) % width, y), ((x - 1) % width, y), (x, (y - 1) % height), (x, (y + 1) % height),
			((x + 1) % width, (y - 1) % height), ((x + 1) % width, (y + 1) % height), ((x - 1) % width, (y - 1) % height), ((x - 1) % width, (y + 1) % height)
			]
		}

for gen in range(generations):
	output = np.zeros(shape=(width, height))
	cells = copy.deepcopy(next_cells)
	for coord, cell in cells.items():
		score = 0
		if cell['strategy'] == '0':
				score += 1
		for neighbour in cell['neighbours']:
			if cell['strategy'] == '0' and cells[neighbour]['strategy'] == '0':
				score += 1
			if cell['strategy'] == '1' and cells[neighbour]['strategy'] == '0':
				score += v
		cell['score'] = score
				
	for coord, cell in cells.items():
		highest_score = 0
		best_strat = None
		for neighbour in cell['neighbours']:
			if cells[neighbour]['score'] > highest_score:
				highest_score = cells[neighbour]['score']
				best_strat = cells[neighbour]['strategy']
		if cell['score'] < highest_score:
			next_cells[coord]['strategy'] = best_strat
			next_cells[coord]['prev_strat'] = cell['strategy']
		if cell['score'] >= highest_score:
			next_cells[coord]['strategy'] = cell['strategy']
			next_cells[coord]['prev_strat'] = cell['strategy']		
		
		x, y = coord[0], coord[1]
		if next_cells[coord]['strategy'] == '0' and next_cells[coord]['prev_strat'] == '1':
			output[x][y] = 2
		elif next_cells[coord]['strategy'] == '1' and next_cells[coord]['prev_strat'] == '0':
			output[x][y] = 3
		else:
			output[x][y] = int(next_cells[coord]['strategy'])
	

	plt.imshow(output, interpolation='nearest')
	plt.colorbar()
	plt.pause(0.01)
	plt.savefig(f"images/foo{gen}.png")
	plt.close("all")

plt.show()