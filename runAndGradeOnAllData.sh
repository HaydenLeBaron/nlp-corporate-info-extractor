rm output/allDoclist.templates

cd src/
python3 extract.py ../config/allDoclist -v
cd ../scorer/
perl score-ie.pl ../output/allDoclist.templates ../data/gold_files.templates

