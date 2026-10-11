curl.exe -s https://httpbin.org/anything --json '{"title":"h1"}' | Select-String '"data"'
