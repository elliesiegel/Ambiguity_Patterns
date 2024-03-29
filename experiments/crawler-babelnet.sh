#!/bin/bash

# example call:    ./crawler-babelnet.sh wordlist.csv JSON_data_comparison/both_false/ API_KEY

WORD_CSV="$1"		# or a list with words
TARGET_DIR="$2"		# e.g. JSON_data_comparison/both_false
API_KEY="$3"		# your api babelnet access key
mkdir -p $TARGET_DIR/words
mkdir -p $TARGET_DIR/RESULTS_figure_CSV
mkdir -p $TARGET_DIR/get_pattern_synsets-output
mkdir -p $TARGET_DIR/get_sense_graph_output

# this script requires the following virtual environment for python
if test "wsd_MA" != "$CONDA_DEFAULT_ENV"
then
	echo "Please go into the right environment (try: conda activate wsd_MA )"
	exit 1
fi

for WORD in $(sed 's/,.*//g' "$WORD_CSV" | tr " " _ )
do
	# Skip already downloaded words
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
	# multilingual:
	python3 get_pattern_synsets.py $TARGET_DIR/words/$WORD/ > $TARGET_DIR/get_pattern_synsets-output/$WORD
	# monolingual:
	python3 get_pattern_synsets_monolingual.py $TARGET_DIR/words/$WORD/ > $TARGET_DIR/get_pattern_monolingual_synsets-output/$WORD

	# STEP 4: create image per word
	# multilingual:
	python3 get_sense_graph.py $TARGET_DIR/words/$WORD/ $TARGET_DIR/RESULTS_figure_CSV/$WORD > $TARGET_DIR/get_sense_graph_output/$WORD
	# monolingual:
	python3 get_sense_graph_monolingual.py $TARGET_DIR/words/$WORD/ $TARGET_DIR/RESULTS_figure_CSV_monolingual/$WORD > $TARGET_DIR/get_sense_monolingual_graph_output/$WORD

	# STEP 5: create CSVs
	# metrics for word graph multilingual:
	NODES=$(grep "total number of nodes:" $TARGET_DIR/get_pattern_synsets-output/$WORD | grep -o "[0-9]*")
	EDGES=$(grep "total number of edges:" $TARGET_DIR/get_pattern_synsets-output/$WORD | grep -o "[0-9]*")
	
	# metrics for word graph monolingual EN:
	NODES_MONO=$(grep "total number of nodes mono (EN):" $TARGET_DIR/get_pattern_monolingual_synsets-output/$WORD | grep -o "[0-9]*")
	EDGES_MONO=$(grep "total number of edges mono (EN):" $TARGET_DIR/get_pattern_monolingual_synsets-output/$WORD | grep -o "[0-9]*")

	# metrics for sense graph multilingual:
	NUM_CLIQUES=$(grep "total number cliques" $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*")
	CLIQUE_EDGES=$(grep "total number clique-edges" $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*")

	VAR_WORDS_CLIQUES=$(grep " variance btw. words in cliques " $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*\.\?[0-9]*" | grep [0-9] )
	VAR_EDGES_CLIQUES=$(grep " variance btw. edges out. from cliques " $TARGET_DIR/get_sense_graph_output/$WORD | grep -o "[0-9]*\.\?[0-9]*" | grep [0-9] )

	# metrics for sense graph monolingual:
	NUM_CLIQUES_MONO=$(grep "total number cliques  mono (EN):" $TARGET_DIR/get_sense_monolingual_graph_output/$WORD | grep -o "[0-9]*")
	CLIQUE_EDGES_MONO=$(grep "total number clique-edges mono (EN):" $TARGET_DIR/get_sense_monolingual_graph_output/$WORD | grep -o "[0-9]*")

	VAR_WORDS_CLIQUES_MONO=$(grep " variance btw. words in cliques mono (EN):" $TARGET_DIR/get_sense_monolingual_graph_output/$WORD | grep -o "[0-9]*\.\?[0-9]*" | grep [0-9] )
	VAR_EDGES_CLIQUES_MONO=$(grep " variance btw. edges out. from cliques mono (EN):" $TARGET_DIR/get_sense_monolingual_graph_output/$WORD | grep -o "[0-9]*\.\?[0-9]*" | grep [0-9] )

	# multilingual data
	echo "$WORD,$NODES,$EDGES,$NUM_CLIQUES,$CLIQUE_EDGES,$VAR_WORDS_CLIQUES,$VAR_EDGES_CLIQUES" >> $TARGET_DIR/RESULTS_figure_CSV/word-nodes-edges.csv
	
	# monolingual data
	echo "$WORD,$NODES_MONO,$EDGES_MONO,$NUM_CLIQUES_MONO,$CLIQUE_EDGES_MONO,$VAR_WORDS_CLIQUES_MONO,$VAR_EDGES_CLIQUES_MONO" >> $TARGET_DIR/RESULTS_figure_CSV_monolingual/word-nodes-edges-monolingual.csv

done
echo "----------------------------------------------------------------------------------------------------"
echo " :D  you reached the end of the word list!"

echo -n "" > crawler-vars-falses/current_word_loading


# for both mono- and multilingual ambiguity graphs
# WORD
# NODES
# EDGES
# NUM_CLIQUES
# CLIQUE_EDGES
# VAR_WORDS_CLIQUES
# VAR_EDGES_CLIQUES
