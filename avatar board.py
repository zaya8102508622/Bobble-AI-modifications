import tkinter as tk
import cv2

class KeyboardApp:
    def __init__(self, master):
        self.master = master
        master.title("Virtual Keyboard")

        self.text_box = tk.Entry(master, width=50)
        self.text_box.grid(row=0, column=0, columnspan=3, padx=2, pady=2)

        self.create_keyboard_buttons()

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
            ('📷', 6, 6) # Add a camera button
        ]

        for text, row, column in buttons:
            if text == '📷': # If the button is the camera button
                button = tk.Button(self.master, text=text, width=8, height=2, command=self.capture_image)
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

    def capture_image(self):
        # Open the camera
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Display the captured frame
            cv2.imshow('Capture Image', frame)
            
            # Check if the user pressed the 'c' key to capture the photo
            key = cv2.waitKey(1)
            if key == ord('c'):
                # Save the captured frame as an image
                cv2.imwrite('captured_photo.jpg', frame)

                # Convert the captured photo to AI avatar
                avatar = self.generate_avatar('captured_photo.jpg')

                # Display the AI avatar
                cv2.imshow('AI Avatar', avatar)

                # Exit the loop after capturing and converting the photo
                break

            # Check if the user pressed the 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardApp(root)
    root.mainloop()