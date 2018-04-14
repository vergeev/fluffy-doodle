from debugger import debugger

debugger = debugger()
pid = int(input('Enter the PID to attach to: '))
debugger.attach(pid)
debugger.detach()
