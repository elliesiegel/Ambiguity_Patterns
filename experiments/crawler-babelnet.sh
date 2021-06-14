#!/bin/bash

# example call:    ./crawler-babelnet.sh wordlist.csv JSON_data_comparison/both_false/ API_KEY

WORD_CSV="$1"
TARGET_DIR="$2" # e.g. JSON_data_comparison/both_false
API_KEY="$3"
mkdir -p $TARGET_DIR/words
mkdir -p $TARGET_DIR/RESULTS_figure_CSV
mkdir -p $TARGET_DIR/get_pattern_synsets-output
mkdir -p $TARGET_DIR/get_sense_graph_output
#TODO change crawler-vars-falses !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CURR_LANGS_ID=$(cat crawler-vars-falses/current_langs)
CURR_WORD_LOADING=$(cat crawler-vars-false/current_word_loading)

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
			# Word to continue with was reached
			CURR_WORD_LOADING=""
		else
			# Continue until last unfinished word
			continue
		fi
	fi
	# Skip allready downloaded words
	if test -d $TARGET_DIR/words/$WORD
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
		python3 get_pattern.py --targetLang_searchLang $LANG --languages $LANG $WORD $TARGET_DIR/words/$WORD/ $API_KEY
		# Check if babelnet queries are still available
		# cancel if over limit
		if grep -q "Your key is not valid or the daily requests limit has been reached." $TARGET_DIR/words/$WORD/*$LANG*
		then
			echo "Ending Script - no more queries available"
			#save count
			echo $CURR_LANGS_ID > crawler-vars-falses/current_langs
			rm $TARGET_DIR/words/$WORD/*$LANG*
			exit 1
		fi
		CURR_LANGS_ID=$(( $CURR_LANGS_ID + 1 ))	
	done

	# STEP 2: delete duplicates
	python3 document_checker.py $TARGET_DIR/words/$WORD/

	# STEP 3: write number of nodes and edges to csv per word
	python3 get_pattern_synsets.py $TARGET_DIR/words/$WORD/ > $TARGET_DIR/get_pattern_synsets-output/$WORD

	# STEP 4: create image per word
	python3 get_sense_graph.py $TARGET_DIR/words/$WORD/ $TARGET_DIR/RESULTS_figure_CSV/$WORD > $TARGET_DIR/get_sense_graph_output/$WORD

	# STEP 5: create CSVs
	NODES=$(grep total $TARGET_DIR/get_pattern_synsets-output/$WORD | grep nodes | grep -o [0-9]*)
	EDGES=$(grep total $TARGET_DIR/get_pattern_synsets-output/$WORD | grep edges | grep -o [0-9]*)
	NUM_CLIQUES=$(grep total $TARGET_DIR/get_sense_graph_output/$WORD | grep cliques | grep -o [0-9]*)
	CLIQUE_EDGES=$(grep total $TARGET_DIR/get_sense_graph_output/$WORD | grep clique-edges | grep -o [0-9]*)
	echo "$WORD,$NODES,$EDGES,$NUM_CLIQUES,$CLIQUE_EDGES" >> $TARGET_DIR/RESULTS_figure_CSV/word-nodes-edges.csv

	CURR_LANGS_ID=1
done
echo "----------------------------------------------------------------------------------------------------"
echo " :D  you reached the end of the word list!"

echo -n "" > crawler-vars-falses/current_word_loading
