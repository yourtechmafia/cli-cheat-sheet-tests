Get-ChildItem -Recurse -Filter *.md | Select-Object -ExpandProperty Name
gci -r -fi *.md | Select-Object -ExpandProperty Name
