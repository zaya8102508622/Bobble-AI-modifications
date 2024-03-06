import cv2
import os

def cartoonize_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median blur to reduce image noise
    gray = cv2.medianBlur(gray, 5)

    # Detect edges in the image and threshold it
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter to smooth the image while preserving edges
    color = cv2.bilateralFilter(image, 9, 300, 300)

    # Combine the edges and color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

def save_cartoonized_image(image, save_dir, filename):
    # Construct the file path for saving the image
    image_path = os.path.join(save_dir, filename)

    # Save the image
    cv2.imwrite(image_path, image)
    print(f"Cartoonized image saved as {filename} in the gallery!")

def camera_access():
    # Open the default camera (camera index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't read frame.")
            break

        # Apply cartoonize filter to the frame
        cartoon_frame = cartoonize_image(frame)

        # Display the resulting cartoon frame
        cv2.imshow('Cartoonized Camera Feed', cartoon_frame)

        # Check for key press events
        key = cv2.waitKey(1) & 0xFF

        # Break the loop when the 'q' key is pressed
        if key == ord('q'):
            break

        # Take a snapshot when the 's' key is pressed
        elif key == ord('s'):
            # Get the directory for saving images (change this to your desired directory)
            save_dir = 'D:\html css'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Generate a unique filename for the saved image
            filename = f'cartoonized_photo_{len(os.listdir(save_dir)) + 1}.png'

            # Save the cartoonized image
            save_cartoonized_image(cartoon_frame, save_dir, filename)

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_access()
