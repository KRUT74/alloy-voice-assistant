import base64
from threading import Lock, Thread

import cv2
import openai
from cv2 import VideoCapture, imencode
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from pyaudio import PyAudio, paInt16
from speech_recognition import Microphone, Recognizer, UnknownValueError

load_dotenv()


class WebcamStream:
    def __init__(self):
        self.stream = None
        self.frame = None
        self.running = False
        self.lock = Lock()
        self._initialize_camera()

    def _initialize_camera(self):
        try:
            self.stream = VideoCapture(index=0)
            if not self.stream.isOpened():
                raise Exception("Failed to open webcam")
            _, self.frame = self.stream.read()
            if self.frame is None:
                raise Exception("Failed to capture frame from webcam")
        except Exception as e:
            print(f"Error initializing webcam: {str(e)}")
            print("Please ensure your webcam is connected and you have granted camera permissions.")
            raise

    def start(self):
        if self.running:
            return self

        if self.stream is None or not self.stream.isOpened():
            self._initialize_camera()

        self.running = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.running:
            if not self.stream.isOpened():
                print("Webcam stream was closed")
                self.running = False
                break
                
            ret, frame = self.stream.read()
            if not ret or frame is None:
                print("Failed to capture frame")
                continue

            self.lock.acquire()
            self.frame = frame
            self.lock.release()

    def read(self, encode=False):
        if self.frame is None:
            print("No frame available")
            return None

        self.lock.acquire()
        frame = self.frame.copy()
        self.lock.release()

        if encode:
            _, buffer = imencode(".jpeg", frame)
            return base64.b64encode(buffer)

        return frame

    def stop(self):
        self.running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()
        if self.stream is not None:
            self.stream.release()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()


class Assistant:
    def __init__(self, model):
        self.chain = self._create_inference_chain(model)

    def answer(self, prompt, image):
        if not prompt:
            return

        print("Prompt:", prompt)

        response = self.chain.invoke(
            {"prompt": prompt, "image_base64": image.decode()},
            config={"configurable": {"session_id": "unused"}},
        ).strip()

        print("Response:", response)

        if response:
            self._tts(response)

    def _tts(self, response):
        player = PyAudio().open(format=paInt16, channels=1, rate=24000, output=True)

        with openai.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            response_format="pcm",
            input=response,
        ) as stream:
            for chunk in stream.iter_bytes(chunk_size=1024):
                player.write(chunk)

    def _create_inference_chain(self, model):
        SYSTEM_PROMPT = """
        You are a witty assistant that will use the chat history and the image 
        provided by the user to answer its questions. Your job is to answer 
        questions.

        Use few words on your answers. Go straight to the point. Do not use any
        emoticons or emojis. 

        Be friendly and helpful. Show some personality.
        """

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    [
                        {"type": "text", "text": "{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                ),
            ]
        )

        chain = prompt_template | model | StrOutputParser()

        chat_message_history = ChatMessageHistory()
        return RunnableWithMessageHistory(
            chain,
            lambda _: chat_message_history,
            input_messages_key="prompt",
            history_messages_key="chat_history",
        )


# You can use OpenAI's GPT-4o model instead of Gemini Flash
# by uncommenting the following line:
model = ChatOpenAI(model="gpt-4o")

try:
    webcam_stream = WebcamStream().start()
    assistant = Assistant(model)

    def audio_callback(recognizer, audio):
        try:
            prompt = recognizer.recognize_whisper(audio, model="base", language="english")
            frame = webcam_stream.read(encode=True)
            if frame is not None:
                assistant.answer(prompt, frame)
            else:
                print("Unable to capture webcam frame")

        except UnknownValueError:
            print("There was an error processing the audio.")

    recognizer = Recognizer()
    microphone = Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    stop_listening = recognizer.listen_in_background(microphone, audio_callback)

    while True:
        frame = webcam_stream.read()
        if frame is not None:
            cv2.imshow("webcam", frame)
        if cv2.waitKey(1) in [27, ord("q")]:
            break

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    if 'webcam_stream' in locals():
        webcam_stream.stop()
    cv2.destroyAllWindows()
    if 'stop_listening' in locals():
        stop_listening(wait_for_stop=False)
