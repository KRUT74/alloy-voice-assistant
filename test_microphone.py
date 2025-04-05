import speech_recognition as sr

def test_microphone():
    print("Testing microphone access...")
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Successfully opened microphone")
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone is ready to use")
            return True
    except Exception as e:
        print(f"Error accessing microphone: {str(e)}")
        print("Please check:")
        print("1. Your microphone is connected")
        print("2. You've granted microphone permissions to Terminal/VS Code")
        print("3. No other application is using the microphone")
        return False

if __name__ == "__main__":
    test_microphone() 