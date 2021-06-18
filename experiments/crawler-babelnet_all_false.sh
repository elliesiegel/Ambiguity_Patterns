#!/bin/bash

WORD_CSV="$1"
CURR_LANGS_ID=$(cat crawler-vars-falses/current_langs)
CURR_WORD_LOADING=$(cat crawler-vars-falses/current_word_loading)

# this script reqires the following virtual environment for python
if test "wsd_MA" != "$CONDA_DEFAULT_ENV"
then
	echo "Please go into the right environment (try: conda activate wsd_MA )"
	exit 1
fi

for WORD in $(sed 's/,.*//g' "$WORD_CSV" | tr " " _ )
do
	echo "List of intitialy known words to skip:"
	if test "$CURR_WORD_LOADING" != ""
	then
		echo -n "$WORD "
		if test "$CURR_WORD_LOADING" == "$WORD"
		then
			CURR_WORD_LOADING=""
		else
			continue
		fi
	fi
	# Skip allready downloaded words
	if test -d JSON_data_comparison/both_false/$WORD
	then
		echo "skipping $WORD (already downloaded)"
		continue
	fi
	echo "+++++++++ next word: $WORD +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	for LANG in $(echo DE_ES_FR CS_IT_NN RU_UK_PL | sed 's/ /\n/g' | tail -n +$(( 0 + $CURR_LANGS_ID )))
	do 
		echo "+++++++++ next lang: $LANG ++++++++++"
		echo $WORD > crawler-vars-falses/current_word_loading
		# STEP 1: get data
		python3 get_pattern.py --targetLang_searchLang $LANG --languages $LANG $WORD JSON_data_comparison/both_false/$WORD/
		# Check if babelnet queries are still available
		# cancel if over limit
		if grep -q "Your key is not valid or the daily requests limit has been reached." JSON_data_comparison/both_false/$WORD/*$LANG*
		then
			echo "Ending Script - no more queries available"
			#save count
			echo $CURR_LANGS_ID > crawler-vars-falses/current_langs
			exit 1
		fi
		CURR_LANGS_ID=$(( $CURR_LANGS_ID + 1 ))	
	done

	# STEP 2: delete duplicates
	python3 document_checker.py JSON_data_comparison/both_false/$WORD/

	# STEP 3: write number of nodes and edges to csv per word
	python3 get_pattern_synsets.py JSON_data_comparison/both_false/$WORD/ > get_pattern_synsets-output_falses/$WORD

	# STEP 4: create image per word
	python3 get_sense_graph.py JSON_data_comparison/both_false/$WORD/ RESULTS_figure_CSV/falses_multilingual/$WORD > get_sense_graph_output_falses/$WORD

	# STEP 5: create CSVs
	NODES=$(grep total get_pattern_synsets-output_falses/$WORD | grep nodes | grep -o [0-9]*)
	EDGES=$(grep total get_pattern_synsets-output_falses/$WORD | grep edges | grep -o [0-9]*)
	NUM_CLIQUES=$(grep total get_sense_graph_output_falses/$WORD | grep cliques | grep -o [0-9]*)
	CLIQUE_EDGES=$(grep total get_sense_graph_output_falses/$WORD | grep clique-edges | grep -o [0-9]*)
	echo "$WORD,$NODES,$EDGES,$NUM_CLIQUES,$CLIQUE_EDGES" >> RESULTS_figure_CSV/all-falses-word-nodes-edges.csv

	CURR_LANGS_ID=1
done
echo "----------------------------------------------------------------------------------------------------"
echo " :D  you reached the end of the word list!"

echo -n "" > crawler-vars-falses/current_word_loading
