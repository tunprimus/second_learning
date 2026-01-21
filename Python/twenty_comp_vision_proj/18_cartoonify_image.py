#!/usr/bin/env python3
import json
import os
import tkinter as tk
from tkinter import Label, filedialog, messagebox

import cv2
import orjson
from PIL import Image, ImageTk

# Some constants
SMALL_PAD_X = 5
SMALL_PAD_Y = 5
MID_PAD_X = 10
MID_PAD_Y = 10
BUTTON_HEIGHT = 2
BUTTON_WIDTH = 20


def cartoonify_image(image, blur_value=5, block_size=9, bilateral_filter_value=250):
    # Ensure blur_value is a positive odd number
    if blur_value % 2 == 0:
        blur_value += 1
    if blur_value < 1:
        blur_value = 1

    # Ensure block_size is a positive odd number greater than 1
    if block_size % 2 == 0:
        block_size += 1
    if block_size <= 1:
        block_size = 3  # Minimum valid value for blockSize

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grey = cv2.medianBlur(grey, blur_value)
    edges = cv2.adaptiveThreshold(
        grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, 9
    )

    colour = cv2.bilateralFilter(
        image, 9, bilateral_filter_value, bilateral_filter_value
    )
    cartoon = cv2.bitwise_and(colour, colour, mask=edges)

    return cartoon


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if file_path:
        image = cv2.imread(file_path)
        adjust_parameters_and_process(image, file_path)


def process_multiple_files():
    file_paths = filedialog.askopenfilenames(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if file_paths:
        for file_path in file_paths:
            image = cv2.imread(file_path)
            cartoon = cartoonify_image(image)
            save_cartoon(cartoon, file_path)
        messagebox.showinfo(
            "Batch Processing Complete", "All images have been cartoonified and saved!"
        )


def save_cartoon(cartoon, original_path):
    save_dir = "cartoonified_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    base_name = os.path.basename(original_path)
    save_path = os.path.join(save_dir, f"cartoonified_{base_name}")
    cv2.imwrite(save_path, cartoon)

    # Log the save operation
    log_operation(original_path, save_path)
    messagebox.showinfo("Image Saved", f"Cartoonified image saved to:\n{save_path}")


def log_operation(input_path, output_path):
    log_file = "operation_log.json"
    log_data = []

    if os.path.exists(log_file):
        with open(log_file, "r") as fip:
            try:
                log_data = orjson.loads(fip)
            except Exception:
                log_data = json.load(fip)

    log_data.append({"input": input_path, "output": output_path})

    with open(log_file, "w") as fop:
        try:
            orjson.dumps(log_data, fop)
        except Exception:
            json.dump(log_data, fop, indent=4)


def view_logs():
    log_file = "operation_log.json"
    if not os.path.exists(log_file):
        messagebox.showwarning(
            "No Logs", "No logs found. Perform some operations first."
        )
        return

    with open(log_file, "r") as fip:
        try:
            logs = orjson.loads(fip)
        except Exception:
            logs = json.load(fip)

    log_window = tk.Toplevel()
    log_window.title("Operation Logs")

    log_text = tk.Text(log_window, wrap="word", height=20, width=60)
    for entry in logs:
        log_text.insert(
            "end", f"Input: {entry['input']}\nOutput: {entry['output']}\n\n"
        )
    log_text.config(state="disabled")
    log_text.pack(padx=MID_PAD_X, pady=MID_PAD_Y)

    close_button = tk.Button(log_window, text="Close", command=log_window.destroy)
    close_button.pack(pady=MID_PAD_Y)


def adjust_parameters_and_process(image, file_path):
    param_window = tk.Toplevel()
    param_window.title("Adjust Parameters")

    # Parameters
    tk.Label(param_window, text="Blur Value (1-15):").grid(
        row=0, column=0, padx=SMALL_PAD_X, pady=SMALL_PAD_Y
    )
    blur_value = tk.Scale(param_window, from_=1, to=15, orient="horizontal")
    blur_value.set(5)
    blur_value.grid(row=0, column=1, padx=SMALL_PAD_X, pady=SMALL_PAD_Y)

    tk.Label(param_window, text="Block Size (1-15):").grid(
        row=1, column=0, padx=SMALL_PAD_X, pady=SMALL_PAD_Y
    )
    block_size = tk.Scale(param_window, from_=1, to=15, orient="horizontal")
    block_size.set(9)
    block_size.grid(row=1, column=1, padx=SMALL_PAD_X, pady=SMALL_PAD_Y)

    tk.Label(param_window, text="Bilateral Filter Value (100-500):").grid(
        row=2, column=0, padx=SMALL_PAD_X, pady=SMALL_PAD_Y
    )
    bilateral_value = tk.Scale(param_window, from_=100, to=500, orient="horizontal")
    bilateral_value.set(250)
    bilateral_value.grid(row=2, column=1, padx=SMALL_PAD_X, pady=SMALL_PAD_Y)

    def process_with_parameters():
        cartoon = cartoonify_image(
            image, blur_value.get(), block_size.get(), bilateral_value.get()
        )
        display_cartoon(cartoon)
        save_option = messagebox.askyesno(
            "Save Image", "Do you want to save the cartoonified image?"
        )
        if save_option:
            save_cartoon(cartoon, file_path)

    process_button = tk.Button(
        param_window, text="Process Image", command=process_with_parameters
    )
    process_button.grid(row=3, column=0, columnspan=2, pady=MID_PAD_Y)


def display_cartoon(cartoon):
    cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    cartoon_pil = Image.fromarray(cartoon_rgb)
    cartoon_tk = ImageTk.PhotoImage(cartoon_pil)

    preview_window = tk.Toplevel()
    preview_window.title("Cartoonified Preview")

    label = tk.Label(preview_window, image=cartoon_tk)
    label.image = cartoon_tk
    label.pack()

    close_button = tk.Button(
        preview_window, text="Close", command=preview_window.destroy
    )
    close_button.pack(pady=MID_PAD_Y)


def main():
    root = tk.Tk()
    root.title("Cartoonify Image")
    root.resizable(True, True)

    # Title Label
    label = Label(root, text="Cartoonification of Images", font=("Arial", 18))
    label.pack(pady=20)

    # Open File Button
    open_button = tk.Button(
        root,
        text="Open Image",
        command=open_file,
        height=BUTTON_HEIGHT,
        width=BUTTON_WIDTH,
    )
    open_button.pack(pady=MID_PAD_Y)

    # Batch Processing Button
    batch_button = tk.Button(
        root,
        text="Batch Process Images",
        command=process_multiple_files,
        height=BUTTON_HEIGHT,
        width=BUTTON_WIDTH,
    )
    batch_button.pack(pady=MID_PAD_Y)

    # View Logs Button
    log_button = tk.Button(
        root,
        text="View Logs",
        command=view_logs,
        height=BUTTON_HEIGHT,
        width=BUTTON_WIDTH,
    )
    log_button.pack(pady=MID_PAD_Y)

    # Footer
    footer_label = Label(
        root, text="Created with OpenCV and Tkinter", font=("Arial", 8), fg="grey"
    )
    footer_label.pack(pady=MID_PAD_Y)

    root.mainloop()


if __name__ == "__main__":
    main()
