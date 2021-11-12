rm output/cadeAllDoclist.templates

cd src/
python3 extract.py ../config/cadeAllDoclist
cd ../scorer/
perl score-ie.pl ../output/cadeAllDoclist.templates ../data/gold_files.templates

