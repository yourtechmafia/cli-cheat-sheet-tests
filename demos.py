"""Run every code example the article shows, verbatim, in every shell on this machine.

Each folder in demos/ holds one example as standalone files (see make_demos.py).
The runner copies nothing into the command: it feeds the file to the real shell
inside a fresh practice folder (the same fixtures as the cheat sheet), with the
OS's stock PATH and, on macOS and Linux, a throwaway HOME. stdout and stderr are
merged, in order, the way a terminal shows them.

Usage:
    python demos.py --label my-mac            # all demos
    python demos.py --label my-mac pipe       # only demos whose name contains "pipe"

Results go to results/demos-<label>.json and results/demos-<label>.md.
"""

import argparse
import base64
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

from harness import IS_WINDOWS, machine_info, make_practice, shells, stock_path, version_of

HERE = os.path.dirname(os.path.abspath(__file__))
DEMOS = os.path.join(HERE, "demos")
OS_NAME = "windows" if IS_WINDOWS else ("darwin" if sys.platform == "darwin" else "linux")
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
IPV4 = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
TRACE = re.compile(r"Root=1-[0-9a-f]+-[0-9a-f]+")
# Not part of any example. A console window draws Unicode directly; a redirected PowerShell
# writes in the OEM code page unless told otherwise, so we ask for UTF-8 to capture what the
# screen would show. Windows PowerShell 5.1 also prints a progress record on first use.
PS_SETUP = "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\n"
PS51_SETUP = PS_SETUP + "$ProgressPreference = 'SilentlyContinue'\n"


def pick_file(folder, shell, family):
    ext = {"posix": "sh", "pwsh": "ps1", "pwsh51": "ps1", "cmd": "cmd"}[family]
    if family == "posix":
        names = [f"{shell}.{OS_NAME}.sh", f"{shell}.sh", f"posix.{OS_NAME}.sh", "posix.sh"]
    elif family == "pwsh":
        names = [f"pwsh.{OS_NAME}.ps1", "pwsh.ps1"]
    elif family == "pwsh51":
        names = [f"powershell.{OS_NAME}.ps1", "powershell.ps1", f"pwsh.{OS_NAME}.ps1", "pwsh.ps1"]
    else:
        names = [f"cmd.{OS_NAME}.{ext}", f"cmd.{ext}"]
    for n in names:
        if os.path.exists(os.path.join(folder, n)):
            return n
    return None


def argv_for(shell, family, path, text, extra):
    exe = shutil.which(shell)
    if family == "posix":
        return [shell, "-s"], open(path, "rb")  # script on stdin: errors read "bash: line 3: ..." not a temp path
    if family in ("pwsh", "pwsh51"):
        body = (PS51_SETUP if family == "pwsh51" else PS_SETUP) + text
        enc = base64.b64encode(body.encode("utf-16-le")).decode("ascii")
        return [exe, *extra, "-NoProfile", "-NonInteractive", "-OutputFormat", "Text", "-EncodedCommand", enc], subprocess.DEVNULL
    return [exe, "/d", "/c", path], subprocess.DEVNULL


def clean(text, cwd, home):
    text = ANSI.sub("", text).replace("\r\n", "\n")
    text = TRACE.sub("Root=1-xxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx", IPV4.sub("203.0.113.7", text))  # no real IPs in results
    for real, shown in ((cwd, "~/practice"), (home, "~")):
        if real:
            text = text.replace(real, shown).replace(os.path.realpath(real), shown)
    return text


