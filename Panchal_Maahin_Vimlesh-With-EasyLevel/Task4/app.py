import pyaudio
import wave
import os
import matplotlib.pyplot as plt
import numpy as np

class VoiceRecorder:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16  # Format of audio format (16-bit PCM)
        self.CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
        self.RATE = 44100  # Sample rate (samples per second)
        self.CHUNK = 1024  # Number of frames per buffer
        self.RECORD_SECONDS = 5  # Duration of recording in seconds
        self.WAVE_OUTPUT_FILENAME = "output.wav"  # Default output file name
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

    def start_recording(self):
        # Open audio stream
        self.stream = self.audio.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)

        print("Recording...")

        self.frames = []  # Clear existing frames

        # Record audio in chunks and store in frames
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        print("Finished recording.")

        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()

    def save_recording(self, filename=None):
        if filename is None:
            filename = self.WAVE_OUTPUT_FILENAME

        # Write the audio data to a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Recording saved as {filename}")

    def playback(self, filename=None):
        if filename is None:
            filename = self.WAVE_OUTPUT_FILENAME

        # Check if file exists
        if not os.path.isfile(filename):
            print(f"File '{filename}' does not exist.")
            return

        # Open the saved WAV file for playback
        wf = wave.open(filename, 'rb')

        # Create an audio stream
        stream_out = self.audio.open(format=self.audio.get_format_from_width(wf.getsampwidth()),
                                     channels=wf.getnchannels(),
                                     rate=wf.getframerate(),
                                     output=True)

        print("Playing back recorded audio...")

        # Read data in chunks and play it
        data = wf.readframes(self.CHUNK)
        while len(data) > 0:
            stream_out.write(data)
            data = wf.readframes(self.CHUNK)

        # Stop and close the stream
        stream_out.stop_stream()
        stream_out.close()
        wf.close()

        print("Playback finished.")

    def plot_waveform(self, filename=None):
        if filename is None:
            filename = self.WAVE_OUTPUT_FILENAME

        # Check if file exists
        if not os.path.isfile(filename):
            print(f"File '{filename}' does not exist.")
            return

        # Open the saved WAV file
        wf = wave.open(filename, 'rb')

        # Read data
        frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)

        # Plot waveform
        plt.figure(figsize=(12, 4))
        plt.plot(data)
        plt.title('Waveform')
        plt.xlabel('Time (samples)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.show()

        # Close the file
        wf.close()

    def close(self):
        # Terminate PyAudio instance
        self.audio.terminate()

if __name__ == '__main__':
    recorder = VoiceRecorder()

    # Record audio
    recorder.start_recording()

    # Save recording to file
    recorder.save_recording()

    # Playback the recorded audio
    recorder.playback()

    # Plot waveform
    recorder.plot_waveform()

    # Close the PyAudio instance
    recorder.close()
