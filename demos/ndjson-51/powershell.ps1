Get-Content books.ndjson -Encoding UTF8 | ConvertFrom-Json | ForEach-Object body | Sort-Object price | Format-Table price, title
