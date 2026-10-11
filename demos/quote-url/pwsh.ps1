curl.exe -s "https://httpbin.org/anything?q=cli&page=2" | Select-String '"page"', '"q"'
