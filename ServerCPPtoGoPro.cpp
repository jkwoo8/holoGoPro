/*
Server Program for Win32 Named Pipes Example.
Copyright (C) 2012 Peter R. Bloomfield.

For an exaplanation of the code, see the associated blog post:
http://avidinsight.uk/2012/03/introduction-to-win32-named-pipes-cpp/

This code is made freely available under the MIT open source license
(see accompanying LICENSE file for details).
It is intended only for educational purposes. and is provide as-is with no
guarantee about its reliability, correctness, or suitability for any purpose.


INSTRUCTIONS:

Run this server program first.
Before closing it, run the accompanying client program.
*/

#include <iostream>
#include <windows.h>
using namespace std;

int main(int argc, const char** argv)
{
    wcout << "Creating an instance of a named pipe..." << endl;

    // Create a pipe to send data
    HANDLE pipe = CreateNamedPipe(
        L"\\\\.\\pipe\\mypipe", // name of the pipe
        PIPE_ACCESS_DUPLEX, // 1-way pipe -- send only
        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT, // send data as a byte stream
        PIPE_UNLIMITED_INSTANCES, // only allow 1 instance of this pipe
        1024, // no outbound buffer
        1024, // no inbound buffer
        0, // use default wait time
        NULL // use default security attributes
    );

    if (pipe == NULL || pipe == INVALID_HANDLE_VALUE) {
        wcout << "Failed to create outbound pipe instance.";
        // look up error code here using GetLastError()
        system("pause");
        return 1;
    }

    wcout << "Server: Waiting for a client to connect to the pipe..." << endl;

    // This call blocks until a client process connects to the pipe
    BOOL result = ConnectNamedPipe(pipe, NULL);
    if (!result) {
        wcout << "Failed to make connection on named pipe." << endl;
        // look up error code here using GetLastError()
        CloseHandle(pipe); // close the pipe
        system("pause");
        return 1;
    }

    wcout << "Sending data to pipe..." << endl;

    // This call blocks until a client process reads all the data
    // const char* data[7] = {"new", "start", "pause", "start", "pause", "stop", "download"};
    const wchar_t* data[7] = {L"new", L"start", L"pause", L"start", L"pause", L"stop", L"download" };
    for (int i = 0; i < 7; i++) {
        DWORD numBytesWritten = 0;
        result = WriteFile(
            pipe, // handle to our outbound pipe
            data[i], // data to send
            wcslen(data[i]) * sizeof(wchar_t), // length of data to send (bytes) ----- strlen(data) * sizeof(char)
            &numBytesWritten, // will store actual amount of data sent
            NULL // not using overlapped IO
        );

        if (result) {
            wcout << "Number of bytes sent: " << numBytesWritten << endl;
        }
        else {
            wcout << "Failed to send data." << endl;
            // look up error code here using GetLastError()
        }
        if (data[i] == L"pause") {
            Sleep(5000);
        }
        else {
            Sleep(4000);
        }
    }
    // Close the pipe (automatically disconnects client too)
    CloseHandle(pipe);

    wcout << "Done." << endl;

    system("pause");
    return 0;
}
