from img_progress.ComputerVision import ComputerVision
path = "../imageClearn/web_sk/1.png"
imgJson = ComputerVision.img_detect(path)
paraJson = ComputerVision.paragraph_detect(path)
print(len(paraJson))