#!/bin/bash

WORD_CSV="$1"
CONTINUE="$2"
CURR_WORD_ID=$(cat crawler-vars/current_word)
CURR_LANGS_ID=$(cat crawler-vars/current_langs)
OPEN_QUERIES=$(cat crawler-vars/open_queries)

for WORD in $(sed 's/,.*//g' "$WORD_CSV" | tr " " _ | sort -u | tail -n +$(( 1 + $CURR_WORD_ID )))
do
	echo "+++++++++ next word at id $CURR_WORD_ID: $WORD +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	for LANG in $(echo DE_ES_FR CS_IT_NN RU_UK_PL | sed 's/ /\n/g' | tail -n +$(( 0 + $CURR_LANGS_ID )))
	do
		echo "+++++++++ next lang: $LANG ++++++++++"
		if [ "$CONTINUE" == "continue" ]
		then
			CONTINUE="no"
			echo "In continue-Mode: deleting last failed try to crawl $word in $LANG"
			echo "[ PRESS ENTER TO CONTINUE ]"
			read ENTER
			rm JSON_data_comparison/both_ture/$WORD/*$LANG*
		fi
		# execute multiple queries
		python3 get_pattern.py --targetLang_searchLang $LANG --languages $LANG $WORD JSON_data_comparison/both_ture/$WORD/
		# count number of queries (aka. json-files) and substract from open-queries
		OPEN_QUERIES=$(( $OPEN_QUERIES - $( ls JSON_data_comparison/both_ture/$WORD/*$LANG* | wc -l ) ))
		echo "===== number of queries still available: $OPEN_QUERIES ====="
		# cancel if over limit
		if [ $OPEN_QUERIES -lt 0 ]
		then
			echo "Ending Script - no more queries available"
			#save counts
			echo $CURR_WORD_ID > crawler-vars/current_word
			echo $CURR_LANGS_ID > crawler-vars/current_langs
			exit 1
		fi
		CURR_LANGS_ID=$(( $CURR_LANGS_ID + 1 ))
	done
	CURR_LANGS_ID=1
	CURR_WORD_ID=$(( $CURR_WORD_ID + 1 ))
done
echo "----------------------------------------------------------------------------------------------------"
echo " :D  you reached the end of the word list!"
