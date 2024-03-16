from services.audio import extract_audio, join_audio_pieces, split_audio_in_pieces
from services.translate import translate_audio

audio_path = extract_audio("data/english_video.mp4")
pieces = split_audio_in_pieces(audio_path)

output_pieces = []
for audio_piece in pieces:
    output_piece = translate_audio(audio_piece, "hin")
    output_pieces += [output_piece]

output_path = join_audio_pieces(output_pieces)
print(output_path)
