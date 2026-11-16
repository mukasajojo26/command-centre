import sys,wave,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
w=wave.open(sys.argv[1]);a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
segs,info=m.transcribe(a,word_timestamps=False,vad_filter=True)
print("lang",info.language,round(info.language_probability,2))
for s in segs: print(f"[{s.start:05.1f}-{s.end:05.1f}] {s.text.strip()}")
