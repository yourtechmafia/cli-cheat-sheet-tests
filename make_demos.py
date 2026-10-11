"""Write the article's code examples to demos/<name>/ as standalone files.

Each file is exactly what the article shows. demos.py runs them verbatim.
File names: posix.sh (zsh and bash), zsh.sh / bash.sh (one shell only),
pwsh.ps1 (PowerShell 7 and, unless powershell.ps1 exists, Windows PowerShell 5.1),
powershell.ps1 (5.1 only), cmd.cmd. Add .darwin/.linux before the extension for
OS-specific files. meta.json holds runner options.
"""

import json
import os

D = {}

# --- How to read and run commands --------------------------------------------
D["anatomy"] = {
    "posix.sh": 'git init -q practice-repo\ncd practice-repo\necho "hello" > README.md\ngit add README.md\ngit commit -m "Fix typo"\n',
    "meta.json": {"os": ["darwin", "linux"], "env": {"GIT_AUTHOR_NAME": "Demo", "GIT_AUTHOR_EMAIL": "demo@example.com",
                                                    "GIT_COMMITTER_NAME": "Demo", "GIT_COMMITTER_EMAIL": "demo@example.com"}},
}
D["double-dash"] = {
    "posix.sh": "touch -- -oops.txt\nls -oops.txt\nls -- -oops.txt\nrm -- -oops.txt\n",
    "pwsh.ps1": "New-Item -ItemType File \"-oops.txt\" | Out-Null\nGet-ChildItem -oops.txt\nGet-ChildItem \"-oops.txt\" -Name\nRemove-Item \"-oops.txt\"\n",
    "cmd.cmd": "type nul > -oops.txt\ndir /b -oops.txt\ndel -oops.txt\n",
}
D["long-options"] = {
    "posix.sh": "grep -i -c error log.txt\ngrep --ignore-case --count error log.txt\n",
    "pwsh.ps1": "Get-ChildItem -Recurse -Filter *.md | Select-Object -ExpandProperty Name\ngci -r -fi *.md | Select-Object -ExpandProperty Name\n",
}
D["help"] = {
    "posix.linux.sh": "ls --help | head -n 4\n",
    "posix.darwin.sh": "man ls | col -b | head -n 6\n",
    "pwsh.ps1": "Update-Help -Module Microsoft.PowerShell.Management -Scope CurrentUser\nGet-Help Get-ChildItem -Examples\n",
    "powershell.ps1": "Update-Help -Module Microsoft.PowerShell.Management\nGet-Help Get-ChildItem -Examples\n",
    "cmd.cmd": "dir /? | find \"Displays\"\necho Exit code: %ERRORLEVEL%\n",
    "meta.json": {"network": True, "timeout": 180},
}
D["alias"] = {
    "zsh.sh": "echo \"alias ll='ls -la'\" >> ~/.zshrc\n",
    "bash.sh": "echo \"alias ll='ls -la'\" >> ~/.bashrc\n",
    "pwsh.ps1": "New-Item -ItemType File -Path $PROFILE -Force | Out-Null\nAdd-Content -Path $PROFILE -Value 'function ll { Get-ChildItem -Force @args }'\n",
    "cmd.cmd": "doskey ll=dir /a $*\nll\n",
    "meta.json": {"followup": "ll notes.txt"},
}

D["bash-in-powershell"] = {
    "pwsh.ps1": ("ls -la\nsort -u names.txt\ngrep zzz log.txt\necho $?\necho $PATH\n"
                 "find . -name \"*.txt\"\ncp -r docs docs-backup\nTest-Path docs-backup\\deep\\c.txt\n"),
    "meta.json": {"os": ["windows"]},
}

