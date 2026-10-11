Get-ChildItem notes.txt, missing.txt -Name > out.txt 2> errors.txt
Get-Content out.txt
Get-Content errors.txt
"first" > report.txt
"second" >> report.txt
Get-Content report.txt
