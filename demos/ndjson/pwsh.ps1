Get-Content books.ndjson | ConvertFrom-Json | ForEach-Object body | Sort-Object price | Format-Table price, title
