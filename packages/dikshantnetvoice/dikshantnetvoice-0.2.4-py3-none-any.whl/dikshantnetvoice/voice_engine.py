from vosk import Model, KaldiRecognizer
import pyaudio
import json
from .utils import parse_natural_language
from .commands import NetworkCommands
from pathlib import Path


class VoiceEngine:
    def __init__(self, model_path=None):
        # Resolve the model path safely and reliably
        if model_path is None:
            model_path = Path(__file__).parent / "data" / "model"

        self.model = Model(str(model_path))  # Vosk expects string path
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        self.net = NetworkCommands()

    def _execute_command(self, parsed: dict):
        """Execute parsed command"""
        cmd = parsed.get('command', '')

        if cmd == 'get_ip':
            return str(self.net.get_ip())
        elif cmd == 'scan_ports':
            return str(self.net.scan_ports(parsed.get('start', 1), parsed.get('end', 100)))
        elif cmd == 'ping' and 'host' in parsed:
            return "Ping successful" if self.net.ping(parsed['host']) else "Ping failed"

        return f"Unknown command: {cmd}"

    def listen(self) -> str:
    """Listen and execute voice commands"""
    print("Listening... (say 'stop' to exit)")
    while True:
        try:
            data = self.stream.read(4096, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if result['text']:
                    parsed = parse_natural_language(result['text'])
                    return self._execute_command(parsed)
        except OSError:
            print("⚠️ Microphone input overflowed. Skipping buffer...")


    def __del__(self):
        """Release audio resources when the object is deleted"""
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.mic.terminate()
        except Exception:
            pass  # Safe cleanup
