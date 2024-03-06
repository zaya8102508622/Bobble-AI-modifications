import tkinter as tk
import cv2
import numpy as np
import os
from PIL import Image
import io

class KeyboardApp:
    def __init__(self, master):
        self.master = master
        master.title("Virtual Keyboard")

        self.text_box = tk.Entry(master, width=50)
        self.text_box.grid(row=0, column=0, columnspan=3, padx=2, pady=2)

        self.create_keyboard_buttons()

        self.drawing_canvas = tk.Canvas(master, width=200, height=200, bg="white")
        self.drawing_canvas.grid(row=1, column=4, rowspan=6, padx=5, pady=5)
        self.drawing_canvas.bind("<B1-Motion>", self.draw)

    def create_keyboard_buttons(self):
        buttons = [
            ('Q', 0, 0), ('W', 0, 1), ('E', 0, 2), ('R', 0, 3), ('T', 0, 4),
            ('Y', 0, 5), ('U', 0, 6), ('I', 0, 7), ('O', 0, 8), ('P', 0, 9),
            ('A', 1, 0), ('S', 1, 1), ('D', 1, 2), ('F', 1, 3), ('G', 1, 4),
            ('H', 1, 5), ('J', 1, 6), ('K', 1, 7), ('L', 1, 8),
            ('Z', 2, 0), ('X', 2, 1), ('C', 2, 2), ('V', 2, 3), ('B', 2, 4),
            ('N', 2, 5), ('M', 2, 6),
            ('Space', 3, 2), ('Backspace', 3, 3),
            ('😀', 4, 4), ('😂', 4, 5), ('😊', 4, 6), ('😍', 4, 7),
            ('🥳', 4, 8), ('😎', 4, 9), ('🤩', 4, 10), ('😜', 4, 11),
            ('😇', 4, 12), ('🤗', 4, 13),
            ('🙄', 5, 4), ('😏', 5, 5), ('😬', 5, 6), ('😳', 5, 7),
            ('😡', 5, 8), ('🤔', 5, 9), ('😴', 5, 10), ('😷', 5, 11),
            ('🤒', 5, 12), ('🤕', 5, 13),
            ('Generate Caricature', 6, 0) # Add a button to generate caricature
        ]

        for text, row, column in buttons:
            if text == 'Generate Caricature': # If the button is for generating caricature
                button = tk.Button(self.master, text=text, width=15, height=2, command=self.generate_caricature)
            else:
                button = tk.Button(self.master, text=text, width=8, height=2, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row + 1, column=column, padx=5, pady=5)

    def on_button_click(self, text):
        current_text = self.text_box.get()
        if text == "Backspace":
            self.text_box.delete(len(current_text) - 1, tk.END)
        elif text == "Space":
            self.text_box.insert(tk.END, " ")
        else:
            self.text_box.insert(tk.END, text)

    def draw(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.drawing_canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)

    def generate_caricature(self):
        # Convert the drawn image to an array
        drawn_image = self.canvas_to_image()

        # Generate the caricature of the drawn image
        caricature = self.generate_caricature_from_image(drawn_image)

        # Display the caricature
        cv2.imshow('Caricature', caricature)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def canvas_to_image(self):
        # Convert the drawn image on the canvas to an array
        drawn_image = np.zeros((200, 200, 3), dtype=np.uint8)
        image = self.drawing_canvas.postscript(colormode='color')
        image = Image.open(io.BytesIO(image.encode('utf-8')))
        image = np.array(image)
        drawn_image[:, :, :] = image[:, :, :3]  # remove alpha channel
        drawn_image = cv2.cvtColor(drawn_image, cv2.COLOR_BGR2RGB)
        return drawn_image

    def generate_caricature_from_image(self, image):
        # Apply caricature effect to the image
        # This is where you would implement your caricature algorithm
        # For demonstration purposes, let's just resize the image
        caricature = cv2.resize(image, (200, 200))
        return caricature

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardApp(root)
    root.mainloop()
