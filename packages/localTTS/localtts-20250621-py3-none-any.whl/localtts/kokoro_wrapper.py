import warnings
warnings.filterwarnings("ignore")

import os
os.environ["PYTHONWARNINGS"] = "ignore"  # 对某些第三方库有效

import json
from datetime import datetime
import soundfile as sf
from kokoro import KPipeline, KModel

class KokoroTTS:
    def __init__(self, model_path: str, config_path: str, voice_path: str, repo_id: str = "xxx", lang_code: str = "a", quiet: bool = True):
        self.quiet = quiet
        self._log("Loading config...")
        with open(config_path) as f:
            config = json.load(f)

        self._log("Initializing model...")
        # print(f"repo id: {repo_id}")
        model = None
        try:
            model = KModel(repo_id='xxx', model=model_path, config=config)
        except Exception as e:
            model = KModel(model=model_path, config=config)
        self._log("Initializing pipeline...")
        
        self.pipeline = None
        try:
            self.pipeline = KPipeline(repo_id='xxx', lang_code=lang_code, model=model)
        except Exception as e:
            self.pipeline = KPipeline(lang_code=lang_code, model=model)
        self._log("Loading voice...")
        self.voice = self.pipeline.load_single_voice(voice_path)
        
        

    def infer(self, text: str, speed: float = 1.0, output_path: str = "output", sample_rate: int = 24000, return_paths: bool = True, split_pattern = None):
        self._log("Starting inference...")
        begin = datetime.now()

        generator = self.pipeline(
            text,
            voice=self.voice,
            speed=speed,
            split_pattern=split_pattern,
        )
        
        file_paths = []
        for i, (graphemes, phonemes, audio) in enumerate(generator):
            filename = output_path if i == 0 else f"{output_path.replace('.wav', '').replace('.WAV', '')}_{i}.wav"
            sf.write(filename, audio, sample_rate)
            file_paths.append(filename)
            self._log(f"[{i}] Saved: {filename}")

        end = datetime.now()
        self._log(f"Inference complete. Time taken: {end - begin}")

        return file_paths if return_paths else None

    def _log(self, msg: str):
        if not self.quiet:
            print(f"[KokoroTTS] {msg}")


if __name__ == "__main__":
    model_path = './temp/kokoro-82M/kokoro-v1_0.pth'
    config_path = './temp/kokoro-82M/config.json'
    voice_path = './temp/kokoro-82M/voices/af_heart.pt'
    output_path = './temp/result.wav'
    from localtts import KokoroTTS as TTS
    tts = TTS(model_path=model_path, config_path=config_path, voice_path=voice_path)

    text = '''
    The sky above the port was the color of television, tuned to a dead channel.
    '''
    
    paths = tts.infer(text, output_path=output_path, return_paths=True)

    print("✅ wav file output：")
    for path in paths:
        print(f"  → {path}")
    