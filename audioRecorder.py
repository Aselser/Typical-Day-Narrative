# Run 'Before Experiment' code from code
import sounddevice as sd
import soundfile as sf
import threading
from queue import Queue
import serial

class AudioRecorder:
    def __init__(self, filepath, mic_id, sample_rate, channels, arduino_port, baud_rate):
        # Archivo de salida de audio
        self.filepath = filepath
        # ID del micrófono
        self.mic_id = mic_id
        # Tasa de muestreo
        self.sample_rate = sample_rate
        # Número de canales
        self.channels = channels
        # Cola de audio
        self.mic_queue = Queue()
        # Bandera de grabación
        self.recording = False
        # Bandera de solicitud de detención
        self.stop_requested = False
        
        # Conexión a la placa Arduino a través de comunicación serie
        self._serial = serial.Serial(arduino_port, baud_rate)

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self.recording:
            self.mic_queue.put(indata.copy())

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self._send_pulse_to_arduino()
            self.mic_queue = Queue()  # Reinicia la cola de audio
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()

    def stop_recording(self):
        if self.recording:
            self.stop_requested = True
            self._send_pulse_to_arduino()

    def _send_pulse_to_arduino(self):
        # Mensaje a enviar a Arduino
        message = "P"
        # Envía el mensaje a Arduino
        self._serial.write(message.encode())

    def _record_audio(self):
        with sf.SoundFile(self.filepath, mode='x', samplerate=self.sample_rate, channels=self.channels, subtype=None) as file:
            with sd.InputStream(samplerate=self.sample_rate, device=self.mic_id, channels=self.channels, callback=self.callback):
                try:
                    while not self.stop_requested:
                        file.write(self.mic_queue.get())
                except RuntimeError as re:
                    print(f"{re}. If recording was stopped by the user, then this can be ignored")
                finally:
                    self.recording = False