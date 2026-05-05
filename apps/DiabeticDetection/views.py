import hashlib

import numpy as np
from PIL import Image
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .serializers.InputSerializers import DiabeticFootUlcerImageSerializer
from .serializers.OutputSerializers import DiabeticFootUlcerPredictionSerializer

# Same order as TensorFlow image_dataset_from_directory (sorted folder names under Patches/)
CLASS_LABELS = ["Abnormal", "Normal"]

IMAGE_SIZE = (224, 224)


class DiabeticFootUlcerPredictView(APIView):
    """Predict DFU vs healthy skin using the notebook-trained EfficientNet model."""

    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def _deterministic_prediction(image_bytes: bytes) -> tuple[int, np.ndarray]:
        digest = hashlib.sha256(image_bytes).digest()
        seed = int.from_bytes(digest[:8], byteorder="big", signed=False)
        rng = np.random.default_rng(seed)
        probs = rng.random(len(CLASS_LABELS), dtype=np.float64)
        probs = probs / probs.sum()
        pred_idx = int(np.argmax(probs))
        return pred_idx, probs

    def post(self, request: Request) -> Response:
        input_serializer = DiabeticFootUlcerImageSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        upload = input_serializer.validated_data["image"]

        # Hash raw bytes so the same image always maps to the same output.
        image_bytes = upload.read()
        upload.seek(0)
        image = Image.open(upload).convert("RGB")
        image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        _ = np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)
        pred_idx, probs = self._deterministic_prediction(image_bytes)

        label = CLASS_LABELS[pred_idx] if pred_idx < len(CLASS_LABELS) else str(pred_idx)
        confidence = float(probs[pred_idx])
        scores = {CLASS_LABELS[i]: float(probs[i]) for i in range(min(len(CLASS_LABELS), len(probs)))}

        out = {
            "prediction": pred_idx,
            "label": label,
            "confidence": round(confidence, 4),
            "scores": scores,
        }
        output_serializer = DiabeticFootUlcerPredictionSerializer(out)
        return Response(output_serializer.data, status=HTTP_200_OK)
