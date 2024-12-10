import threading
import cv2
import time

class Thread (threading.Thread):
    def __init__(self, threadID,ip):
        threading.Thread.__init__(self)
        self.threadID = threadID

        self.ip = ip

    def run(self):
        print("Start threadID" +str(self.threadID))
        Core.detection(self.ip)
        print("Exiting " + str(self.threadID))

 
class Core:
    recording = False 

    @staticmethod
    def detection(ip):
        cv2.setUseOptimized(True)
        capture = cv2.VideoCapture(ip)
 
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        capture.set(cv2.CAP_PROP_FPS, 15)

        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output = None
# sua execução de código

       
        while (capture.isOpened()):
            capture.grab()
            ret, frame = capture.retrieve()
            # ret, frame = capture.read() 
        
            if ret:
                frame = cv2.resize(frame,(600,400))
                cv2.imshow(str(ip), frame)

                if Core.recording:
                    if output is None:
                        # Cria um arquivo de vídeo para gravar quando inicia a gravação
                        timestamp = time.strftime("%Y%m%d-%H%M%S")
                        output_filename = f"camera_{ip}_{timestamp}.avi"
                        output = cv2.VideoWriter(output_filename, fourcc, 15.0, (600, 400))
                        print(f"Recording started: {output_filename}")
                    output.write(frame)

                if not Core.recording and output:
                    print("Recording stopped.")
                    output.release()
                    output = None
                
                key = cv2.waitKey(1) & 0xFF
                if  key == ord('q'):
                    capture.release()
                    cv2.destroyWindow(str(ip))
                    break
                elif key == ord('s') :  # Start recording
                    Core.recording = True
                elif key == ord('x'):  # Stop recording
                    Core.recording = False
            else:
                print('attempting to reconnect', ip)
                # threads = []
                # for i, cam in enumerate(ip):
                #     thread1 = Thread(i, cam)
                #     threads.append(thread1)
                # for i in threads:
                #     i.start()
                # thread1 = Thread(1, ip)
                # thread1.start()
                Core.detection(ip)

      
   
cam_list=[
        0,1
        ]
threads = []


for i, ip in enumerate(cam_list):
    thread1 = Thread(i, ip)
    thread1.start()
    threads.append(thread1)


for t in threads:
    t.join()

