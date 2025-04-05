import cv2

def test_camera():
    print("Testing webcam access...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        print("Please check:")
        print("1. Your webcam is connected")
        print("2. You've granted camera permissions to Terminal/VS Code")
        print("3. No other application is using the webcam")
        return False
    
    print("Successfully opened webcam")
    ret, frame = cap.read()
    
    if not ret or frame is None:
        print("Error: Could not capture frame from webcam")
        return False
    
    print("Successfully captured frame from webcam")
    print(f"Frame size: {frame.shape}")
    
    cap.release()
    return True

if __name__ == "__main__":
    test_camera() 