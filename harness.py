"""Run the cheat sheet's 31 tasks in every shell available on this machine.

Each command is executed by the real shell (zsh, bash, pwsh, powershell, cmd)
inside a fresh practice folder full of throwaway files, and then checked for
its effect: the file exists, the output contains the right lines, the process
is gone. Nothing runs in your real home folder: on macOS and Linux the harness
points HOME at a temporary folder.

Usage:
    python harness.py                 # native commands for each shell
    python harness.py --portability   # run the bash/zsh command, verbatim, in every shell
    python harness.py --label my-mac  # name for the results file

Results are written to results/<label>[-portability].json and .csv.
"""

import argparse
import base64
import csv
import json
import os
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time

from tasks import FIXTURES, TASKS

IS_WINDOWS = os.name == "nt"
TIMEOUT = 60


def shells():
    """Return the shells to test on this machine, as (name, family, argv-builder)."""
    found = []
    if IS_WINDOWS:
        for name, family in (("pwsh", "pwsh"), ("powershell", "pwsh51"), ("cmd", "cmd")):
            if shutil.which(name):
                found.append((name, family))
    else:
        for name in ("zsh", "bash"):
            if shutil.which(name):
                found.append((name, "posix"))
    return found


def run(argv, cwd=None, env=None, timeout=TIMEOUT):
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=timeout)
    dec = lambda b: b.decode("utf-8", errors="replace")
    return p.returncode, dec(p.stdout), dec(p.stderr)


def version_of(shell):
    try:
        if shell in ("zsh", "bash"):
            return run([shell, "--version"])[1].splitlines()[0].strip()
        if shell in ("pwsh", "powershell"):
            code = "$PSVersionTable.PSVersion.ToString(); $PSVersionTable.PSEdition"
            return " ".join(run([shell, "-NoProfile", "-Command", code])[1].split())
        if shell == "cmd":
            return run(["cmd", "/d", "/c", "ver"])[1].strip()
    except Exception as exc:  # noqa: BLE001
        return f"unknown ({exc})"
    return "unknown"


def machine_info():
    info = {"python": sys.version.split()[0], "platform": platform.platform(), "machine": platform.machine()}
    if sys.platform == "darwin":
        info["macos"] = run(["sw_vers", "-productVersion"])[1].strip()
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            info["os_release"] = dict(l.strip().split("=", 1) for l in f if "=" in l).get("PRETTY_NAME", "").strip('"')
    for tool in ("curl",):
        exe = shutil.which(tool, path=stock_path())
        if exe:
            info[tool] = run([exe, "--version"])[1].splitlines()[0].strip()
    return info


