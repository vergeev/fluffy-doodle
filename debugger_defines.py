from ctypes import *

# Map the Microsoft types to ctypes for clarity
# https://msdn.microsoft.com/en-us/library/windows/desktop/aa383751(v=vs.85).aspx
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)
HANDLE = c_void_p
PVOID = c_void_p
ULONG_PTR = POINTER(c_ulong)


DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010
PROCESS_ALL_ACCESS = 0x001F0FFF  # a sum of all the rights: https://msdn.microsoft.com/en-us/library/windows/desktop/ms684880(v=vs.85).aspx
INFINITE = 0xFFFFFFFF  # intended for WaitForDebugEvent

# Constants from https://msdn.microsoft.com/en-us/library/windows/desktop/ms679285(v=vs.85).aspx
DBG_CONTINUE = 0x00010002


class STARTUPINFO(Structure):
    _fields_ = [
        ('cb',          DWORD),
        ('lpReserved',  LPTSTR),
        ('lpDesktop',   LPTSTR),
        ('lpTitle',     DWORD),
        ('dwX',         DWORD),
        ('dwY',         DWORD),
        ('dwXSize',     DWORD),
        ('dwYSize',     DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags',     DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', LPBYTE),
        ('hStdInput',   HANDLE),
        ('hStdOutput',  HANDLE),
        ('hStdError',   HANDLE),
    ]


class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ('hProcess',    HANDLE),
        ('hThread',     HANDLE),
        ('dwProcessId', DWORD),
        ('dwThreadId',  DWORD),
    ]


class EXCEPTION_RECORD(Structure):
    # https://msdn.microsoft.com/en-us/library/aa363082(v=vs.85).aspx
    EXCEPTION_MAXIMUM_PARAMETERS = 15  # according to the docs, 3 is enough, but just to be safe
    pass


# doing this in order to make recursive pointer
EXCEPTION_RECORD._fields_ = [
    ('ExceptionCode',   DWORD),
    ('ExceptionFlags',  DWORD),
    ('ExceptionRecord', POINTER(EXCEPTION_RECORD)),
    ('ExceptionAddress', PVOID),
    ('NumberParameters', DWORD),
    ('ExceptionInformation', ULONG_PTR * EXCEPTION_RECORD.EXCEPTION_MAXIMUM_PARAMETERS),
]


class EXCEPTION_DEBUG_INFO(Structure):
    # https://msdn.microsoft.com/en-us/library/ms679326(v=vs.85).aspx
    _fields_ = [
        ('dwFirstChance', DWORD),
        ('ExceptionRecord', EXCEPTION_RECORD),
        ('dwFirstChance', DWORD),
    ]


class DEBUG_EVENT_UNION(Union):
    _fields_ = [
        ('Exception', EXCEPTION_DEBUG_INFO),
        # there are other attributes to implement: https://msdn.microsoft.com/en-us/library/ms679308.aspx
    ]


class DEBUG_EVENT(Structure):
    # https://msdn.microsoft.com/en-us/library/ms679308.aspx
    _fields_ = [
        ('dwDebugEventCode', DWORD),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
        ('u', DEBUG_EVENT_UNION),
    ]
