import subprocess
import os
import sys

def run_where(target) -> list:
    proc = subprocess.Popen(['where', target], stdout=subprocess.PIPE)
    targets = []

    while True:
        line = proc.stdout.readline().rstrip()
        if not line:
            break
        targets.append(line.decode())

    return targets

def open_target(target):
    targets = run_where(target)

    if not targets:
        print(f'There are no targets for {target}')
        exit(1)

    index = 1
    for target in targets:
        print(f'[{index}] {target}')
        index += 1

    path = targets[0]
    os.system(f'explorer /select,"{path}"')

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) == 1 or (len(argv) == 2 and argv[1] == '.'):
        os.system('explorer .')
        return

    if len(argv) != 2:
        print('No target to show')
        exit(2)

    open_target(argv[1])

if __name__ == "__main__":
    sys.exit(main(sys.argv))