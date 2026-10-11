# CLI cheat sheet tests

The test harness behind ScrapingBee's command line interface guide. It runs 31 everyday
command line tasks in **zsh, bash, PowerShell 7.6, Windows PowerShell 5.1, and Command Prompt**
on macOS, Ubuntu 26.04 LTS, and Windows 11, and checks that each command did what it claims.

## How it works

- `tasks.py` lists each task with its bash/zsh, PowerShell, and Command Prompt command and a
  check (file created, output contains the right lines, process gone).
- `harness.py` runs every command in the real shell, inside a fresh practice folder of
  throwaway files. On macOS and Linux it points `HOME` at a temporary folder, so nothing
  touches your real home folder or shell config.
- PowerShell commands run through `-EncodedCommand` without an execution policy override, so
  the policy behaves as it would for you. Command Prompt commands run from a `.cmd` file.
- `--portability` mode types the **bash/zsh command verbatim** into every shell, to see which
  commands work unchanged everywhere.

## Run it yourself

```bash
python3 harness.py --label my-machine
python3 harness.py --portability --label my-machine
```

Results land in `results/<label>.json` and `.csv`.

The GitHub Actions workflow (`.github/workflows/cheat-sheet.yml`) runs the same harness on
`windows-11-arm` (Windows 11), `windows-2025`, `macos-latest`, and an `ubuntu:26.04` container,
installing PowerShell 7.6.6 on the Windows runners first.
