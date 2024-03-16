import os

import scipy.io.wavfile
import torch
import torchaudio
from transformers import AutoProcessor, SeamlessM4Tv2Model

device = torch.device("cuda")
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large").to(device)


def translate_audio(audio_path, lang):
    print("Translating : ", audio_path)

    folder_path = os.path.dirname(audio_path)
    folder_path = os.path.join(folder_path, "translated")
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.basename(audio_path)
    output_path = os.path.join(folder_path, filename)

    # Load and resample your audio
    audio, orig_freq = torchaudio.load(audio_path)
    audio = torchaudio.functional.resample(audio, orig_freq=orig_freq, new_freq=16_000)

    # Process your audio and move the tensors to the device
    audio_inputs = processor(audios=audio, src_lang="eng", return_tensors="pt")
    audio_inputs = {k: v.to(device) for k, v in audio_inputs.items()}

    audio_array_from_audio = (
        model.generate(**audio_inputs, tgt_lang=lang)[0].cpu().numpy().squeeze()
    )

    # Save the output
    sample_rate = 16000
    scipy.io.wavfile.write(output_path, rate=sample_rate, data=audio_array_from_audio)

    return output_path
