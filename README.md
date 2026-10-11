# CLI cheat sheet tests

The test harness behind ScrapingBee's guide to using a command line interface on Mac, Windows
and Linux. It runs 31 everyday command line tasks in **zsh, bash, PowerShell 7.6, Windows
PowerShell 5.1 and Command Prompt**, checks that each command did what it claims, and runs every
code example from the article verbatim in each shell.

## Results (October 11, 2026)

| System | Shells | Native commands | bash commands typed verbatim |
| ----- | ----- | ----- | ----- |
| macOS 26.6.2, Apple silicon (GitHub `macos-latest` and a local Mac) | zsh 5.9, bash 3.2.57 | 29 of 30 (BSD `ls` has no `--help`; `man ls` works) | n/a |
| Ubuntu 26.04.1 LTS (`ubuntu:26.04` container) | bash 5.3.9, coreutils from uutils 0.10.0 | 30 of 30 | n/a |
| Windows 11 build 26200, Arm64 (`windows-11-arm`) | PowerShell 7.6.6 | 30 of 30 | 15 of 30 |
| | Windows PowerShell 5.1.26100 | 30 of 30 | 13 of 30 |
| | Command Prompt | 28 of 30 (no built-in head/tail or follow) | 3 of 30 |
| Windows Server 2025 build 26100, x64 (`windows-2025`) | same three shells | same as Windows 11 | same as Windows 11 |

**Only 1 of 30 bash commands (`cd docs`) worked unchanged in all five shells.** Task 27 (search history) needs a
person at the keyboard, so it's documented rather than automated, which is why the counts are
out of 30, not 31.

Raw results, including every command's output, are in `results/`.

## How it works

- `tasks.py` lists each task with its bash/zsh, PowerShell and Command Prompt command and a
  check (file created, output contains the right lines, process gone).
- `harness.py` runs every command in the real shell, inside a fresh practice folder of
  throwaway files. On macOS and Linux it points `HOME` at a temporary folder, so nothing
  touches your real home folder or shell config.
- Each shell runs with its operating system's **stock PATH**, so tools a build machine adds
  (Git for Windows' Unix utilities, Homebrew) can't make a command look portable.
- PowerShell commands run through `-EncodedCommand` without an execution policy override, so
  the policy behaves as it would for you. Command Prompt commands run from a `.cmd` file.
- `--portability` mode types the **bash/zsh command verbatim** into every shell, to see which
  commands work unchanged everywhere. Tasks whose effect is invisible (such as `cd`) are followed
  by a shell-native probe (`pwd`, `Get-Location`, `cd`), so only the command itself is tested.
- `make_demos.py` writes each article example to `demos/<name>/` as standalone files, and
  `demos.py` runs them verbatim, merging output and errors the way a terminal shows them.
- `interactive_tests.py` checks the claims that need a real terminal (leading-space history,
  aliases in scripts) inside a pseudo-terminal, and `scheduling/cron-test.sh` proves a cron
  entry fires.

## Run it yourself

```bash
python3 harness.py --label my-machine
python3 harness.py --portability --label my-machine
python3 demos.py --label my-machine
```

Results land in `results/`.

The GitHub Actions workflow (`.github/workflows/cheat-sheet.yml`) runs everything on
`windows-11-arm` (Windows 11), `windows-2025`, `macos-latest` and an `ubuntu:26.04` container,
installing PowerShell 7.6.6 on the Windows runners first. GitHub's runners set the execution
policy to Unrestricted, so the execution policy example forces Restricted, the Windows 11
client default for Windows PowerShell 5.1.
