import os, zlib, hashlib, json

GITDIR = ".sahajgit"

def hash_data(data): return hashlib.sha1(data).hexdigest()
def repo_path(): return os.path.join(os.getcwd(), GITDIR)
def object_path(h): return os.path.join(repo_path(), "objects", h[:2], h[2:])

def write_object(obj_type, data):
    header = f"{obj_type} {len(data)}".encode() + b"\0"
    store = zlib.compress(header + data)
    h = hash_data(header + data)
    path = object_path(h)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(store)
    return h

def read_object(h):
    raw = zlib.decompress(open(object_path(h), "rb").read())
    nul = raw.index(b"\0")
    obj_type = raw[:nul].decode().split()[0]
    return obj_type, raw[nul+1:]

def init():
    for d in ["objects", "refs/heads", "refs/tags"]:
        os.makedirs(os.path.join(repo_path(), d), exist_ok=True)
    open(os.path.join(repo_path(), "HEAD"), "w").write("ref: refs/heads/main\n")

def current_branch():
    head = open(os.path.join(repo_path(), "HEAD")).read().strip()
    return head[5:].split("/")[-1] if head.startswith("ref: ") else head

def update_ref(branch, h):
    path = os.path.join(repo_path(), "refs", "heads", branch)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(h + "\n")

def read_ref(branch):
    path = os.path.join(repo_path(), "refs", "heads", branch)
    return open(path).read().strip() if os.path.exists(path) else None

def index_path(): return os.path.join(repo_path(), "index")
def load_index(): return json.load(open(index_path())) if os.path.exists(index_path()) else {}
def save_index(idx): json.dump(idx, open(index_path(), "w"), indent=2)
