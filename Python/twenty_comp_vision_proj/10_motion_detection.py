#!/usr/bin/env python3
import cv2
try:
    import customtkinter as tk
    print("Using customtkinter")
except ImportError:
    import tkinter as tk
    print("Using tkinter")
try:
    from customtkinter import ttk
    print("Using customtkinter")
except ImportError:
    from tkinter import ttk
    print("Using tkinter")
# from tkinter import messagebox

class MotionDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motion Detection")
        self.root.geometry("300x150")
        self.root.resizable(True, True)

        self.start_button = ttk.Button(root, text="Start Detection", command=self.start_detection)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(root, text="Status: Not running")
        self.status_label.pack(pady=5)

        self.running = False
        self.cap = None

    def start_detection(self):
        self.running = True
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.status_label.configure(text="Status: Running")
        self.detect_motion()

    def stop_detection(self):
        self.running = False
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.status_label.configure(text="Status: Not running")
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()

    def detect_motion(self):
        self.cap = cv2.VideoCapture(0)
        _, prev_frame = self.cap.read()
        prev_grey = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        prev_grey = cv2.GaussianBlur(prev_grey, (21, 21), 0)

        while self.running:
            _, frame = self.cap.read()
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grey = cv2.GaussianBlur(grey, (21, 21), 0)

            delta_frame = cv2.absdiff(prev_grey, grey)
            thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Motion Detection", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or not self.running:
                break

            prev_grey = grey.copy()

        self.stop_detection()

if __name__ == "__main__":
    try:
        root = tk.CTk()
    except AttributeError:
        root = tk.Tk()
    app = MotionDetectionApp(root)
    root.mainloop()
