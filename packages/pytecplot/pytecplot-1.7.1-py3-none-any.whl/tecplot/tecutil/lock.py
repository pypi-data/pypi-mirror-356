import contextlib
import functools
import sys

from .tecutil_connector import _tecutil_connector, _tecutil


@contextlib.contextmanager
def lock(with_recording=True):
    """
    ParentLockStart takes a boolean: ShutdownImplicitRecording
    ShutdownImplicitRecording = True -> No recording
    ShutdownImplicitRecording = False -> With Recording
    """
    lock.FORCE_RECORDING = getattr(lock, 'FORCE_RECORDING', False)
    if _tecutil_connector.connected:
        yield
    else:
        _tecutil.ParentLockStart(not (with_recording or lock.FORCE_RECORDING))
        try:
            yield
        finally:
            _tecutil.handle.tecUtilParentLockFinish()


@contextlib.contextmanager
def force_recording():
    """Do not disable implicit recording when locking the engine."""
    if lock.FORCE_RECORDING:
        yield
    else:
        try:
            lock.FORCE_RECORDING = True
            yield
        finally:
            lock.FORCE_RECORDING = False
