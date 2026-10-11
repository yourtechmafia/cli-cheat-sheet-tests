"hi" > hi.txt
[System.IO.File]::ReadAllBytes("$PWD\hi.txt") -join ' '
