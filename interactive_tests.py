"""Check the interactive-only claims in a real pseudo-terminal (macOS/Linux).

1. A command typed with a leading space stays out of history only with the option on
   (zsh: setopt HIST_IGNORE_SPACE, bash: HISTCONTROL=ignorespace).
2. An alias defined in the rc file works when you type it, but not inside a script.

Each shell starts with a throwaway HOME, so your real history and rc files are untouched.
"""

import os
import pty
import select
import shutil
import subprocess
import tempfile
import time


def drive(argv, env, lines, wait=0.6):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvpe(argv[0], argv, env)
    out = b""

    def drain(t):
        nonlocal out
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if r:
                try:
                    out += os.read(fd, 4096)
                except OSError:
                    return

    drain(1.5)
    for line in lines:
        os.write(fd, line.encode() + b"\r")
        drain(wait)
    drain(1)
    try:
        os.waitpid(pid, 0)
    except ChildProcessError:
        pass
    return out.decode("utf-8", "replace")


def history_test(shell, ignore=True):
    home = tempfile.mkdtemp(prefix="home-")
    env = {"HOME": home, "PATH": "/usr/bin:/bin", "TERM": "xterm-256color"}
    if shell == "zsh":
        rc, hist = ".zshrc", ".zsh_history"
        setup = f"HISTFILE=~/{hist}\nSAVEHIST=100\nHISTSIZE=100\n" + ("setopt HIST_IGNORE_SPACE\n" if ignore else "")
    else:
        rc, hist = ".bashrc", ".bash_history"
        setup = f"HISTFILE=~/{hist}\n" + ("HISTCONTROL=ignorespace\n" if ignore else "")
    with open(os.path.join(home, rc), "w") as f:
        f.write(setup)
    argv = [shutil.which(shell), "-i"] if shell == "zsh" else [shutil.which(shell), "--rcfile", os.path.join(home, rc), "-i"]
    drive(argv, env, ["echo visible-command", " export API_KEY=secret-test-value", "exit"])
    with open(os.path.join(home, hist), encoding="utf-8", errors="replace") as f:
        saved = f.read()
    shutil.rmtree(home, ignore_errors=True)
    return {"shell": shell, "ignore_option": ignore, "rc": setup.strip(), "history_file": saved.strip(),
            "visible_saved": "visible-command" in saved, "spaced_saved": "secret-test-value" in saved}


def alias_test(shell):
    home = tempfile.mkdtemp(prefix="home-")
    cwd = tempfile.mkdtemp(prefix="practice-")
    open(os.path.join(cwd, "notes.txt"), "w").write("hello\n")
    env = {"HOME": home, "PATH": "/usr/bin:/bin", "TERM": "xterm-256color"}
    rc = ".zshrc" if shell == "zsh" else ".bashrc"
    with open(os.path.join(home, rc), "w") as f:
        f.write("alias ll='ls -la'\n")
    with open(os.path.join(cwd, "uses-alias.sh"), "w") as f:
        f.write("ll notes.txt\n")
    script = subprocess.run([shutil.which(shell), "uses-alias.sh"], cwd=cwd, env=env, capture_output=True, text=True)
    shutil.rmtree(home, ignore_errors=True)
    shutil.rmtree(cwd, ignore_errors=True)
    return {"shell": shell, "script_exit": script.returncode, "script_output": (script.stdout + script.stderr).strip()}


if __name__ == "__main__":
    import json
    results = {"history": [history_test(s, i) for s in ("zsh", "bash") if shutil.which(s) for i in (False, True)],
               "alias_in_script": [alias_test(s) for s in ("zsh", "bash") if shutil.which(s)]}
    print(json.dumps(results, indent=2))
