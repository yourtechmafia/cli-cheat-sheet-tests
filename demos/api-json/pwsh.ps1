Invoke-RestMethod https://api.github.com/repos/curl/curl/releases/latest | Select-Object tag_name, published_at
