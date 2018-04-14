from ctypes import *
from debugger_defines import *


kernel32 = windll.kernel32


class debugger:

    def load(self, exe_path):
        creation_flags = DEBUG_PROCESS
        process_information = PROCESS_INFORMATION()
        startupinfo = STARTUPINFO()
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(
            exe_path,
            None,
            None,
            None,
            None,
            creation_flags,
            None,
            None,
            byref(startupinfo),
            byref(process_information)
        ):
            print('[*] We have successfully launched the process!')
            print('[*] PID: {}'.format(process_information.dwProcessId))
        else:
            print('[*] Error 0x{}'.format(kernel32.GetLastError()))