def make_practice(root):
    cwd = tempfile.mkdtemp(prefix="practice-", dir=root)
    for rel, content in FIXTURES.items():
        path = os.path.join(cwd, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
    os.chmod(os.path.join(cwd, "hello.sh"), 0o644)  # no execute bit: the task adds it
    return cwd


def build_argv(shell, family, text, scripts_dir):
    exe = shutil.which(shell)  # full path, resolved before the stock PATH applies
    if family == "posix":
        script = os.path.join(scripts_dir, "run.sh")
        with open(script, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
        return [exe, script]
    if family in ("pwsh", "pwsh51"):
        encoded = base64.b64encode(text.encode("utf-16-le")).decode("ascii")
        return [exe, "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded]
    script = os.path.join(scripts_dir, "run.cmd")
    with open(script, "w", encoding="ascii", newline="\r\n") as f:
        f.write("@echo off\n" + text + "\n")
    return [exe, "/d", "/c", script]


def kill_tree(proc):
    if proc.poll() is not None:
        return
    if IS_WINDOWS:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
    else:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass


def stock_path():
    """The PATH a fresh install of each OS gives you, so tools that CI images add
    (Git for Windows' Unix utilities, Homebrew) can't make a command look portable."""
    if IS_WINDOWS:
        sr = os.environ.get("SystemRoot", r"C:\Windows")
        dirs = [sr + r"\system32", sr, sr + r"\System32\Wbem", sr + r"\System32\WindowsPowerShell\v1.0",
                sr + r"\System32\OpenSSH"]
        pwsh = shutil.which("pwsh")
        if pwsh:
            dirs.append(os.path.dirname(pwsh))  # where the PowerShell 7 installer puts it
        dirs.append(os.path.join(os.environ.get("USERPROFILE", ""), r"AppData\Local\Microsoft\WindowsApps"))
        return ";".join(dirs)
    if sys.platform == "darwin":
        return "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"  # /etc/paths on a new Mac
    return "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"  # Ubuntu default


def run_task(task, shell, family, root, portability):
    cwd = make_practice(root)
    scripts_dir = tempfile.mkdtemp(prefix="scripts-", dir=root)
    env = dict(os.environ)
    env["PATH"] = stock_path()
    env.setdefault("TERM", "xterm-256color")  # what a terminal emulator would set
    if IS_WINDOWS:
        home = env.get("USERPROFILE", os.path.expanduser("~"))
    else:
        home = tempfile.mkdtemp(prefix="home-", dir=root)
        env["HOME"] = home

    if portability:
        text = task.get("posix")
    elif family == "pwsh51":
        text = task.get("pwsh51", task.get("pwsh"))
    else:
        text = task.get(family if family != "pwsh51" else "pwsh")
    result = {"task_id": task["id"], "task": task["task"], "shell": shell, "command": text}
    if text is None:
        result.update(status="interactive" if task.get("interactive") else "no built-in equivalent",
                      ok=None, note=task.get("interactive", ""))
        return result

    sleeper = None
    if task.get("sleeper"):
        sleeper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)"])
        text = text.replace("{pid}", str(sleeper.pid))
    text = text.replace("{rcfile}", ".zshrc" if shell == "zsh" else ".bashrc")
    result["command"] = text

    argv = build_argv(shell, "posix" if (portability and family == "posix") else family, text, scripts_dir)
    ctx = {"cwd": cwd, "home": home}
    started = time.time()
    try:
        if task.get("follow"):
            proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    start_new_session=not IS_WINDOWS)
            time.sleep(2)
            with open(os.path.join(cwd, "log.txt"), "a", encoding="utf-8") as f:
                f.write("line 11 appended\n")
            time.sleep(3)
            kill_tree(proc)
            out, err = proc.communicate(timeout=10)
            ctx.update(exit=proc.returncode, stdout=out.decode("utf-8", "replace"), stderr=err.decode("utf-8", "replace"))
        else:
            code, out, err = run(argv, cwd=cwd, env=env)
            ctx.update(exit=code, stdout=out, stderr=err)
    except subprocess.TimeoutExpired:
        ctx.update(exit=None, stdout="", stderr=f"timed out after {TIMEOUT}s")

    if task.get("persist") and ctx["exit"] == 0:
        if IS_WINDOWS:
            probe = "[Environment]::GetEnvironmentVariable('API_KEY','User')"
            ctx["persist_out"] = run(["powershell", "-NoProfile", "-Command", probe])[1]
            run(["powershell", "-NoProfile", "-Command",
                 "[Environment]::SetEnvironmentVariable('API_KEY',$null,'User')"])
        else:
            ctx["persist_out"] = run([shutil.which(shell), "-i", "-c", "echo $API_KEY"], env=env)[1]

    if sleeper is not None:
        for _ in range(30):
            if sleeper.poll() is not None:
                break
            time.sleep(0.1)
        ctx["sleeper_gone"] = sleeper.poll() is not None
        if sleeper.poll() is None:
            sleeper.kill()

    try:
        ok = bool(task["check"](ctx))
    except Exception:  # noqa: BLE001
        ok = False
    result.update(
        status="works" if ok else "failed",
        ok=ok,
        exit=ctx.get("exit"),
        seconds=round(time.time() - started, 2),
        stdout=ctx.get("stdout", "")[-2000:],
        stderr=ctx.get("stderr", "")[-1000:],
        persist_out=ctx.get("persist_out", ""),
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--portability", action="store_true")
    parser.add_argument("--label", default=platform.node() or "local")
    args = parser.parse_args()

    root = tempfile.mkdtemp(prefix="cli-cheat-sheet-")
    found = shells()
    report = {"label": args.label, "mode": "portability" if args.portability else "native",
              "machine": machine_info(), "shells": {s: version_of(s) for s, _ in found}, "results": []}
    for shell, family in found:
        for task in TASKS:
            r = run_task(task, shell, family, root, args.portability)
            report["results"].append(r)
            mark = {True: "ok ", False: "FAIL", None: "-- "}[r["ok"]]
            print(f"[{shell:10}] {mark} {task['id']:>2}. {task['task']}", flush=True)
    shutil.rmtree(root, ignore_errors=True)

    os.makedirs("results", exist_ok=True)
    stem = os.path.join("results", args.label + ("-portability" if args.portability else ""))
    with open(stem + ".json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    with open(stem + ".csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["task_id", "task", "shell", "status", "exit", "command"])
        for r in report["results"]:
            w.writerow([r["task_id"], r["task"], r["shell"], r["status"], r.get("exit"), r["command"]])
    print(json.dumps({"machine": report["machine"], "shells": report["shells"]}, indent=2))


if __name__ == "__main__":
    main()
