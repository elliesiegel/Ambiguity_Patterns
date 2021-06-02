#!/bin/bash
for word in get_pattern_synsets-output_falses/*
do
	WORD=$(echo $word | sed 's/.*\///g')
	echo $WORD
	python3 get_sense_graph.py JSON_data_comparison/both_false/$WORD/ RESULTS_figure_CSV/falses_multilingual/$WORD > get_sense_graph_output_falses/$WORD
	NODES=$(grep total get_pattern_synsets-output_falses/$WORD | grep nodes | grep -o [0-9]*)
	EDGES=$(grep total get_pattern_synsets-output_falses/$WORD | grep edges | grep -o [0-9]*)
	NUM_CLIQUES=$(grep total get_sense_graph_output_falses/$WORD | grep cliques | grep -o [0-9]*)
	CLIQUE_EDGES=$(grep total get_sense_graph_output_falses/$WORD | grep clique-edges | grep -o [0-9]*)
	echo "$WORD,$NODES,$EDGES,$NUM_CLIQUES,$CLIQUE_EDGES" >> RESULTS_figure_CSV/all-falses-word-nodes-edges.csv
done