# --- Pipes, redirection, exit codes --------------------------------------------
D["pipe"] = {
    "posix.sh": "grep ERROR log.txt | wc -l\n",
    "pwsh.ps1": "Select-String -Path log.txt -Pattern ERROR | Measure-Object | Select-Object -ExpandProperty Count\n",
    "cmd.cmd": "findstr ERROR log.txt | find /c /v \"\"\n",
}
D["pipe-objects"] = {
    "posix.sh": "ls -lS *.txt | head -n 3\n",
    "pwsh.ps1": "Get-ChildItem *.txt | Sort-Object Length -Descending | Select-Object -First 3 Name, Length\n",
}
D["redirect"] = {
    "posix.sh": ("ls notes.txt missing.txt > out.txt 2> errors.txt\n"
                 "cat out.txt\ncat errors.txt\n"
                 "echo \"first\" > report.txt\necho \"second\" >> report.txt\ncat report.txt\n"
                 "ls notes.txt missing.txt > all.txt 2>&1\ncat all.txt\n"),
    "pwsh.ps1": ("Get-ChildItem notes.txt, missing.txt -Name > out.txt 2> errors.txt\n"
                 "Get-Content out.txt\nGet-Content errors.txt\n"
                 "\"first\" > report.txt\n\"second\" >> report.txt\nGet-Content report.txt\n"),
    "cmd.cmd": ("dir /b notes.txt missing.txt > out.txt 2> errors.txt\n"
                "type out.txt\ntype errors.txt\n"
                "echo first> report.txt\necho second>> report.txt\ntype report.txt\n"),
}
D["redirect-encoding"] = {
    "pwsh.ps1": "\"hi\" > hi.txt\n[System.IO.File]::ReadAllBytes(\"$PWD\\hi.txt\") -join ' '\n",
    "meta.json": {"os": ["windows"]},
}
D["echo-space"] = {
    "cmd.cmd": "echo first > spaced.txt\necho first> tight.txt\nfor %%f in (spaced.txt tight.txt) do echo %%f: %%~zf bytes\n",
}
D["exit-codes"] = {
    "posix.sh": ("grep zzz log.txt\necho \"grep found nothing: $?\"\n"
                 "nosuchcommand\necho \"command not found: $?\"\n"
                 "./hello.sh\necho \"not executable: $?\"\n"
                 "sh -c 'kill -INT $$'\necho \"stopped by Ctrl+C (SIGINT): $?\"\n"),
    "pwsh.ps1": ("findstr zzz log.txt\n\"findstr exit code: $LASTEXITCODE\"\n"
                 "nosuchcommand\n\"last command succeeded: $?\"\n"),
    "cmd.cmd": ("findstr zzz log.txt\necho findstr exit code: %ERRORLEVEL%\n"
                "nosuchcommand\necho command not found: %ERRORLEVEL%\n"),
}
D["ls-missing"] = {
    "posix.sh": "ls missing.txt\necho \"exit code: $?\"\n",
}
D["and-or"] = {
    "posix.sh": "mkdir out && echo \"created\" || echo \"failed\"\nmkdir out && echo \"created\" || echo \"failed\"\n",
    "pwsh.ps1": "mkdir out && echo \"created\" || echo \"failed\"\nmkdir out && echo \"created\" || echo \"failed\"\n",
    "powershell.ps1": "mkdir out && echo \"created\"\n",
    "cmd.cmd": "mkdir out && echo created || echo failed\nmkdir out && echo created || echo failed\n",
}
D["and-or-51"] = {
    "powershell.ps1": "mkdir out | Out-Null; if ($?) { \"created\" } else { \"failed\" }\nmkdir out 2>$null | Out-Null; if ($?) { \"created\" } else { \"failed\" }\n",
    "meta.json": {"os": ["windows"]},
}

