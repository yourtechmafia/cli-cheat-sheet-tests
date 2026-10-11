# Demos on macos-ci

```json
{
  "python": "3.14.7",
  "platform": "macOS-26.6.2-arm64-arm-64bit-Mach-O",
  "machine": "arm64",
  "macos": "26.6.2",
  "curl": "curl 8.7.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1"
}
{
  "zsh": "zsh 5.9 (arm64-apple-darwin25.0)",
  "bash": "GNU bash, version 3.2.57(1)-release (arm64-apple-darwin25)"
}
```

## alias / zsh (exit 0)

```
echo "alias ll='ls -la'" >> ~/.zshrc
```

Output:

```
```

Follow-up in a new interactive shell: `ll notes.txt` (exit 0)

```
-rw-r--r--  1 runner  staff  12 Oct 11 11:56 notes.txt
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
bash: no job control in this shell
-rw-r--r--  1 runner  staff  12 Oct 11 11:56 notes.txt
```

## anatomy / zsh (exit 0)

```
git init -q practice-repo
cd practice-repo
echo "hello" > README.md
git add README.md
git commit -m "Fix typo"
```

Output:

```
[main (root-commit) 9637d00] Fix typo
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
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
[main (root-commit) 9637d00] Fix typo
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

## and-or / zsh (exit 0)

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

## api-json / zsh (exit 0)

```
curl -s https://api.github.com/repos/curl/curl/releases/latest | jq -r '.tag_name, .published_at'
```

Output:

```
null
null
```

## api-json / bash (exit 0)

```
curl -s https://api.github.com/repos/curl/curl/releases/latest | jq -r '.tag_name, .published_at'
```

Output:

```
null
null
```

## double-dash / zsh (exit 0)

```
touch -- -oops.txt
ls -oops.txt
ls -- -oops.txt
rm -- -oops.txt
```

Output:

```
ls: invalid option -- .
usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
-oops.txt
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
ls: invalid option -- .
usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
-oops.txt
```

## env-permanent / zsh (exit 0)

```
echo 'export GREETING="hello"' >> ~/.zshrc
source ~/.zshrc
echo $GREETING
```

Output:

```
hello
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

## env-session / zsh (exit 0)

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

## escape / zsh (exit 0)

```
echo "Price: \$5 and a \"quote\""
```

Output:

```
Price: $5 and a "quote"
```

## escape / bash (exit 0)

```
echo "Price: \$5 and a \"quote\""
```

Output:

```
Price: $5 and a "quote"
```

## exit-codes / zsh (exit 0)

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
zsh: command not found: nosuchcommand
command not found: 127
zsh: permission denied: ./hello.sh
not executable: 126
stopped by Ctrl+C (SIGINT): 130
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

## help / zsh (exit 0)

```
man ls | col -b | head -n 6
```

Output:

```
LS(1)			    General Commands Manual			 LS(1)

NAME
     ls – list directory contents

SYNOPSIS
```

## help / bash (exit 0)

```
man ls | col -b | head -n 6
```

Output:

```
LS(1)			    General Commands Manual			 LS(1)

NAME
     ls – list directory contents

SYNOPSIS
```

## homebrew-path / zsh (exit 0)

```
brew --version
echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv zsh)"
brew --version
```

Output:

```
zsh: command not found: brew
Homebrew 6.0.22
Homebrew/homebrew-core (git revision 3cc40d0f3a3; last commit 2026-09-07)
Homebrew/homebrew-cask (git revision 3b664150524; last commit 2026-09-07)
```

## long-options / zsh (exit 0)

```
grep -i -c error log.txt
grep --ignore-case --count error log.txt
```

Output:

```
2
2
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

## ls-missing / zsh (exit 0)

```
ls missing.txt
echo "exit code: $?"
```

Output:

```
ls: missing.txt: No such file or directory
exit code: 1
```

## ls-missing / bash (exit 0)

```
ls missing.txt
echo "exit code: $?"
```

Output:

```
ls: missing.txt: No such file or directory
exit code: 1
```

## ndjson / zsh (exit 0)

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

## noclobber / zsh (exit 0)

```
set -o noclobber
echo "oops" > notes.txt
cat notes.txt
```

Output:

```
zsh: file exists: notes.txt
hello
world
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

