#!/bin/bash

for API_KEY in 299a9265-9746-4b40-a13f-b1cb0a7d3f1d ace0cfca-d881-48dd-985a-c0ebd1b9bb53 f5331829-ad6c-4b3d-832d-dcae0306b68b; do ./crawler-babelnet.sh JSON_FINAL/true_true/first20.txt JSON_FINAL/true_true/ $API_KEY; done
for API_KEY in 299a9265-9746-4b40-a13f-b1cb0a7d3f1d ace0cfca-d881-48dd-985a-c0ebd1b9bb53 f5331829-ad6c-4b3d-832d-dcae0306b68b; do ./crawler-babelnet.sh JSON_FINAL/false_true/first20.txt JSON_FINAL/false_true/ $API_KEY; done
for API_KEY in 299a9265-9746-4b40-a13f-b1cb0a7d3f1d ace0cfca-d881-48dd-985a-c0ebd1b9bb53 f5331829-ad6c-4b3d-832d-dcae0306b68b; do ./crawler-babelnet.sh JSON_FINAL/false_false/first20.txt JSON_FINAL/false_false/ $API_KEY; done
for API_KEY in 299a9265-9746-4b40-a13f-b1cb0a7d3f1d ace0cfca-d881-48dd-985a-c0ebd1b9bb53 f5331829-ad6c-4b3d-832d-dcae0306b68b; do ./crawler-babelnet.sh JSON_FINAL/monolingual/first20.txt JSON_FINAL/monolingual/ $API_KEY; done
for API_KEY in 299a9265-9746-4b40-a13f-b1cb0a7d3f1d ace0cfca-d881-48dd-985a-c0ebd1b9bb53 f5331829-ad6c-4b3d-832d-dcae0306b68b; do ./crawler-babelnet.sh JSON_FINAL/multilingual/first20.txt JSON_FINAL/multilingual/ $API_KEY; done
