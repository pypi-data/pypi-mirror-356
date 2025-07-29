from typing import Any, Dict, Optional, List, Tuple, Union

from ovos_config.config import Configuration
from ovos_plugin_manager.stt import OVOSSTTFactory
from ovos_plugin_manager.templates.stt import StreamingSTT, StreamThread
from ovos_plugin_manager.utils import ReadWriteStream
from ovos_utils.log import LOG
from speech_recognition import AudioData


class FakeStreamThread(StreamThread):

    def __init__(self, queue, language, engine, sample_rate, sample_width):
        super().__init__(queue, language)
        self.buffer = ReadWriteStream()
        self.engine = engine
        self.sample_rate = sample_rate
        self.sample_width = sample_width

    def finalize(self):
        """ return final transcription """

        if not self.buffer:
            return ""

        try:
            # plugins expect AudioData objects
            audio = AudioData(self.buffer.read(),
                              sample_rate=self.sample_rate,
                              sample_width=self.sample_width)
            transcript = self.engine.execute(audio, self.language)

            self.buffer.clear()
            return transcript
        except Exception:
            LOG.exception(f"Error in STT plugin: {self.engine.__class__.__name__}")
        return None

    def handle_audio_stream(self, audio, language):
        for chunk in audio:
            self.update(chunk)

    def update(self, chunk: bytes):
        self.buffer.write(chunk)


class FakeStreamingSTT(StreamingSTT):
    def __init__(self, engine, config=None):
        super().__init__(config)
        self.engine = engine

    def create_streaming_thread(self):
        listener = Configuration().get("listener", {})
        sample_rate = listener.get("sample_rate", 16000)
        sample_width = listener.get("sample_width", 2)
        return FakeStreamThread(self.queue, self.lang, self.engine, sample_rate,
                                sample_width)

    def transcribe(self, audio: Optional[Union[bytes, AudioData]] = None,
                   lang: Optional[str] = None) -> List[Tuple[str, float]]:
        """transcribe audio data to a list of
        possible transcriptions and respective confidences"""
        # plugins expect AudioData objects
        if audio is None:
            audiod = AudioData(self.stream.buffer.read(),
                               sample_rate=self.stream.sample_rate,
                               sample_width=self.stream.sample_width)
            self.stream.buffer.clear()
        elif isinstance(audio, bytes):
            audiod = AudioData(audio,
                               sample_rate=self.stream.sample_rate,
                               sample_width=self.stream.sample_width)
        elif isinstance(audio, AudioData):
            audiod = audio
        else:
            raise ValueError(f"'audio' must be 'bytes' or 'AudioData', got '{type(audio)}'")
        LOG.debug(f"Transcribing with lang: {lang}")
        return self.engine.transcribe(audiod, lang)


def load_stt_module(config: Dict[str, Any] = None) -> StreamingSTT:
    """
    Load an STT module based on configuration
    @param config: STT or global configuration or None (uses Configuration)
    @return: Initialized StreamingSTT plugin
    """
    # Create a copy because we're setting default values here
    stt_config = config or Configuration().get("stt", {})
    stt_config = dict(stt_config)
    default_lang = Configuration().get('lang')
    stt_config.setdefault("lang", default_lang)
    if stt_config['lang'] != default_lang:
        LOG.warning(f"STT lang ({stt_config['lang']} differs from global "
                    f"({Configuration.get('lang')}")
    plug = OVOSSTTFactory.create(stt_config)
    if not isinstance(plug, StreamingSTT):
        LOG.debug(f"Using FakeStreamingSTT wrapper with config={config}")
        return FakeStreamingSTT(plug, config)
    return plug


def load_fallback_stt(cfg: Dict[str, Any] = None) -> Optional[StreamingSTT]:
    """
    Load a fallback STT module based on configuration
    @param cfg: STT or global configuration or None (uses Configuration)
    @return: Initialized StreamingSTT plugin if configured, else None
    """
    cfg = cfg or Configuration().get("stt", {})
    default_lang = Configuration().get('lang')
    fbm = cfg.get("fallback_module")
    if not fbm:
        return None
    try:
        config = cfg.get(fbm, {})
        config.setdefault("lang", default_lang)
        if config['lang'] != default_lang:
            LOG.warning(f"Fallback STT lang ({config['lang']} differs from "
                        f"global ({Configuration.get('lang')}")
        plug = OVOSSTTFactory.create({"module": fbm, fbm: config})
        if not isinstance(plug, StreamingSTT):
            LOG.debug(f"Using FakeStreamingSTT wrapper with config={config}")
            return FakeStreamingSTT(plug, config)
        return plug
    except:
        LOG.exception("Failed to load fallback STT")
        return None
