from .rec_models import (
    SameFirstLetterModel,
    ClusterNames,
    RandomRecommendationModel
)
from .base import ServeModels


class NameModels(ServeModels):

    def set_models(self):
        return [
            RandomRecommendationModel,
            SameFirstLetterModel,
            # ClusterNames,
        ], RandomRecommendationModel
