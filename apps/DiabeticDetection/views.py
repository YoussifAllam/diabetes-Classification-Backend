from pathlib import Path

import numpy as np
from django.conf import settings
from PIL import Image
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .serializers.InputSerializers import DiabeticFootUlcerImageSerializer
from .serializers.OutputSerializers import DiabeticFootUlcerPredictionSerializer

try:
    import tensorflow as tf
except ImportError:  # pragma: no cover
    tf = None

# Same order as TensorFlow image_dataset_from_directory (sorted folder names under Patches/)
CLASS_LABELS = ["Abnormal", "Normal"]

IMAGE_SIZE = (224, 224)


class DiabeticFootUlcerPredictView(APIView):
    """Predict DFU vs healthy skin using the notebook-trained EfficientNet model."""

    parser_classes = (MultiPartParser, FormParser)
    _model = None

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            if tf is None:
                raise RuntimeError(
                    "tensorflow is not installed. Add it to requirements and reinstall."
                )
            model_path = Path(settings.BASE_DIR) / "static" / "model.h5"
            cls._model = tf.keras.models.load_model(
                model_path,
                compile=False,
                safe_mode=False,
            )
        return cls._model

    def post(self, request: Request) -> Response:
        input_serializer = DiabeticFootUlcerImageSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        upload = input_serializer.validated_data["image"]

        image = Image.open(upload).convert("RGB")
        image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        batch = np.asarray(image, dtype=np.float32)
        batch = np.expand_dims(batch, axis=0)

        model = self._get_model()
        raw = model.predict(batch, verbose=0)[0]
        raw = np.asarray(raw, dtype=np.float64)
        exp = np.exp(raw - np.max(raw))
        probs = (exp / exp.sum()).astype(np.float64)
        pred_idx = int(np.argmax(raw))

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