# --- Environment variables and PATH --------------------------------------------
D["env-session"] = {
    "posix.sh": ("GREETING=\"hello\"\nbash -c 'echo \"child sees: [$GREETING]\"'\n"
                 "export GREETING\nbash -c 'echo \"child sees: [$GREETING]\"'\n"),
    "pwsh.ps1": "$env:GREETING = \"hello\"\n$env:GREETING\n",
    "cmd.cmd": "set GREETING=hello\necho %GREETING%\n",
}
D["set-spaces"] = {
    "cmd.cmd": "set GREETING = hello\necho [%GREETING%]\necho [%GREETING %]\n",
}
D["env-permanent"] = {
    "zsh.sh": "echo 'export GREETING=\"hello\"' >> ~/.zshrc\nsource ~/.zshrc\necho $GREETING\n",
    "bash.sh": "echo 'export GREETING=\"hello\"' >> ~/.bashrc\nsource ~/.bashrc\necho $GREETING\n",
    "pwsh.ps1": ("[Environment]::SetEnvironmentVariable(\"GREETING\", \"hello\", \"User\")\n"
                 "[Environment]::GetEnvironmentVariable(\"GREETING\", \"User\")\n"
                 "\"this session: [$env:GREETING]\"\n"),
    "cmd.cmd": "setx GREETING hello\necho this session: [%GREETING%]\n",
    "meta.json": {"cleanup_user_env": ["GREETING"]},
}
D["setx-truncate"] = {
    "pwsh.ps1": "setx LONGVAR (\"x\" * 1100)\n",
    "meta.json": {"os": ["windows"], "cleanup_user_env": ["LONGVAR"]},
}
D["homebrew-path"] = {
    "zsh.darwin.sh": ("brew --version\n"
                      "echo 'eval \"$(/opt/homebrew/bin/brew shellenv zsh)\"' >> ~/.zprofile\n"
                      "eval \"$(/opt/homebrew/bin/brew shellenv zsh)\"\n"
                      "brew --version\n"),
    "meta.json": {"os": ["darwin"]},
}
D["which"] = {
    "posix.sh": "command -v curl\n",
    "pwsh.ps1": "Get-Command curl | Format-Table CommandType, Name, Definition -AutoSize\n",
    "cmd.cmd": "where curl\n",
}
D["path"] = {
    "posix.sh": "echo $PATH | tr ':' '\\n'\n",
    "pwsh.ps1": "$env:PATH -split ';'\n",
    "cmd.cmd": "echo %PATH:;=&echo.%\n",
}

# --- Quoting and wildcards ---------------------------------------------------------
D["quotes"] = {
    "posix.sh": "echo 'Home is $HOME'\necho \"Home is $HOME\"\n",
    "pwsh.ps1": "'Home is $HOME'\n\"Home is $HOME\"\n",
    "cmd.cmd": "echo 'Home is %USERPROFILE%'\necho \"Home is %USERPROFILE%\"\n",
}
D["quote-url"] = {
    "posix.sh": "curl -s \"https://httpbin.org/anything?q=cli&page=2\" | grep '\"args\"' -A 3\n",
    "pwsh.ps1": "curl.exe -s \"https://httpbin.org/anything?q=cli&page=2\" | Select-String '\"page\"', '\"q\"'\n",
    "cmd.cmd": "curl -s \"https://httpbin.org/anything?q=cli&page=2\" | findstr /c:\"page\" /c:\"\\\"q\\\"\"\n",
    "meta.json": {"network": True},
}
D["quote-url-unquoted"] = {
    "posix.sh": "curl -s https://httpbin.org/anything?q=cli&page=2\n",
    "meta.json": {"network": True},
}
D["quote-json"] = {
    "posix.sh": "curl -s https://httpbin.org/anything --json '{\"title\":\"h1\"}' | grep '\"data\"'\n",
    "pwsh.ps1": "curl.exe -s https://httpbin.org/anything --json '{\"title\":\"h1\"}' | Select-String '\"data\"'\n",
    "cmd.cmd": ("curl -s https://httpbin.org/anything --json '{\"title\":\"h1\"}' | findstr /c:\"data\"\n"
                "curl -s https://httpbin.org/anything --json \"{\\\"title\\\":\\\"h1\\\"}\" | findstr /c:\"data\"\n"),
    "meta.json": {"network": True},
}
D["escape"] = {
    "posix.sh": "echo \"Price: \\$5 and a \\\"quote\\\"\"\n",
    "pwsh.ps1": "\"Price: `$5 and a `\"quote`\"\"\n",
    "cmd.cmd": "echo Price: $5 and a ^<tag^>\n",
}
D["wildcards"] = {
    "posix.sh": "echo *.txt\necho \"*.txt\"\necho *.zzz\n",
    "pwsh.ps1": "echo *.txt\nGet-ChildItem *.txt -Name\n",
    "cmd.cmd": "echo *.txt\ndir /b *.txt\n",
}

