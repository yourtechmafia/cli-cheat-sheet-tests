jq -r '[.body.price, .body.title] | @tsv' books.ndjson | sort
