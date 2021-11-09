#NOTE: run in development-anskeys
#TODO: adjust to ask the user for a percentage of the total files

rm ../gold_files.templates
for file in *; do echo $file >> ../list_of_files.txt; done
cat $(cat ../list_of_files.txt) >> gold_files.templates
mv gold_files.templates ../
