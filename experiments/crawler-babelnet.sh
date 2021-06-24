#!/bin/bash

# example call:    ./crawler-babelnet.sh wordlist.csv JSON_data_comparison/both_false/ API_KEY

WORD_CSV="$1"
TARGET_DIR="$2" # e.g. JSON_data_comparison/both_false
API_KEY="$3"
mkdir -p $TARGET_DIR/words
mkdir -p $TARGET_DIR/RESULTS_figure_CSV
mkdir -p $TARGET_DIR/get_pattern_synsets-output
mkdir -p $TARGET_DIR/get_sense_graph_output

# this script reqires the following virtual environment for python
if test "wsd_MA" != "$CONDA_DEFAULT_ENV"
then
	echo "Please go into the right environment (try: conda activate wsd_MA )"
	exit 1
fi

for WORD in $(sed 's/,.*//g' "$WORD_CSV" | tr " " _ )
do
	# Skip allready downloaded words
	if test -d $TARGET_DIR/words/$WORD
	then
		echo "skip: $WORD"
		continue
	fi
	echo "+++++++++ next word: $WORD +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	for LANG in DE_ES_FR CS_IT_NN RU_UK_PL
	#for LANG in DE_ES_FR # IT_RU_EN
	do 
		echo "+++++++++ next lang: $LANG ++++++++++"
		echo $WORD > crawler-vars-falses/current_word_loading
		# STEP 1: get data
		python3 get_pattern.py --targetLang_searchLang $LANG --languages $LANG $WORD $TARGET_DIR/words/$WORD/ $API_KEY
		# Check if babelnet queries are still available
		# cancel if over limit
		if grep -q "Your key is not valid or the daily requests limit has been reached.\|The maximum keys number per IP has been reached." $TARGET_DIR/words/$WORD/*
		then
			echo "Ending Script - no more queries available"
			rm -rf $TARGET_DIR/words/$WORD
			exit 1
		fi
	done

	# STEP 2: delete duplicates
	python3 document_checker.py $TARGET_DIR/words/$WORD/

	# STEP 3: write number of nodes and edges to csv per word
	python3 get_pattern_synsets.py $TARGET_DIR/words/$WORD/ > $TARGET_DIR/get_pattern_synsets-output/$WORD

	# STEP 4: create image per word
	python3 get_sense_graph.py $TARGET_DIR/words/$WORD/ $TARGET_DIR/RESULTS_figure_CSV/$WORD > $TARGET_DIR/get_sense_graph_output/$WORD

	# STEP 5: create CSVs
	# metrics for word graph:
	NODES=$(grep "total number of nodes:" $TARGET_DIR/get_pattern_synsets-output/$WORD | grep -o "[0-9]*")
	EDGES=$(grep "total number of edges:" $TARGET_DIR/get_pattern_synsets-output/$WORD | grep -o "[0-9]*")
	
	# metrics for sense graph:
	NUM_CLIQUES=$(grep "total number cliques" $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*")
	CLIQUE_EDGES=$(grep "total number clique-edges" $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*")

	VAR_WORDS_CLIQUES=$(grep " variance btw. words in cliques " $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*\.[0-9]*" | grep [0-9] )
	VAR_EDGES_CLIQUES=$(grep " variance btw. edges out. from cliques " $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*\.[0-9]*" | grep [0-9] )

	echo "$WORD,$NODES,$EDGES,$NUM_CLIQUES,$CLIQUE_EDGES,$VAR_WORDS_CLIQUES,$VAR_EDGES_CLIQUES" >> $TARGET_DIR/RESULTS_figure_CSV/word-nodes-edges.csv

done
echo "----------------------------------------------------------------------------------------------------"
echo " :D  you reached the end of the word list!"

echo -n "" > crawler-vars-falses/current_word_loading

# WORD
# NODES
# EDGES
# NUM_CLIQUES
# CLIQUE_EDGES
# VAR_WORDS_CLIQUES
# VAR_EDGES_CLIQUES