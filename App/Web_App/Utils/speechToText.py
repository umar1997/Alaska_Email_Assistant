import os

import io
import wave
from google.cloud import speech


os.environ['GOOGLE_APPLICATION_CREDENTIALS']= './Keys/alaska-email-assistant-key.json'


class SpeechToText:
    """
    Function: Convert from.WAV file to Text

    Input:
    -   Filepath

    Output:
    -   Text

    """ 
    def __init__(self, filepath):

        self.file_path = filepath

    def readAudio(self,):

        with io.open(self.file_path, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        print('Read Audio File.')
        return audio

    def frame_rate_channel_duration(self, ):

        # x, samplerate  = librosa.load(self.file_path, sr = 16000)
        # sf.write('./../Speech_Files/Temp.wav', x, samplerate )
        # with wave.open('./../Speech_Files/Temp.wav', "rb") as wave_file:
        with wave.open(self.file_path, "rb") as wave_file:
            frames = wave_file.getnframes()
            frame_rate = wave_file.getframerate()
            channels = wave_file.getnchannels()
            duration = round(frames / float(frame_rate), 3)
        return frame_rate, channels, duration

    def getConfig(self,):

        frame_rate, channels, duration = self.frame_rate_channel_duration()

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            enable_automatic_punctuation=True,
            sample_rate_hertz = frame_rate,
            audio_channel_count=channels,
            language_code="en-US",
        )

        print('Frame Rate: {}, # of Channels: {}, Duration: {}'.format(frame_rate, channels, duration))
        return config

    def clientRequest(self,):

        audio = self.readAudio()
        config = self.getConfig()

        print('Created Client Instance.')
        client = speech.SpeechClient()
        print('Sending Google API Request.')
        response = client.recognize(request={"config": config, "audio": audio})

        return response

    def convertToText(self,):
        # https://cloud.google.com/speech-to-text/docs/reference/rest/v1/speech/recognize#response-body
        response = self.clientRequest()

        # print('Billed Time: {}'.format(response.totalBilledTime))
        for result in response.results:
            print("Confidence: {} \n Text: {}".format(result.alternatives[0].confidence, result.alternatives[0].transcript))
            return result.alternatives[0].transcript


if __name__ == "__main__": 
    file_path = './../Speech_Files/Email.wav'
    voice = SpeechToText(file_path)
    voice.convertToText()
    