import subprocess
import re
import shlex
import subprocess

if __name__ == '__main__':
    shell_cmd = 'ping 192.168.194.2'
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            s1 = str(line, encoding='gbk')
            print(s1)
    if p.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')