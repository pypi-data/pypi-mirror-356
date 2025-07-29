from ovos_plugin_manager.templates.stt import STT
from ovos_stt_plugin_fasterwhisper import FasterWhisperSTT

from ovos_utils import classproperty


class ZuazoFasterWhisperSTT(STT):
    MODELS_LARGE_V3 = ["Jarbas/faster-whisper-large-v3-pt-cv13",
                       "Jarbas/faster-whisper-large-v3-ca-cv13",
                       "Jarbas/faster-whisper-large-v3-eu-cv16"]
    MODELS_LARGE_V2 = ["Jarbas/faster-whisper-large-v2-pt-cv13",
                       "Jarbas/faster-whisper-large-v2-gl-cv13",
                       "Jarbas/faster-whisper-large-v2-ca-cv13",
                       "Jarbas/faster-whisper-large-v2-es-cv13",
                       "Jarbas/faster-whisper-large-v2-eu-cv16"]
    MODELS_LARGE = ["Jarbas/faster-whisper-large-pt-cv13",
                    "Jarbas/faster-whisper-large-gl-cv13",
                    "Jarbas/faster-whisper-large-ca-cv13",
                    "Jarbas/faster-whisper-large-es-cv13",
                    "Jarbas/faster-whisper-large-eu-cv16"]
    MODELS_MEDIUM = ["Jarbas/faster-whisper-medium-pt-cv13",
                     "Jarbas/faster-whisper-medium-gl-cv13",
                     "Jarbas/faster-whisper-medium-ca-cv13",
                     "Jarbas/faster-whisper-medium-es-cv13",
                     "Jarbas/faster-whisper-medium-eu-cv16"]
    MODELS_SMALL = ["Jarbas/faster-whisper-small-pt-cv13",
                    "Jarbas/faster-whisper-small-gl-cv13",
                    "Jarbas/faster-whisper-small-ca-cv13",
                    "Jarbas/faster-whisper-small-es-cv13",
                    "Jarbas/faster-whisper-small-eu-cv16"]
    MODELS_BASE = ["Jarbas/faster-whisper-base-pt-cv13",
                   "Jarbas/faster-whisper-base-gl-cv13",
                   "Jarbas/faster-whisper-base-ca-cv13",
                   "Jarbas/faster-whisper-base-es-cv13",
                   "Jarbas/faster-whisper-base-eu-cv16"]
    MODELS_TINY = ["Jarbas/faster-whisper-tiny-pt-cv13",
                   "Jarbas/faster-whisper-tiny-gl-cv13",
                   "Jarbas/faster-whisper-tiny-ca-cv13",
                   "Jarbas/faster-whisper-tiny-es-cv13",
                   "Jarbas/faster-whisper-tiny-eu-cv16"]
    LANGUAGES = {
        "es": "spanish",
        "pt": "portuguese",
        "ca": "catalan",
        "eu": "basque",
        "gl": "galician"
    }

    def __init__(self, config: dict = None):
        super().__init__(config=config)
        model = self.config.get("model") or "small"
        mapping = {
            "tiny": self.MODELS_TINY,
            "base": self.MODELS_BASE,
            "small": self.MODELS_SMALL,
            "medium": self.MODELS_MEDIUM,
            "large-v1": self.MODELS_LARGE,
            "large-v2": self.MODELS_LARGE_V2,
            "large-v3": self.MODELS_LARGE_V3
        }
        if model in ['tiny', 'base', 'small', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large']:
            if model == "large-v3" and self.lang[:2] not in ["pt", "ca", "eu"]:
                raise ValueError("large-v3 models only available for pt/ca/eu")
            if model == "large":
                if self.lang[:2] in ["pt", "eu"]:
                    model = "large-v3"
                else:
                    model = "large-v2"
            models = mapping[model]
            if self.lang[:2] == "pt":
                model = models[0]
            elif self.lang[:2] == "gl":
                model = models[1]
            elif self.lang[:2] == "ca":
                model = models[1] if model == "large-v3" else models[2]
            elif self.lang[:2] == "es":
                model = models[3]
            elif self.lang[:2] == "eu":
                model = models[-1]
        if not model or model not in FasterWhisperSTT.MODELS + self.MODELS_LARGE_V3 + self.MODELS_LARGE_V2 + \
                self.MODELS_LARGE + self.MODELS_MEDIUM + self.MODELS_SMALL + self.MODELS_BASE + self.MODELS_TINY:
            raise ValueError(f"ZuazoSTT is meant to use pretrained models for {self.available_languages},"
                             f" use FasterWhisper plugin instead if you want to use your own model "
                             f"or a different language")
        self.stt = FasterWhisperSTT(config=config)

    def execute(self, audio, language=None):
        return self.stt.execute(audio, language)

    @classproperty
    def available_languages(cls) -> set:
        return set(cls.LANGUAGES.keys())


if __name__ == "__main__":
    b = FasterWhisperSTT(config={
        "lang": "pt"
    })

    from speech_recognition import Recognizer, AudioFile

    jfk = "/home/miro/Transferências/tpt.wav"
    with AudioFile(jfk) as source:
        audio = Recognizer().record(source)

    a = b.execute(audio, language="pt")
    print(a)
    # And so, my fellow Americans, ask not what your country can do for you. Ask what you can do for your country.
