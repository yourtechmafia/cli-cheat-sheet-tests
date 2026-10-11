curl -s https://api.github.com/repos/curl/curl/releases/latest | jq -r '.tag_name, .published_at'