# --- Scripts and scheduling --------------------------------------------------------
D["script-bash"] = {
    "posix.sh": "./hello.sh\nchmod +x hello.sh\n./hello.sh\nhello.sh\n",
}
D["script-pwsh"] = {
    "pwsh.ps1": "hello.ps1\n.\\hello.ps1\n",
    "cmd.cmd": "hello.cmd\n",
    "meta.json": {"os": ["windows"]},
}
D["execution-policy"] = {
    "powershell.ps1": ".\\hello.ps1\n",
    "meta.json": {"os": ["windows"], "pwsh_args": ["-ExecutionPolicy", "Restricted"]},
}
D["execution-policy-fix"] = {
    "powershell.ps1": ("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force\n"
                       "Get-ExecutionPolicy -Scope CurrentUser\n"
                       "Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser -Force\n"),
    "meta.json": {"os": ["windows"]},
}
D["schtasks"] = {
    "cmd.cmd": ("schtasks /create /tn \"HelloScript\" /tr \"%CD%\\hello.cmd\" /sc daily /st 08:00 /f\n"
                "schtasks /query /tn \"HelloScript\"\nschtasks /delete /tn \"HelloScript\" /f\n"),
    "meta.json": {"os": ["windows"]},
}
D["register-task"] = {
    "pwsh.ps1": ("$action  = New-ScheduledTaskAction -Execute \"pwsh.exe\" -Argument \"-File $PWD\\hello.ps1\"\n"
                 "$trigger = New-ScheduledTaskTrigger -Daily -At 8am\n"
                 "Register-ScheduledTask -TaskName \"HelloScript\" -Action $action -Trigger $trigger | Select-Object TaskName, State\n"
                 "Unregister-ScheduledTask -TaskName \"HelloScript\" -Confirm:$false\n"),
    "meta.json": {"os": ["windows"], "only": ["pwsh"]},
}

# --- Web data ---------------------------------------------------------------------------
D["api-json"] = {
    "posix.sh": "curl -s https://api.github.com/repos/curl/curl/releases/latest | jq -r '.tag_name, .published_at'\n",
    "pwsh.ps1": "Invoke-RestMethod https://api.github.com/repos/curl/curl/releases/latest | Select-Object tag_name, published_at\n",
    "meta.json": {"network": True},
}
D["ndjson"] = {
    "posix.sh": "jq -r '[.body.price, .body.title] | @tsv' books.ndjson | sort\n",
    "pwsh.ps1": "Get-Content books.ndjson | ConvertFrom-Json | ForEach-Object body | Sort-Object price | Format-Table price, title\n",
    "meta.json": {"extra_files": ["ndjson/books.ndjson"]},
}
D["ndjson-51"] = {
    "powershell.ps1": "Get-Content books.ndjson -Encoding UTF8 | ConvertFrom-Json | ForEach-Object body | Sort-Object price | Format-Table price, title\n",
    "meta.json": {"os": ["windows"], "extra_files": ["ndjson/books.ndjson"]},
}

# --- Safety ------------------------------------------------------------------------------
D["whatif"] = {
    "pwsh.ps1": "Remove-Item folder -Recurse -WhatIf\n",
}
D["rm-interactive"] = {
    "posix.sh": "printf 'n\\n' | rm -i notes.txt\nls notes.txt\n",
}
D["noclobber"] = {
    "posix.sh": "set -o noclobber\necho \"oops\" > notes.txt\ncat notes.txt\n",
    "pwsh.ps1": "\"oops\" | Out-File notes.txt -NoClobber\nGet-Content notes.txt\n",
}


def main():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demos")
    for name, files in D.items():
        folder = os.path.join(root, name)
        os.makedirs(folder, exist_ok=True)
        for fname, content in files.items():
            path = os.path.join(folder, fname)
            if fname == "meta.json":
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=2)
                continue
            newline = "\r\n" if fname.endswith(".cmd") else "\n"
            with open(path, "w", encoding="utf-8", newline=newline) as f:
                f.write(content)
    print(f"wrote {len(D)} demos to {root}")


if __name__ == "__main__":
    main()
