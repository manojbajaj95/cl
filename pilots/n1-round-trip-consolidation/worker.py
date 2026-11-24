import array
import bisect
import collections
import ctypes
import fractions
import functools
import heapq
import itertools
import json
import math
import operator
import re
import resource
import statistics
import string
import sys


def restrict():
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    resource.setrlimit(resource.RLIMIT_AS, (256 << 20, 256 << 20))
    lib = ctypes.CDLL("libseccomp.so.2", use_errno=True)
    lib.seccomp_init.restype = ctypes.c_void_p
    lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    lib.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    lib.seccomp_load.argtypes = [ctypes.c_void_p]
    ctx = lib.seccomp_init(0x00050000 | 1)
    if not ctx:
        raise RuntimeError("seccomp_init failed")
    for name in ("write", "exit_group", "brk", "mmap", "mprotect", "munmap", "mremap",
                 "rt_sigaction", "rt_sigprocmask", "rt_sigreturn", "futex", "clock_gettime"):
        syscall = lib.seccomp_syscall_resolve_name(name.encode())
        if syscall < 0 or lib.seccomp_rule_add(ctx, 0x7FFF0000, syscall, 0):
            raise RuntimeError(f"seccomp_rule_add failed: {name}")
    if lib.seccomp_load(ctx):
        raise RuntimeError("seccomp_load failed")


def main():
    job = json.load(sys.stdin)
    restrict()
    sys.stderr.write("restricted\n")
    sys.stderr.flush()
    namespace = {"__name__": "__candidate__"}
    exec(job["code"], namespace)
    if "tests" in job:
        for test in job["tests"]:
            exec(test, namespace)
        result = True
    else:
        f = namespace["transform"]
        result = []
        for x in job["inputs"]:
            try:
                y = f(x)
                result.append([True, json.loads(json.dumps(y, allow_nan=False))])
            except Exception:
                result.append([False, None])
    print(json.dumps(result))


if __name__ == "__main__":
    main()
