from audio_grabber import *
import os

outputPath = "./audiofiles/"
inputPath = "./scripts/"
files = os.listdir(inputPath)
print("\n")
for i in range(len(files)):
    print(str(i+1) + ": " + files[i])
selectedFile = input("\nEnter corresponding number of the desired file:\n")
inputFile = files[int(selectedFile)-1]
print("Chosen file:" + files[int(selectedFile)-1])

with open(inputPath + files[int(selectedFile)-1], encoding="utf8") as scriptFile:
    for line in scriptFile:
        iterName = line[:10]
        iterScript = line[11:]
        try:
            fetch_audio(iterScript, outputPath, iterName)
        except KeyboardInterrupt:
            print("❌ Error: KeyboardInterrupt\n")