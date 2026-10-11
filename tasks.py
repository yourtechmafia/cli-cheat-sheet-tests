"""The 31 everyday command line tasks, one command per shell family, plus a check
that verifies the command did what it claims (not only that it exited 0).

Placeholders the harness fills in:
  {pid}   process id of a throwaway sleeper process (task 29)

A "probe" is a shell-native command that runs after the task's command to show its effect
(for example, print the current folder after `cd`). It is never part of what's being tested:
in portability mode the bash command runs verbatim, followed by each shell's own probe.
  {home}  the home folder the harness uses for the run
"""

import os


def _read(ctx, name):
    path = os.path.join(ctx["cwd"], name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _exists(ctx, *parts):
    return os.path.exists(os.path.join(ctx["cwd"], *parts))


def _out(ctx):
    return ctx["stdout"]


LOG_LINES = [
    "line 1 INFO starting",
    "line 2 INFO loading config",
    "line 3 ERROR config missing",
    "line 4 INFO retrying",
    "line 5 INFO connected",
    "line 6 WARN slow response",
    "line 7 ERROR timeout",
    "line 8 INFO retrying",
    "line 9 INFO done",
    "line 10 INFO exit",
]

FIXTURES = {
    "notes.txt": "hello\nworld\n",
    "log.txt": "\n".join(LOG_LINES) + "\n",
    "names.txt": "banana\napple\nbanana\ncherry\napple\n",
    "old.txt": "rename me\n",
    "file.txt": "delete me\n",
    ".hidden": "secret\n",
    "docs/a.txt": "doc a\n",
    "docs/b.md": "doc b\n",
    "docs/deep/c.txt": "doc c\n",
    "folder/inside.txt": "x\n",
    "hello.sh": "#!/usr/bin/env bash\necho \"Hello from bash\"\n",
    "hello.ps1": "Write-Output \"Hello from PowerShell\"\n",
    "hello.cmd": "@echo off\r\necho Hello from Command Prompt\r\n",
}


def _sorted_unique(ctx):
    lines = [l.strip() for l in _out(ctx).splitlines() if l.strip()]
    return lines == ["apple", "banana", "cherry"]


def _head_tail(ctx):
    o = _out(ctx)
    return all(f"line {n} " in o for n in (1, 2, 3, 8, 9, 10)) and "line 5 " not in o


TASKS = [
    {
        "id": 1, "task": "Where am I (print the current folder)",
        "posix": "pwd", "pwsh": "Get-Location", "cmd": "cd",
        "check": lambda c: os.path.basename(c["cwd"]) in _out(c),
    },
    {
        "id": 2, "task": "List files, including hidden ones",
        "posix": "ls -la", "pwsh": "Get-ChildItem -Force", "cmd": "dir /a",
        "check": lambda c: ".hidden" in _out(c),
    },
    {
        "id": 3, "task": "Change folder",
        "posix": "cd docs", "pwsh": "Set-Location docs", "cmd": "cd docs",
        "probe": {"posix": "pwd", "pwsh": "(Get-Location).Path", "cmd": "cd"},
        "check": lambda c: _out(c).strip().splitlines()[-1].rstrip("\\/").endswith("docs") if _out(c).strip() else False,
    },
    {
        "id": 4, "task": "Go to your home folder",
        "posix": "cd ~", "pwsh": "Set-Location ~", "cmd": "cd /d %USERPROFILE%",
        "probe": {"posix": "pwd", "pwsh": "(Get-Location).Path", "cmd": "cd"},
        "check": lambda c: os.path.basename(c["home"].rstrip("\\/")) in _out(c),
    },
    {
        "id": 5, "task": "Make nested folders",
        "posix": "mkdir -p a/b/c", "pwsh": "New-Item -ItemType Directory -Path a/b/c -Force", "cmd": "mkdir a\\b\\c",
        "check": lambda c: os.path.isdir(os.path.join(c["cwd"], "a", "b", "c")),
    },
    {
        "id": 6, "task": "Create an empty file",
        "posix": "touch empty.txt", "pwsh": "New-Item -ItemType File -Path empty.txt", "cmd": "type nul > empty.txt",
        "check": lambda c: _exists(c, "empty.txt") and os.path.getsize(os.path.join(c["cwd"], "empty.txt")) == 0,
    },
    {
        "id": 7, "task": "Copy a file",
        "posix": "cp notes.txt notes-copy.txt", "pwsh": "Copy-Item notes.txt notes-copy.txt", "cmd": "copy notes.txt notes-copy.txt",
        "check": lambda c: _read(c, "notes-copy.txt") == _read(c, "notes.txt"),
    },
    {
        "id": 8, "task": "Copy a folder",
        "posix": "cp -r docs docs-backup", "pwsh": "Copy-Item docs docs-backup -Recurse", "cmd": "xcopy docs docs-backup /e /i /q",
        "check": lambda c: _exists(c, "docs-backup", "deep", "c.txt"),
    },
    {
        "id": 9, "task": "Move or rename",
        "posix": "mv old.txt new.txt", "pwsh": "Move-Item old.txt new.txt", "cmd": "move old.txt new.txt",
        "check": lambda c: _exists(c, "new.txt") and not _exists(c, "old.txt"),
    },
    {
        "id": 10, "task": "Delete a file",
        "posix": "rm file.txt", "pwsh": "Remove-Item file.txt", "cmd": "del file.txt",
        "check": lambda c: not _exists(c, "file.txt"),
    },
    {
        "id": 11, "task": "Delete a folder and its contents",
        "posix": "rm -r folder", "pwsh": "Remove-Item folder -Recurse", "cmd": "rmdir /s /q folder",
        "check": lambda c: not _exists(c, "folder"),
    },
    {
        "id": 12, "task": "Print a file",
        "posix": "cat notes.txt", "pwsh": "Get-Content notes.txt", "cmd": "type notes.txt",
        "check": lambda c: "hello" in _out(c) and "world" in _out(c),
    },
    {
        "id": 13, "task": "Show the first and last lines",
        "posix": "head -n 3 log.txt\ntail -n 3 log.txt",
        "pwsh": "Get-Content log.txt -TotalCount 3\nGet-Content log.txt -Tail 3",
        "cmd": None,
        "check": _head_tail,
    },
    {
        "id": 14, "task": "Follow a log as it grows",
        "posix": "tail -f log.txt", "pwsh": "Get-Content log.txt -Wait", "cmd": None,
        "follow": True,
        "check": lambda c: "line 11 appended" in _out(c),
    },
    {
        "id": 15, "task": "Search for text in a file",
        "posix": "grep -i error log.txt", "pwsh": "Select-String -Pattern error -Path log.txt", "cmd": "findstr /i error log.txt",
        "check": lambda c: "config missing" in _out(c) and "timeout" in _out(c) and "connected" not in _out(c),
    },
    {
        "id": 16, "task": "Find files by name",
        "posix": "find . -name \"*.txt\"", "pwsh": "Get-ChildItem -Recurse -Filter *.txt", "cmd": "dir /s /b *.txt",
        "check": lambda c: "c.txt" in _out(c) and "notes.txt" in _out(c),
    },
    {
        "id": 17, "task": "Count lines",
        "posix": "wc -l < log.txt", "pwsh": "(Get-Content log.txt | Measure-Object -Line).Lines", "cmd": "find /c /v \"\" < log.txt",
        "check": lambda c: "10" in _out(c).split(),
    },
    {
        "id": 18, "task": "Sort and remove duplicates",
        "posix": "sort -u names.txt", "pwsh": "Get-Content names.txt | Sort-Object -Unique", "cmd": "sort /unique names.txt",
        "check": _sorted_unique,
    },
    {
        "id": 19, "task": "Show the last exit code",
        "posix": "grep zzz log.txt\necho $?", "pwsh": "findstr zzz log.txt\n$LASTEXITCODE", "cmd": "findstr zzz log.txt\necho %ERRORLEVEL%",
        "check": lambda c: _out(c).strip().splitlines()[-1].strip() == "1" if _out(c).strip() else False,
    },
    {
        "id": 20, "task": "Run B only if A succeeds",
        "posix": "mkdir out && echo created", "pwsh": "mkdir out && echo created", "cmd": "mkdir out && echo created",
        "pwsh51": "mkdir out; if ($?) { echo created }",
        "check": lambda c: _exists(c, "out") and "created" in _out(c),
    },
    {
        "id": 21, "task": "Read an environment variable",
        "posix": "echo $HOME", "pwsh": "$env:USERPROFILE", "cmd": "echo %USERPROFILE%",
        "check": lambda c: os.path.basename(c["home"].rstrip("\\/")) in _out(c),
    },
    {
        "id": 22, "task": "Set an environment variable for this session",
        "posix": "export GREETING=hello\necho $GREETING", "pwsh": "$env:GREETING = \"hello\"\n$env:GREETING",
        "cmd": "set GREETING=hello\necho %GREETING%",
        "check": lambda c: "hello" in _out(c),
    },
    {
        "id": 23, "task": "Set an environment variable permanently",
        "posix": "echo 'export GREETING=hello' >> ~/{rcfile}",
        "pwsh": "[Environment]::SetEnvironmentVariable(\"GREETING\", \"hello\", \"User\")",
        "cmd": "setx GREETING hello",
        "persist": True,
        "check": lambda c: "hello" in c.get("persist_out", ""),
    },
    {
        "id": 24, "task": "Show PATH",
        "posix": "echo $PATH", "pwsh": "$env:PATH", "cmd": "echo %PATH%",
        "check": lambda c: len(_out(c).strip()) > 10 and (":" in _out(c) or ";" in _out(c)),
    },
    {
        "id": 25, "task": "Find which program a command runs",
        "posix": "command -v curl", "pwsh": "Get-Command curl", "cmd": "where curl",
        "check": lambda c: "curl" in _out(c).lower(),
    },
    {
        "id": 26, "task": "Get help for a command",
        "posix": "ls --help", "pwsh": "Get-Help Get-ChildItem", "cmd": "dir /?",
        # Help text counts even with a non-zero exit: Command Prompt's /? exits with 1
        "check": lambda c: len(_out(c).strip()) > 50,
    },
    {
        "id": 27, "task": "Search command history",
        "posix": None, "pwsh": None, "cmd": None,
        "interactive": "Ctrl+R in zsh, bash, and PowerShell (PSReadLine); F7 or doskey /history in Command Prompt",
        "check": lambda c: True,
    },
    {
        "id": 28, "task": "Clear the screen",
        "posix": "clear", "pwsh": "Clear-Host", "cmd": "cls",
        "check": lambda c: c["exit"] == 0,
    },
    {
        "id": 29, "task": "List and stop a process",
        "posix": "ps -p {pid}\nkill {pid}",
        "pwsh": "Get-Process -Id {pid}\nStop-Process -Id {pid}",
        "cmd": "tasklist /fi \"PID eq {pid}\"\ntaskkill /pid {pid} /f",
        "sleeper": True,
        "check": lambda c: c.get("sleeper_gone") is True,
    },
    {
        "id": 30, "task": "Download a URL to a file",
        "posix": "curl -sSo page.html https://example.com",
        "pwsh": "Invoke-WebRequest https://example.com -OutFile page.html",
        "cmd": "curl -sSo page.html https://example.com",
        "check": lambda c: "Example Domain" in (_read(c, "page.html") or ""),
    },
    {
        "id": 31, "task": "Run a script",
        "posix": "chmod +x hello.sh\n./hello.sh", "pwsh": ".\\hello.ps1", "cmd": "hello.cmd",
        "check": lambda c: "Hello from" in _out(c),
    },
]
