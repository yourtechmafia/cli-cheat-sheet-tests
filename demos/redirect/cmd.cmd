dir /b notes.txt missing.txt > out.txt 2> errors.txt
type out.txt
type errors.txt
echo first> report.txt
echo second>> report.txt
type report.txt
