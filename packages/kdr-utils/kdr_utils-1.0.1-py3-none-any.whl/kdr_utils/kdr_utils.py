import time
from enum import Enum, auto
from typing import NamedTuple, Generic, TypeVar
from functools import total_ordering

import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

UNCHANGED = object()  # sentinel value for wait_for()

class Error(Enum):
    NOT_FOUND = auto()
    FAILED = auto()
    TIMEOUT = auto()
    UNKNOWN = auto()

T = TypeVar("T")
class Result(NamedTuple, Generic[T]):
    ok: T | None
    err: Error | None

@total_ordering
class DebugLevel(Enum):
    SILENT = 0
    QUIET = 1
    CHATTY = 2

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class WaitedFor(NamedTuple):
    line: str | None
    lines: list[str]

def get_serial_port(device_name: str) -> Result[ListPortInfo]:
    """
    Get COM port by device name (or just port name).
    """
    port_info = next(
        (port for port in list_ports.comports() if device_name in port.device or device_name in port.description),
        None
    )
    if port_info:
        return Result(port_info, None)
    return Result(None, Error.NOT_FOUND)


def open_serial_port(port_name: str, baud_rate: int) -> Result[serial.Serial]:
    """
    Open COM port, return error for SerialException, or raise anything else (is there anything else?)
    """
    try:
        ser = serial.Serial(port_name, baud_rate)
    except serial.serialutil.SerialException:
        return Result(None, Error.FAILED)
    except Exception:
        raise

    return Result(ser, None)

def serial_read_line(ser: serial.Serial) -> str | None:
    """
    Read a line and kind of sanitize it
    """
    line = ser.readline()
    if not line:
        return None
    
    return (
        line.decode(errors='replace')
        .replace('\r\n', '')
        .replace('\x1b[2J\x1b[H', '')  # Remove console clear esc sequence
    )
    
def wait_for(
        ser: serial.Serial, 
        string: str | list[str], 
        *,
        reset_input_buffer: bool = True,
        timeout_serial: float | int | None | object = UNCHANGED,  # object = UNCHANGED sentinel. No rust options :(
        timeout_wait_for: float | int | None = None,
        debug_level: DebugLevel = DebugLevel.SILENT
    ) -> Result[WaitedFor]:
    """
    Read lines from the input buffer until one of them contains a target string.

    Reset the buffer to avoid catching lines since the last serial_wait_for() call.
    Set ser.timeout or serial_timeout (temporary) to 0.2ish to enable KeyboardInterrupt and wait_for_timeout.
    Missing the 'on' argument to deal with stupid E3 prompts that can appear while waiting, eg. after sw ether. (Requires writable serial port).
    """

    def _timed_out():
        return timeout_wait_for is not None and (time.time() - start_time) > timeout_wait_for
    
    def _matches_any(line):
        return any(target in line for target in targets)
    
    if reset_input_buffer:
        ser.reset_input_buffer()

    if debug_level >= DebugLevel.QUIET:
        print(f"Wait for line containing '{string}'")

    targets = [string] if isinstance(string, str) else string  # Support str or [str]

    serial_timeout_orig = ser.timeout
    if timeout_serial is not UNCHANGED:
        ser.timeout = timeout_serial

    start_time = time.time()
    lines = []

    try:
        while True:
            if _timed_out():
                if debug_level >= DebugLevel.QUIET:
                    print(f"Timeout waiting for {targets}")
                return Result(WaitedFor(None, lines), Error.TIMEOUT)
            
            line = serial_read_line(ser)
            
            if not line:
                continue
            
            lines.append(line)

            if debug_level >= DebugLevel.CHATTY: 
                print(f"[ {line} ]")

            # TODO: Implement 'on' here

            if _matches_any(line):
                if debug_level >= DebugLevel.QUIET: 
                    print('Found line\n')
                return Result(WaitedFor(line, lines), None)

    finally:
        ser.timeout = serial_timeout_orig
