ls notes.txt missing.txt > out.txt 2> errors.txt
cat out.txt
cat errors.txt
echo "first" > report.txt
echo "second" >> report.txt
cat report.txt
ls notes.txt missing.txt > all.txt 2>&1
cat all.txt
