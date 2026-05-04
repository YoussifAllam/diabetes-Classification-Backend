from pathlib import Path
import pickle

import numpy as np
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .serializers.InputSerializers import DiabetesPredictionInputSerializer
from .serializers.OutputSerializers import DiabetesPredictionOutputSerializer


GENDER_ENCODING = {
    "female": 0,
    "male": 1,
    "other": 2,
}

SMOKING_HISTORY_ENCODING = {
    "current": 0,
    "ever": 1,
    "former": 2,
    "never": 3,
    "no info": 4,
    "not current": 5,
}


class DiabetesPredictionView(APIView):
    _model = None

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            model_path = Path(settings.BASE_DIR) / "static" / "best_diabetes_model.pkl"
            with model_path.open("rb") as model_file:
                cls._model = pickle.load(model_file)
        return cls._model

    def post(self, request: Request) -> Response:
        input_serializer = DiabetesPredictionInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        feature_vector = np.array(
            [
                [
                    GENDER_ENCODING[data["gender"]],
                    data["age"],
                    data["hypertension"],
                    data["heart_disease"],
                    SMOKING_HISTORY_ENCODING[data["smoking_history"]],
                    data["bmi"],
                    data["HbA1c_level"],
                    data["blood_glucose_level"],
                ]
            ]
        )

        model = self._get_model()
        prediction = int(model.predict(feature_vector)[0])

        response_data = {
            "prediction": prediction,
            "label": "diabetic" if prediction == 1 else "non-diabetic",
        }

        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(feature_vector)[0][1])
            response_data["probability"] = round(probability, 4)

        output_serializer = DiabetesPredictionOutputSerializer(response_data)
        return Response(output_serializer.data, status=HTTP_200_OK)
