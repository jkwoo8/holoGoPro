# holoGoPro

### ServerCPPtoGoPro.cpp
- The server coded in C++ that sends commands to the GoPro's python API.

### ServerCPPtoPy.cpp
- The server coded in C++ that sends commands to a python file (clientPytoCPP.py).

### clientPytoCPP.py
- The client coded in Python that sends commands to a C++ file (ServerCPPtoPy.cpp).

### holoGoPro_IPC.py
- Sends commands to the GoPro. Accepts input from the C++ server (ServerCPPtoGoPro.cpp).

### holoGoPro_UI.py
- Sends commands to the GoPro. Accepts user input from command prompt.
