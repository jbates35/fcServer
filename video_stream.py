import cv2

def gen_feed(multi_ip='127.0.0.1', multi_port = '1595'):

    def generate():
        print("Generating feed")
        
        cap = cv2.VideoCapture(f'udp://{multi_ip}:{multi_port}')
        
        print("Feed generated")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No frame")
                break
            
            ret, buffer = cv2.imencode ('.jpg', frame)
            frame = buffer.tobytes()
            
            if frame is not None:
                print("Frame found")
                
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()
        
    return generate()

if __name__ == "__main__":
    udp_address = '127.0.0.1'
    udp_port = 1595

    # Create a VideoCapture object
    cap = cv2.VideoCapture(f'udp://{udp_address}:{udp_port}')
    
    print("VideoCapture object created")

    # Check if the VideoCapture object was successfully initialized
    if not cap.isOpened():
        print('Failed to open UDP video feed')
        exit()

    # Read frames from the video feed
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print('Failed to capture frame')
            break

        # Display the frame
        cv2.imshow('UDP Video Feed', frame)

        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close windows
    cap.release()
    cv2.destroyAllWindows()