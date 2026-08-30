import subprocess, os, tempfile
def test_flow():
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        subprocess.run(["python3", "-m", "sahajgit", "init"])
        open("a.txt", "w").write("hi")
        subprocess.run(["python3", "-m", "sahajgit", "add", "a.txt"])
        r = subprocess.run(["python3", "-m", "sahajgit", "commit", "-m", "first"], capture_output=True, text=True)
        assert "first" in r.stdout
