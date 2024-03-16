import os
import shutil
import uuid

from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.views import View

from .services.audio import extract_audio, join_audio_pieces, split_audio_in_pieces
from .services.translate import translate_audio

available_languages = ["hin", "deu", "spa", "jpn", "fra", "kor"]


class HealthCheck(View):
    def get(self, request):
        return JsonResponse({"message": "SpeechSync at your service"})


class UploadVideoView(View):
    def post(self, request):
        if request.FILES.get("file"):
            file = request.FILES["file"]
            language = request.GET.get("language")
            if not language:
                return JsonResponse({"error": "language is required"}, status=400)
            if language not in available_languages:
                return JsonResponse({"error": "language is incorrect"}, status=400)

            id = str(uuid.uuid4())
            folder_path = os.path.join(settings.TEMP_ROOT, id)
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, "video.mp4")

            with open(file_path, "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            audio_path = extract_audio(file_path)
            pieces = split_audio_in_pieces(audio_path)

            try:
                output_pieces = []
                for audio_piece in pieces:
                    output_piece = translate_audio(audio_piece, language)
                    output_pieces += [output_piece]

                join_audio_pieces(output_pieces)
            except:
                return JsonResponse({"error": "Something wend wrong :("}, status=400)

            return JsonResponse({"error": None, "id": id})
        return JsonResponse({"error": "No file uploaded"}, status=400)


class DownloadVideoView(View):
    def get(self, request):
        id = request.GET.get("id")
        if not id:
            raise Http404("File name parameter 'filename' is missing in the request.")

        folder_path = os.path.join(settings.TEMP_ROOT, id)
        file_path = os.path.join(folder_path, "audio", "translated", "joined_audio.wav")

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_data = f.read()

            response = HttpResponse(file_data, content_type="application/octet-stream")
            response["Content-Disposition"] = "attachment; filename=video.mp4"

            shutil.rmtree(folder_path)

            return response
        return JsonResponse({"error": f"ID {id} not found"}, status=400)
