
from goprocam import GoProCamera, constants
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time
import os

class ControlGoPro:
    def __init__(self, goPro):
        self.goPro = goPro
        self.filename = ""
        self.active = False # might be a function, but for now will use a flag
        self.prevCommand = ""
    
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
            raise Exception("There is already a recording in progress.")
        
        self.active = True
        
        self.filename = input("What would you like to name the file? ")

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
            raise Exception("You must setup a new recording to start recording.")
        
        # save the file using the filename when ur fully done with recording everything?

        self.goPro.shutter(constants.start)
    
    def pauseRecording(self):
        if not self.active or self.goPro.getStatus(constants.Status.Status, constants.Status.STATUS.IsRecording) == 0:
            raise Exception("There is no recording to be paused.")
        self.goPro.shutter(constants.stop)
        time.sleep(1)
        self.goPro.downloadLastMedia()
        # weird looping if its the 5 seconds on and 15 seconds off, automatically stopping
        # while True:
        #     # time.sleep(5)
        #     timeElapsed = self.goPro.getStatus(constants.Status.Status, constants.Status.STATUS.RecordElapsed)
        #     if timeElapsed >= 5:
        #         self.goPro.shutter(constants.stop)
        #         time.sleep(15)
        #         command = input("Input (new, start, pause, stop, download): ")

        #         if command == "start":
        #             # not sure if we can have all these shutters(videos) without saving them to a filename
        #             self.startRecording()
        #         else:
        #             break
    
    def stopRecording(self):
        if not self.active or self.prevCommand != "pause":
            raise Exception("There is no recording that needs to be stopped.")
        self.active = False
    
    def downloadFile(self):
        if self.prevCommand != "stop":
            raise Exception("There is no recording to download.")
        
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
            raise Exception("There is not a recording in progress.")
        
        timeElapsed = self.goPro.getStatus(constants.Status.Status, constants.Status.STATUS.RecordElapsed)
        print("Time Elapsed", timeElapsed, " seconds.")

    def main(self):
        while True:
            command = input("Input (new, start, pause, stop, download, on, off, battery, duration): ")
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

if __name__ == "__main__":
    goPro = GoProCamera.GoPro()

    commands = ControlGoPro(goPro)

    commands.main()

# goPro = GoProCamera.GoPro()
# goPro.shutter(constants.start)
# time.sleep(5)
# goPro.shutter(constants.stop)
# goPro.downloadAll()