## path / zsh (exit 0)

```
echo $PATH | tr ':' '\n'
```

Output:

```
/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbin
```

## path / bash (exit 0)

```
echo $PATH | tr ':' '\n'
```

Output:

```
/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbin
```

## pipe / zsh (exit 0)

```
grep ERROR log.txt | wc -l
```

Output:

```
       2
```

## pipe / bash (exit 0)

```
grep ERROR log.txt | wc -l
```

Output:

```
       2
```

## pipe-objects / zsh (exit 0)

```
ls -lS *.txt | head -n 3
```

Output:

```
-rw-r--r--  1 runner  staff  222 Oct 11 11:56 log.txt
-rw-r--r--  1 runner  staff   33 Oct 11 11:56 names.txt
-rw-r--r--  1 runner  staff   12 Oct 11 11:56 notes.txt
```

## pipe-objects / bash (exit 0)

```
ls -lS *.txt | head -n 3
```

Output:

```
-rw-r--r--  1 runner  staff  222 Oct 11 11:56 log.txt
-rw-r--r--  1 runner  staff   33 Oct 11 11:56 names.txt
-rw-r--r--  1 runner  staff   12 Oct 11 11:56 notes.txt
```

## quote-json / zsh (exit 0)

```
curl -s https://httpbin.org/anything --json '{"title":"h1"}' | grep '"data"'
```

Output:

```
  "data": "{\"title\":\"h1\"}", 
```

## quote-json / bash (exit 0)

```
curl -s https://httpbin.org/anything --json '{"title":"h1"}' | grep '"data"'
```

Output:

```
  "data": "{\"title\":\"h1\"}", 
```

## quote-url / zsh (exit 0)

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

## quote-url-unquoted / zsh (exit 0)

```
curl -s https://httpbin.org/anything?q=cli&page=2
```

Output:

```
zsh: no matches found: https://httpbin.org/anything?q=cli
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
    "User-Agent": "curl/8.7.1", 
    "X-Amzn-Trace-Id": "Root=1-xxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx"
  }, 
  "json": null, 
  "method": "GET", 
  "origin": "203.0.113.7", 
  "url": "https://httpbin.org/anything?q=cli"
}
```

## quotes / zsh (exit 0)

```
echo 'Home is $HOME'
echo "Home is $HOME"
```

Output:

```
Home is $HOME
Home is ~
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

## redirect / zsh (exit 0)

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
ls: missing.txt: No such file or directory
first
second
ls: missing.txt: No such file or directory
notes.txt
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
ls: missing.txt: No such file or directory
first
second
ls: missing.txt: No such file or directory
notes.txt
```

## rm-interactive / zsh (exit 0)

```
printf 'n\n' | rm -i notes.txt
ls notes.txt
```

Output:

```
remove notes.txt? notes.txt
```

## rm-interactive / bash (exit 0)

```
printf 'n\n' | rm -i notes.txt
ls notes.txt
```

Output:

```
remove notes.txt? notes.txt
```

## script-bash / zsh (exit 127)

```
./hello.sh
chmod +x hello.sh
./hello.sh
hello.sh
```

Output:

```
zsh: permission denied: ./hello.sh
Hello from bash
zsh: command not found: hello.sh
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

## which / zsh (exit 0)

```
command -v curl
```

Output:

```
/usr/bin/curl
```

## which / bash (exit 0)

```
command -v curl
```

Output:

```
/usr/bin/curl
```

## wildcards / zsh (exit 1)

```
echo *.txt
echo "*.txt"
echo *.zzz
```

Output:

```
file.txt log.txt names.txt notes.txt old.txt
*.txt
zsh: no matches found: *.zzz
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
