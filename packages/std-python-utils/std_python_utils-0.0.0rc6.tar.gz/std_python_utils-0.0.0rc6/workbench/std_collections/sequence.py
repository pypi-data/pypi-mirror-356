import subprocess

linux_seq_cmd = 'seq'


def linux_seq(size: int) -> tuple[int]:
    subproc_cmd = ('seq', str(size))
    completed_cmd = subprocess.run(subproc_cmd, capture_output=True, check=True)
    if completed_cmd.returncode != 0:
        raise

    return tuple(map(int, completed_cmd.stdout.split()))
