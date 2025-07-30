# shellrosetta/cli.py

import sys
from .core import lnx2ps, ps2lnx

def print_header():
    print("=" * 65)
    print("ShellRosetta: Linux ↔ PowerShell CLI Command Translator")
    print("Author: David Donohue")
    print("Repo: github.com/sdirishguy/shellrosetta")
    print("=" * 65)

def show_help():
    print_header()
    print("Usage:")
    print("  shellrosetta lnx2ps \"linux command here\"")
    print("  shellrosetta ps2lnx \"powershell command here\"")
    print("  shellrosetta          # Interactive shell mode")
    print("")
    print("Examples:")
    print("  shellrosetta lnx2ps \"ls -alh | grep foo\"")
    print("  shellrosetta ps2lnx \"Get-ChildItem -Force | Select-String foo\"")
    print("=" * 65)

def run_interactive():
    print_header()
    print("Welcome to ShellRosetta Interactive Mode!")
    print("Type 'exit' to quit, or 'mode' to switch translation direction.")
    mode = ""
    # Ask user for translation direction
    while mode not in ("lnx2ps", "ps2lnx"):
        mode = input("Mode [lnx2ps/ps2lnx] (or 'exit'): ").strip().lower()
        if mode == "exit":
            print("Goodbye!")
            return
    print(f"Type your {mode.upper()} commands below. Type 'mode' to switch, 'exit' to quit.\n")
    while True:
        try:
            inp = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if inp.lower() == "exit":
            print("Goodbye!")
            break
        if inp.lower() == "mode":
            # Allow switching translation direction anytime
            while True:
                mode = input("Mode [lnx2ps/ps2lnx] (or 'exit'): ").strip().lower()
                if mode == "exit":
                    print("Goodbye!")
                    return
                if mode in ("lnx2ps", "ps2lnx"):
                    print(f"Switched to {mode.upper()} mode.\n")
                    break
            continue
        if not inp:
            continue
        print("\n--- Translation ---")
        if mode == "lnx2ps":
            print("PowerShell Equivalent:")
            print("  " + lnx2ps(inp))
        else:
            print("Linux Equivalent:")
            print("  " + ps2lnx(inp))
        print("-------------------\n")

def main():
    # If no args, drop into interactive mode
    if len(sys.argv) == 1:
        run_interactive()
        return
    if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
        show_help()
        sys.exit(0)
    mode = sys.argv[1].lower()
    if mode not in ['lnx2ps', 'ps2lnx']:
        print("Unknown mode:", mode)
        show_help()
        sys.exit(1)
    command = sys.argv[2]
    print_header()
    print(f"Original command: {command}\n")
    if mode == "lnx2ps":
        print("PowerShell Equivalent:")
        print("  " + lnx2ps(command) + "\n")
    else:
        print("Linux Equivalent:")
        print("  " + ps2lnx(command) + "\n")

# Allow both python -m and entry point execution
if __name__ == "__main__" or __name__ == "shellrosetta.cli":
    main()
