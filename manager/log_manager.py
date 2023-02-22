import os
import sys


def hide_logs(fd=2):
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_std = os.dup(fd)
    sys.stderr.flush()
    os.dup2(devnull, fd)
    os.close(devnull)
    return old_std


def show_logs(old_std, fd=2):
    os.dup2(old_std, fd)
    os.close(old_std)
