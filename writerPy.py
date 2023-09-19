import time
import sys
import win32pipe, win32file, pywintypes


def pipe_server():
    print("pipe server")
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\Foo',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("got client")
        some_data = str.encode("Hello from Python!")
        win32file.WriteFile(pipe, some_data)

        print("finished now")
    finally:
        win32file.CloseHandle(pipe)


def pipe_client():
    print("pipe client")
    quit = False

    while not quit:
        # print("before")
        # In the second line -  | win32file.GENERIC_WRITE
        # In the third line - | win32file.FILE_SHARE_DELETE | win32file.FILE_SHARE_WRITE
        # in the third line
        try:
            handle = win32file.CreateFile(
                r'\\.\pipe\mypipe',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            print(handle)
            print("after handle intialization")
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            print("here 1")
            while True:
                resp = win32file.ReadFile(handle, 64*1024)
                print(f"message: {resp}")
        except pywintypes.error as e:
            print("error was thrown")
            print(e.args)
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("broken pipe, bye bye")
                quit = True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need s or c as argument")
    elif sys.argv[1] == "s":
        pipe_server()
    elif sys.argv[1] == "c":
        pipe_client()
    else:
        print(f"no can do: {sys.argv[1]}")

