import subprocess


def runcmd(cmd):
    print("here", cmd)
    return subprocess.run(cmd.split(' '), stdout=subprocess.PIPE).stdout.decode('utf8').strip()
