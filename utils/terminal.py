import subprocess


def runcmd(cmd):
    return subprocess.run(cmd.split(' '), stdout=subprocess.PIPE).stdout.decode('utf8').strip()
