
from goprocam import GoProCamera, constants
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time
import sys
import win32pipe, win32file, pywintypes
import os

class ControlGoPro:
    def __init__(self, goPro):
        self.goPro = goPro
        self.filename = ""
        self.active = False # might be a function, but for now will use a flag
        self.prevCommand = ""
        self.variableMap = {"CarpetDone" : "new", "PostExposure" : "start", "LayerEndVentFTU" : "pause", "PrintEndPrepareZAxis" : "stop"}
    
    def setupNewRecording(self):
        self.filename = ""
        self.goPro.delete("all")

        directory = "/Users/jana.woo/Desktop/GoPro/library"
        filenames = []

        for filename in os.listdir(directory):
            if filename.endswith('.MP4'):
                filenames.append(filename)

        for file in filenames:
            try:
                os.remove(file)
            except OSError as e:
                print("There was an error deleting this file: ", file)
        
        if self.goPro.getStatus(constants.Status.Status, constants.Status.STATUS.IsRecording) != 0:
            # raise Exception("There is already a recording in progress.")
            print("There is already a recording in progress.")
        
        self.active = True
        
        # self.filename = input("What would you like to name the file? ")
        self.filename = ""

        if self.filename == "":
            date = datetime.today()
            dateModified = date.strftime("%Y-%m-%d--")
            time = datetime.now()
            timeModified = time.strftime("%M%S-.MP4")
            self.filename = "GoProRecording" + dateModified + timeModified
            print("New Filename: ", self.filename)
        else:
            self.filename += ".MP4"
    
    def startRecording(self):
        if not self.active:
            # raise Exception("You must setup a new recording to start recording.")
            print("You must setup a new recording to start recording.")
        
        # save the file using the filename when ur fully done with recording everything?

        self.goPro.shutter(constants.start)
    
    def pauseRecording(self):
        if not self.active or self.goPro.getStatus(constants.Status.Status, constants.Status.STATUS.IsRecording) == 0:
            # raise Exception("There is no recording to be paused.")
            print("There is no recording to be paused.")
        self.goPro.shutter(constants.stop)
        time.sleep(1)
        self.goPro.downloadLastMedia()
    
    def stopRecording(self):
        if not self.active or self.prevCommand != "pause":
            # raise Exception("There is no recording that needs to be stopped.")
            print("There is no recording that needs to be stopped.")
        self.active = False
        
        directory = "/Users/jana.woo/Desktop/GoPro/library"
        filenames = []

        for filename in os.listdir(directory):
            if filename.endswith('.MP4'):
                filenames.append(filename)

        clips = []

        for file in filenames:
            clip = VideoFileClip(file)
            clips.append(clip)

        resultClip = concatenate_videoclips(clips)
        resultClip.write_videofile(self.filename)
    
    def downloadFile(self):
        if self.prevCommand != "stop":
            # raise Exception("There is no recording to download.")
            print("There is no recording to download.")
        
        directory = "/Users/jana.woo/Desktop/GoPro/library"
        filenames = []

        for filename in os.listdir(directory):
            if filename.endswith('.MP4'):
                filenames.append(filename)

        clips = []

        for file in filenames:
            clip = VideoFileClip(file)
            clips.append(clip)

        resultClip = concatenate_videoclips(clips)
        resultClip.write_videofile(self.filename)
            
    
    def turnOn(self):
        self.goPro.power_on()
    
    def turnOff(self):
        self.goPro.power_off()
    
    def checkBattery(self):
        value = goPro.parse_value("battery", goPro.getStatus(constants.Status.Status, constants.Status.STATUS.Battery))
        if value == "LOW":
            print("The GoPro's battery is low. Please charge the GoPro.")
    
    def durRecording(self):
        if self.goPro.getStatus(constants.Status.Status, constants.Status.STATUS.IsRecording) == 0:
            # raise Exception("There is not a recording in progress.")
            print("There is not a recording in progress.")
        
        timeElapsed = self.goPro.getStatus(constants.Status.Status, constants.Status.STATUS.RecordElapsed)
        print("Time Elapsed", timeElapsed, " seconds.")

    def commandCenter(self, commandPreMap):
        # command = input("Input (new, start, pause, stop, download, on, off, battery, duration): ")
        if commandPreMap not in self.variableMap:
            print("Please enter a valid command")
            return
        else:
            command = self.variableMap[commandPreMap]

        print("Next command: ", command)

        if command == "new":
            self.setupNewRecording()
        elif command == "start":
            self.startRecording()
        elif command == "pause":
            self.pauseRecording()
        elif command == "stop":
            self.stopRecording()
        elif command == "download":
            self.downloadFile()
        elif command == "on":
            self.turnOn()
        elif command == "off":
            self.turnOff()
        elif command == "battery":
            self.checkBattery()
        elif command == "duration":
            self.durRecording()
        else:
            print("Please enter a valid command.")
            
        self.prevCommand = command

    def main(self):
        while True:
            # print("before")
            # In the second line -  | win32file.GENERIC_WRITE
            # In the third line - | win32file.FILE_SHARE_DELETE | win32file.FILE_SHARE_WRITE
            # in the third line
            try:
                handle = win32file.CreateFile(
                    r'\\.\pipe\GoPro',
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None
                )
                res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
                if res == 0:
                    print(f"SetNamedPipeHandleState return code: {res}")
                while True:
                    resp = win32file.ReadFile(handle, 64*1024)
                    # print(f"message: {resp}")
                    inputCommand = resp[1].decode("utf-16-le")
                    print("Received command: ", inputCommand)
                    self.commandCenter(inputCommand)
            except pywintypes.error as e:
                print("error was thrown")
                print(e.args)
                if e.args[0] == 2:
                    print("no pipe, trying again in a sec")
                    time.sleep(1)
                elif e.args[0] == 109:
                    print("broken pipe, bye bye")
                    quit = True


if __name__ == "__main__":
    goPro = GoProCamera.GoPro()

    commands = ControlGoPro(goPro)

    commands.main()

# goPro = GoProCamera.GoPro()
# goPro.shutter(constants.start)
# time.sleep(5)
# goPro.shutter(constants.stop)
# goPro.downloadAll()
