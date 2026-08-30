import sys, os, time, json as _json
sys.path.insert(0, os.path.expanduser("~/sahajcore"))
from lexer import tokenize
from parser import Parser
import interpreter as _interp
from interpreter import Interp, BFunc

# Add missing string methods to the interpreter
_interp.SM['slice'] = lambda s, a, b=None: s[a:b] if b is not None else s[a:]
_interp.SM['startsWith'] = lambda s, p: s.startswith(p)
_interp.SM['strip'] = lambda s: s.strip()
_interp.SM['indexOf'] = lambda s, sub: s.find(sub)

def run(command, args):
    script = f"sahajgit-core/{command}.sahaj"
    if not os.path.exists(script):
        print(f"sahajgit: '{command}' is not a sahajgit command"); return
    interp = Interp()
    interp.g.set('sys', {
        'args': args,
        'user': BFunc('user', lambda: os.environ.get('USER', 'unknown')),
        'time': BFunc('time', lambda: int(time.time())),
    })
    interp.g.set('ord', BFunc('ord', ord))
    interp.g.set('fs', {
        'read': BFunc('read', lambda p: open(p).read()),
        'write': BFunc('write', lambda p, c: open(p, 'w').write(c) or None),
        'exists': BFunc('exists', os.path.exists),
        'mkdir': BFunc('mkdir', lambda p: os.makedirs(p, exist_ok=True) or None),
        'listdir': BFunc('listdir', os.listdir),
    })
    interp.g.set('json', {'parse': BFunc('parse', _json.loads), 'stringify': BFunc('stringify', _json.dumps)})
    interp.g.set('datetime', {'from_timestamp': BFunc('from_timestamp', lambda t: time.ctime(t))})
    try:
        ast = Parser(tokenize(open(script).read())).parse()
        interp.run(ast)
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: sahajgit <init|add|commit|log|status> [args]"); return
    run(sys.argv[1], sys.argv[2:])

if __name__ == '__main__':
    main()
