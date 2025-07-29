import ctypes
import os
import time
from ctypes import c_int, c_void_p, POINTER, byref


# Futex constants
FUTEX_WAIT = 0
FUTEX_WAKE = 1
ctypes.c_int

class FutexLock:

    def __init__(self):
        # Create a mutex with an initial value of 0 (unlocked)
        self._lock = ctypes.c_int(0)

    def _futex_wait(self, addr, val):
        """ Wait on the futex at addr until its value changes from val. """
        libc = ctypes.CDLL("libc.so.6")
        libc.futex.argtypes = [POINTER(c_int), c_int, c_int, c_void_p, c_void_p, c_int]
        libc.futex.restype = c_int
        return libc.futex(byref(self._lock), FUTEX_WAIT, val, None, None, 0)

    def _futex_wake(self, addr):
        """ Wake one thread waiting on the futex at addr. """
        libc = ctypes.CDLL("libc.so.6")
        libc.futex.argtypes = [POINTER(c_int), c_int, c_int, c_void_p, c_void_p, c_int]
        libc.futex.restype = c_int
        return libc.futex(byref(self._lock), FUTEX_WAKE, 1, None, None, 0)

    def acquire(self):
        """ Acquire the lock, blocking until it is available. """
        while True:
            if self._lock.value == 0:  # Check if the lock is free
                if ctypes.atomic_compare_exchange(self._lock, 0, 1):  # Try to set the lock
                    return  # Lock acquired
            # If lock is already acquired, wait
            self._futex_wait(byref(self._lock), 1)

    def release(self):
        """ Release the lock. """
        if self._lock.value == 1:  # Only release if it was held
            self._lock.value = 0  # Unlock
            self._futex_wake(byref(self._lock))  # Wake a waiting thread