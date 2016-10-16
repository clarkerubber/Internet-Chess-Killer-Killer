#!/usr/bin/env python

"""Analysing players for lichess.org"""

import argparse
import chess
import chess.uci
import chess.pgn
import logging
import os
import sys
import pickle
from modules.fishnet.fishnet import stockfish_command
from modules.bcolors.bcolors import bcolors
from modules.analysis.player import analyse_player
from modules.api.tools import get_files, get_player_games
from modules.analysis.tools import avg
from collections import Counter

import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.tools as tls
import numpy as np


try:
    # Optionally fix colors on Windows and in journals if the colorama module
    # is available.
    import colorama
    wrapper = colorama.AnsiToWin32(sys.stdout)
    if wrapper.should_wrap():
        sys.stdout = wrapper.stream
except ImportError:
    pass

cheaters_pkl = get_files('test-data/saved/cheaters')
legits_pkl = get_files('test-data/saved/legits')

cheaters = {}
legits = {}

for i in cheaters_pkl:
	with open('test-data/saved/cheaters/'+i, 'rb') as inputpkl:
		cheaters[os.path.splitext(i)[0]] = pickle.load(inputpkl)

for i in legits_pkl:
	with open('test-data/saved/legits/'+i, 'rb') as inputpkl:
		legits[os.path.splitext(i)[0]] = pickle.load(inputpkl)

legitavg = avg(sum(list(y.ranks() for x, y in legits.items()), []))
cheateravg = avg(sum(list(y.ranks() for x, y in cheaters.items()), []))

#print 'legitavg: '+str(legitavg)
#print 'cheateravg: '+str(cheateravg)
print 'legits'
lmodes = []
lmodes2 = []
cmodes = []
cmodes2 = []
for x, y in legits.items():
	data = Counter(y.ranks())
	print '   '+y.name+':'
	m0freq = data.most_common(1)[0][1]/float(len(y.ranks()))
	lmodes.append(m0freq)
	data = Counter([x for x in y.ranks() if x <= 20])
	m1freq = sum(data.values())/float(len(y.ranks()))
	lmodes2.append((m0freq, m1freq))
	print '    avg: '+str(avg(y.ranks()))
	print '   mode: '+str(m0freq)
	print '   good: '+str(m1freq)

print 'max mode 0 freq'
print max(lmodes)
print 'max mode2 0 freq'
print sorted(lmodes2)

print 'cheaters'
for x, y in cheaters.items():
	data = Counter(y.ranks())
	print '   '+y.name+':'
	m0freq = data.most_common(1)[0][1]/float(len(y.ranks()))
	cmodes.append(m0freq)
	data = Counter([x for x in y.ranks() if x <= 20])
	m1freq = sum(data.values())/float(len(y.ranks()))
	cmodes2.append((m0freq, m1freq))
	print '    avg: '+str(avg(y.ranks()))
	print '   mode: '+str(m0freq)
	print '   good: '+str(m1freq)

print 'min mode 0 freq'
print min(cmodes)
print 'min mode2 0 freq'
print sorted(cmodes2)

"""
for x, y in legits.items():
	print " "
	print y.error_v_move_no()
	print y.scaled_error_v_move_no()

for x, y in cheaters.items():
	print " "
	print y.error_v_move_no()
	print y.scaled_error_v_move_no()

fig, ax = plt.subplots()

for x, y in legits.items():
	xt, yt = y.error_v_move_no()
	ax.scatter(xt, yt)

fig.savefig('figures/legits/merged/ErrorVMoveNo.svg')

fig, ax = plt.subplots()

for x, y in legits.items():
	xt, yt = y.scaled_error_v_move_no()
	ax.scatter(xt, yt)

fig.savefig('figures/legits/merged/ScaledErrorVMoveNo.svg')


fig, ax = plt.subplots()

for x, y in cheaters.items():
	xt, yt = y.error_v_move_no()
	ax.scatter(xt, yt)

fig.savefig('figures/cheaters/merged/ErrorVMoveNo.svg')

fig, ax = plt.subplots()

for x, y in cheaters.items():
	xt, yt = y.scaled_error_v_move_no()
	ax.scatter(xt, yt)

fig.savefig('figures/cheaters/merged/ScaledErrorVMoveNo.svg')
"""
