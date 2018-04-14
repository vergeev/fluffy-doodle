from ctypes import *
from debugger_defines import *


kernel32 = windll.kernel32


class debugger:

    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False

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
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print('[*] Error 0x{}'.format(kernel32.GetLastError()))

    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = pid
            self.run()
        else:
            print('[*] Unable to attach to the process')

    def run(self):
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            input('Press any key to continue...')
            self.debugger_active = False
            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId,
                debug_event.dwThreadId,
                continue_status
            )
    
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print('[*] Finished debugging. Exiting...')
            return True
        else:
            print('[*] There was an error')
            return False

