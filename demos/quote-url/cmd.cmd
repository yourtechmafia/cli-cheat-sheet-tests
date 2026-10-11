curl -s "https://httpbin.org/anything?q=cli&page=2" | findstr /c:"page" /c:"\"q\""