def run_demo(name, root):
    folder = os.path.join(DEMOS, name)
    meta = {}
    if os.path.exists(os.path.join(folder, "meta.json")):
        with open(os.path.join(folder, "meta.json"), encoding="utf-8") as f:
            meta = json.load(f)
    if "os" in meta and OS_NAME not in meta["os"]:
        return []
    out = []
    for shell, family in shells():
        if "only" in meta and shell not in meta["only"]:
            continue
        fname = pick_file(folder, shell, family)
        if not fname:
            continue
        cwd = make_practice(root)
        for extra in meta.get("extra_files", []):
            shutil.copy(os.path.join(DEMOS, extra), os.path.join(cwd, os.path.basename(extra)))
        env = dict(os.environ)
        env["PATH"] = stock_path()
        env.setdefault("TERM", "xterm-256color")
        env.update(meta.get("env", {}))
        if IS_WINDOWS:
            home = env.get("USERPROFILE", "")
        else:
            home = tempfile.mkdtemp(prefix="home-", dir=root)
            env["HOME"] = home
            for rc in (".zshrc", ".bashrc"):
                open(os.path.join(home, rc), "a").close()
        # cmd files run from the practice folder so relative names behave like typing them
        path = os.path.join(folder, fname)
        if family == "cmd":
            path = os.path.join(cwd, "_demo.cmd")
            with open(os.path.join(folder, fname), encoding="utf-8") as src:
                body = src.read()
            with open(path, "w", encoding="ascii", newline="\r\n") as f:
                f.write("@echo off\n" + body)
        with open(os.path.join(folder, fname), encoding="utf-8") as f:
            text = f.read()
        argv, stdin = argv_for(shell, family, path, text, meta.get("pwsh_args", []) if family != "posix" else [])
        try:
            p = subprocess.run(argv, executable=shutil.which(shell), cwd=cwd, env=env, stdin=stdin, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, timeout=meta.get("timeout", 60))
            code, output = p.returncode, p.stdout.decode("utf-8", "replace")
        except subprocess.TimeoutExpired:
            code, output = None, "timed out"
        finally:
            if hasattr(stdin, "close"):
                stdin.close()
        rec = {"demo": name, "shell": shell, "file": fname, "code": text, "exit": code,
               "output": clean(output, cwd, home)}
        followup = meta.get("followup")
        if followup and family == "posix":
            fp = subprocess.run([shutil.which(shell), "-i", "-c", followup], cwd=cwd, env=env,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
            rec["followup"] = {"command": followup, "exit": fp.returncode,
                               "output": clean(fp.stdout.decode("utf-8", "replace"), cwd, home)}
        elif followup and family in ("pwsh", "pwsh51"):
            fp = subprocess.run([shutil.which(shell), "-NonInteractive", "-Command", followup], cwd=cwd, env=env,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
            rec["followup"] = {"command": followup, "exit": fp.returncode,
                               "output": clean(fp.stdout.decode("utf-8", "replace"), cwd, home)}
        if IS_WINDOWS:
            for var in meta.get("cleanup_user_env", []):
                subprocess.run(["powershell", "-NoProfile", "-Command",
                                f"[Environment]::SetEnvironmentVariable('{var}',$null,'User')"], capture_output=True)
        out.append(rec)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", default=platform.node() or "local")
    parser.add_argument("only", nargs="*")
    args = parser.parse_args()

    root = tempfile.mkdtemp(prefix="cli-demos-")
    report = {"label": args.label, "machine": machine_info(),
              "shells": {s: version_of(s) for s, _ in shells()}, "demos": []}
    names = sorted(n for n in os.listdir(DEMOS) if os.path.isdir(os.path.join(DEMOS, n)))
    if args.only:
        names = [n for n in names if any(o in n for o in args.only)]
    for name in names:
        try:
            recs = run_demo(name, root)
        except Exception as exc:  # noqa: BLE001  one broken example must not hide the others
            recs = [{"demo": name, "shell": "-", "file": "-", "code": "", "exit": None, "output": f"runner error: {exc}"}]
        for rec in recs:
            report["demos"].append(rec)
            print(f"[{rec['shell']:10}] exit {str(rec['exit']):>4}  {name}", flush=True)
    shutil.rmtree(root, ignore_errors=True)

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    stem = os.path.join(HERE, "results", "demos-" + args.label)
    with open(stem + ".json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    with open(stem + ".md", "w", encoding="utf-8") as f:
        f.write(f"# Demos on {args.label}\n\n```json\n{json.dumps(report['machine'], indent=2)}\n"
                f"{json.dumps(report['shells'], indent=2)}\n```\n")
        for rec in report["demos"]:
            f.write(f"\n## {rec['demo']} / {rec['shell']} (exit {rec['exit']})\n\n```\n{rec['code']}```\n\n"
                    f"Output:\n\n```\n{rec['output']}```\n")
            if "followup" in rec:
                fu = rec["followup"]
                f.write(f"\nFollow-up in a new interactive shell: `{fu['command']}` (exit {fu['exit']})\n\n"
                        f"```\n{fu['output']}```\n")


if __name__ == "__main__":
    main()
