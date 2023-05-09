import cv2

def gen_feed(multi_ip='239.255.0.1', multi_port = '1234'):

    def generate():
        cap = cv2.VideoCapture(f'udp://{multi_ip}:{multi_port}')
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            ret, buffer = cv2.imencode ('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()
        
    return generate()