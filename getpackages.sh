#!\bin\bash
echo 'Getting package list from vDir'
cp Main.py vDir/Main.py 
echo 'prepareing Main.py for Checking Packages'
pipreqs vDir/ --savepath rr.txt
echo 'finish'
