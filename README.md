# SahajGit

> **Meta-project:** This version control system is implemented in SahajCore,
> a programming language I also built from scratch.


A Git clone **written in SahajCore** (a custom programming language).

This is a meta-project: a version control system implemented in a language I also built from scratch.

## Features

- Content-addressable object store (SHA1 hashing)
- Commits with parent tracking
- Branch support
- File staging and status

## Commands

```bash
python3 sahajgit.py init          # Initialize repository
python3 sahajgit.py add <file>    # Stage file
python3 sahajgit.py commit -m "msg"  # Create commit
python3 sahajgit.py log           # Show history
python3 sahajgit.py status        # Show status
```

## Architecture

All Git logic is written in **SahajCore** (.sahaj files in `sahajgit-core/`):
- `init.sahaj` - Repository initialization
- `add.sahaj` - File staging
- `commit.sahaj` - Commit creation
- `log.sahaj` - History display
- `status.sahaj` - Working tree status

A minimal Python runner (`sahajgit.py`) executes the SahajCore scripts.

## Why?

This project demonstrates:
1. A working version control system
2. Real-world use of SahajCore language
3. Understanding of Git internals

Built entirely on an Android phone using Termux.
