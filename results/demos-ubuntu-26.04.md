# Demos on ubuntu-26.04

```json
{
  "python": "3.14.4",
  "platform": "Linux-6.17.0-1022-azure-x86_64-with-glibc2.43",
  "machine": "x86_64",
  "os_release": "Ubuntu 26.04.1 LTS",
  "curl": "curl 8.18.0 (x86_64-pc-linux-gnu) libcurl/8.18.0 OpenSSL/3.5.5 zlib/1.3.1 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.68.0 librtmp/2.3 mit-krb5/1.22.1 OpenLDAP/2.6.10"
}
{
  "bash": "GNU bash, version 5.3.9(1)-release (x86_64-pc-linux-gnu)"
}
```

## alias / bash (exit 0)

```
echo "alias ll='ls -la'" >> ~/.bashrc
```

Output:

```
```

Follow-up in a new interactive shell: `ll notes.txt` (exit 0)

```
bash: cannot set terminal process group (3532): Inappropriate ioctl for device
bash: no job control in this shell
-rw-r--r-- 1 root root 12 Oct 11 12:17 notes.txt
```

## anatomy / bash (exit 0)

```
git init -q practice-repo
cd practice-repo
echo "hello" > README.md
git add README.md
git commit -m "Fix typo"
```

Output:

```
[master (root-commit) a3dab61] Fix typo
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

## and-or / bash (exit 0)

```
mkdir out && echo "created" || echo "failed"
mkdir out && echo "created" || echo "failed"
```

Output:

```
created
mkdir: out: File exists
failed
```

## api-json / bash (exit 0)

```
curl -s https://api.github.com/repos/curl/curl/releases/latest | jq -r '.tag_name, .published_at'
```

Output:

```
curl-8_22_0
2026-09-02T05:59:35Z
```

## double-dash / bash (exit 0)

```
touch -- -oops.txt
ls -oops.txt
ls -- -oops.txt
rm -- -oops.txt
```

Output:

```
error: unexpected argument '-.' found

  tip: to pass '-.' as a value, use '-- -.'

Usage: ls [OPTION]... [FILE]...

For more information, try '--help'.
-oops.txt
```

## env-permanent / bash (exit 0)

```
echo 'export GREETING="hello"' >> ~/.bashrc
source ~/.bashrc
echo $GREETING
```

Output:

```
hello
```

## env-session / bash (exit 0)

```
GREETING="hello"
bash -c 'echo "child sees: [$GREETING]"'
export GREETING
bash -c 'echo "child sees: [$GREETING]"'
```

Output:

```
child sees: []
child sees: [hello]
```

## escape / bash (exit 0)

```
echo "Price: \$5 and a \"quote\""
```

Output:

```
Price: $5 and a "quote"
```

## exit-codes / bash (exit 0)

```
grep zzz log.txt
echo "grep found nothing: $?"
nosuchcommand
echo "command not found: $?"
./hello.sh
echo "not executable: $?"
sh -c 'kill -INT $$'
echo "stopped by Ctrl+C (SIGINT): $?"
```

Output:

```
grep found nothing: 1
bash: line 3: nosuchcommand: command not found
command not found: 127
bash: line 5: ./hello.sh: Permission denied
not executable: 126
stopped by Ctrl+C (SIGINT): 130
```

## help / bash (exit 0)

```
ls --help | head -n 4
```

Output:

```
List directory contents.
Ignore files and directories starting with a '.' by default

Usage: ls [OPTION]... [FILE]...
```

## long-options / bash (exit 0)

```
grep -i -c error log.txt
grep --ignore-case --count error log.txt
```

Output:

```
2
2
```

## ls-missing / bash (exit 0)

```
ls missing.txt
echo "exit code: $?"
```

Output:

```
ls: cannot access 'missing.txt': No such file or directory
exit code: 2
```

## ndjson / bash (exit 0)

```
jq -r '[.body.price, .body.title] | @tsv' books.ndjson | sort
```

Output:

```
£47.82	Sharp Objects
£50.10	Soumission
£51.77	A Light in the Attic
£53.74	Tipping the Velvet
£54.23	Sapiens: A Brief History of Humankind
```

## noclobber / bash (exit 0)

```
set -o noclobber
echo "oops" > notes.txt
cat notes.txt
```

Output:

```
bash: line 2: notes.txt: cannot overwrite existing file
hello
world
```

## path / bash (exit 0)

```
echo $PATH | tr ':' '\n'
```

Output:

```
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/sbin
/bin
```

## pipe / bash (exit 0)

```
grep ERROR log.txt | wc -l
```

Output:

```
2
```

## pipe-objects / bash (exit 0)

```
ls -lS *.txt | head -n 3
```

Output:

```
-rw-r--r-- 1 root root 222 Oct 11 12:17 log.txt
-rw-r--r-- 1 root root  33 Oct 11 12:17 names.txt
-rw-r--r-- 1 root root  12 Oct 11 12:17 notes.txt
```

## quote-json / bash (exit 0)

```
curl -s https://httpbin.org/anything --json '{"title":"h1"}' | grep '"data"'
```

Output:

```
  "data": "{\"title\":\"h1\"}", 
```

## quote-url / bash (exit 0)

```
curl -s "https://httpbin.org/anything?q=cli&page=2" | grep '"args"' -A 3
```

Output:

```
  "args": {
    "page": "2", 
    "q": "cli"
  }, 
```

## quote-url-unquoted / bash (exit 0)

```
curl -s https://httpbin.org/anything?q=cli&page=2
```

Output:

```
{
  "args": {
    "q": "cli"
  }, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/8.18.0", 
    "X-Amzn-Trace-Id": "Root=1-xxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx"
  }, 
  "json": null, 
  "method": "GET", 
  "origin": "203.0.113.7", 
  "url": "https://httpbin.org/anything?q=cli"
}
```

## quotes / bash (exit 0)

```
echo 'Home is $HOME'
echo "Home is $HOME"
```

Output:

```
Home is $HOME
Home is ~
```

## redirect / bash (exit 0)

```
ls notes.txt missing.txt > out.txt 2> errors.txt
cat out.txt
cat errors.txt
echo "first" > report.txt
echo "second" >> report.txt
cat report.txt
ls notes.txt missing.txt > all.txt 2>&1
cat all.txt
```

Output:

```
notes.txt
ls: cannot access 'missing.txt': No such file or directory
first
second
ls: cannot access 'missing.txt': No such file or directory
notes.txt
```

## rm-interactive / bash (exit 0)

```
printf 'n\n' | rm -i notes.txt
ls notes.txt
```

Output:

```
rm: remove regular file 'notes.txt'? notes.txt
```

## script-bash / bash (exit 127)

```
./hello.sh
chmod +x hello.sh
./hello.sh
hello.sh
```

Output:

```
bash: line 1: ./hello.sh: Permission denied
Hello from bash
bash: line 4: hello.sh: command not found
```

## which / bash (exit 0)

```
command -v curl
```

Output:

```
/usr/bin/curl
```

## wildcards / bash (exit 0)

```
echo *.txt
echo "*.txt"
echo *.zzz
```

Output:

```
file.txt log.txt names.txt notes.txt old.txt
*.txt
*.zzz
```
