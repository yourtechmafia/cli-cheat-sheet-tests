Get-ChildItem *.txt | Sort-Object Length -Descending | Select-Object -First 3 Name, Length
