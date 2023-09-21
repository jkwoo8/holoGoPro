# holoGoPro

[Project documentation: ](https://docs.google.com/document/d/1_5s2ieNZGdISDR6xQpITRaY2e29EQ-QsLLo4al05tkc/edit?usp=sharing)

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
