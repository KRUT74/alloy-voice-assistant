# Alloy Voice Assistant

A voice-enabled AI assistant that can see through your webcam and respond to voice commands.

## Prerequisites

1. Python 3.8 or higher installed on your system
2. Git installed on your system
3. A webcam and microphone
4. API keys:
   - OpenAI API key
   - Google API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KRUT74/alloy-voice-assistant.git
cd alloy-voice-assistant
```

2. Create and activate a virtual environment:

For macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install system dependencies:

For Apple Silicon (M1/M2) Macs:
```bash
brew install portaudio
```

For Ubuntu/Debian:
```bash
sudo apt-get install python3-dev portaudio19-dev python3-pyaudio
```

For Windows:
No additional system dependencies required.

4. Install Python dependencies:
```bash
pip install -U pip
pip install -r requirements.txt
```

5. Set up your API keys:
Create a `.env` file in the project root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated:
```bash
source .venv/bin/activate  # For macOS/Linux
# or
.venv\Scripts\activate    # For Windows
```

2. Run the assistant:
```bash
python3 assistant.py
```

3. To exit the application:
- Press 'q' or 'ESC' key
- Or use Ctrl+C in the terminal

## Features

- Voice command recognition
- Real-time webcam feed analysis
- AI-powered responses
- Text-to-speech output
- Hardware verification tools (test_camera.py, test_microphone.py)

## Troubleshooting

If you encounter permission issues with the webcam or microphone:
1. Make sure you've granted camera and microphone permissions to your terminal/IDE
2. Check if your webcam and microphone are properly connected
3. Ensure no other application is using the webcam or microphone

For any other issues, please check the Issues section or create a new issue.