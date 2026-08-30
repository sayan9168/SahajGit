import os, sys, json, time, getpass
from . import core

def cmd_init(a):
    core.init(); print("Initialized empty SahajGit repository")

def _add_file(p, idx):
    data = open(p, "rb").read()
    idx[os.path.normpath(p)] = core.write_object("blob", data)

def cmd_add(a):
    idx = core.load_index()
    for p in (a or ["."]):
        if os.path.isfile(p): _add_file(p, idx)
        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                if core.GITDIR in root: continue
                for f in files: _add_file(os.path.join(root, f), idx)
    core.save_index(idx); print("Staged changes")

def cmd_commit(a):
    msg = a[a.index("-m")+1] if "-m" in a else ""
    idx = core.load_index()
    tree = core.write_object("tree", json.dumps(idx, sort_keys=True).encode())
    branch = core.current_branch(); parent = core.read_ref(branch)
    commit = {"tree": tree, "parent": parent, "author": getpass.getuser(), "time": int(time.time()), "message": msg}
    h = core.write_object("commit", json.dumps(commit).encode())
    core.update_ref(branch, h)
    print(f"[{branch} {h[:7]}] {msg}")

def cmd_log(a):
    h = core.read_ref(core.current_branch())
    while h:
        _, data = core.read_object(h); c = json.loads(data)
        print(f"commit {h}\nAuthor: {c['author']}  {time.ctime(c['time'])}\n    {c['message']}\n")
        h = c.get("parent")

def cmd_status(a):
    idx = core.load_index(); print("On branch", core.current_branch())
    mod, unt = [], []
    for root, _, files in os.walk("."):
        if core.GITDIR in root: continue
        for f in files:
            p = os.path.normpath(os.path.join(root, f))
            data = open(p, "rb").read()
            h = core.hash_data(b"blob %d\0" % len(data) + data)
            if p not in idx: unt.append(p)
            elif idx[p] != h: mod.append(p)
    if mod: print("Changes not staged:", *mod, sep="\n  ")
    if unt: print("Untracked:", *unt, sep="\n  ")
    if not mod and not unt: print("working tree clean")

def cmd_branch(a):
    if a: core.update_ref(a[0], core.read_ref(core.current_branch())); print("Created branch", a[0])
    else: print("*", core.current_branch())

def cmd_checkout(a):
    if a:
        open(os.path.join(core.repo_path(), "HEAD"), "w").write(f"ref: refs/heads/{a[0]}\n")
        print("Switched to branch", a[0])

def main():
    if len(sys.argv) < 2:
        print("Usage: sahajgit <init|add|commit|log|status|branch|checkout> [args]"); return
    cmds = {"init": cmd_init, "add": cmd_add, "commit": cmd_commit, "log": cmd_log,
            "status": cmd_status, "branch": cmd_branch, "checkout": cmd_checkout}
    cmds.get(sys.argv[1], lambda x: print("Unknown command"))(sys.argv[2:])
