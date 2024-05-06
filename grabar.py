import cv2
import os

class VideoRecorder:
    def __init__(self, cap, record_button, output_dir=None):
        self.cap = cap
        self.record_button = record_button
        self.is_recording = False
        self.output_dir = output_dir  # Agregar el nuevo argumento

    def record_video(self):
        if not self.is_recording:
            self.is_recording = True
            if self.output_dir:
                video_name = os.path.join(self.output_dir, "video.mp4")  # Utilizar el output_dir
            else:
                video_name = "video.mp4"
            fourcc = cv2.VideoWriter_fourcc(*"XVID")  # Cambiado el códec a XVID
            frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"H264"), 30, (frame_width, frame_height))

            self.record_button.setText("Stop")
        else:
            self.is_recording = False
            self.out.release()
            self.record_button.setText("Record")

