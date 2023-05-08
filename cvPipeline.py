import os
import numpy as np
import cv2

pipe_path = "/tmp/fishPipe"

# Open the named pipe for reading
pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)

connected = False

while not connected:
    try:
        # Attempt to read raw bytes from the named pipe
        raw_data = os.read(pipe_fd, 921600)  # Adjust the buffer size according to your frame dimensions
        
        if len(raw_data) > 0:
            connected = True
    
    except BlockingIOError:
        continue

while True:
    # Read raw bytes from the named pipe
    try:
        raw_data = os.read(pipe_fd, 921600)  # Adjust the buffer size according to your frame dimensions
    except BlockingIOError:
        continue

    # Check if any data was read
    if len(raw_data) == 0:
        continue

    # Convert raw bytes to numpy array
    frame = np.frombuffer(raw_data, dtype=np.uint8).reshape((480, 640, 3))  # Adjust the shape according to your frame dimensions

    # Display the frame
    cv2.imshow("Fish Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the named pipe and destroy the window
os.close(pipe_fd)
cv2.destroyAllWindows()
