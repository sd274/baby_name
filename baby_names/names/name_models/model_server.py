from .rec_models import (
    SameFirstLetterModel,
    ClusterNames,
    RandomRecommendationModel,
    NameOrigin
)
from .base import ServeModels
import pandas as pd
import os
import random
import numpy as np
class NameModels(ServeModels):

    def set_models(self):
        return [
            # RandomRecommendationModel,
            # SameFirstLetterModel,
            # ClusterNames,
            NameOrigin,
        ], RandomRecommendationModel


class BanditServer(NameModels):

    def get_model_to_use(self):
        model_names = [a.__name__ for a in self.models]
        print(model_names)
        user_id = self.user.id
        log_file = os.path.join(self.log_folder, 'reaction_logs.csv')
        log_data = pd.read_csv(log_file).query('user == @user_id')
        log_data['success'] = np.where(
            log_data.reaction.isin(['maybe', 'yes']),
            1,
            0
        )
        log_data['total'] = 1
        log_data = (
            log_data
            .groupby(['recommendation_type'])
            .agg({'total':'sum', 'success':'sum'})
            .to_dict(orient='index')
        )
        a = [log_data.get(model, {'total':1})['total']  for model in model_names]
        b = [log_data.get(model, {'success':1})['success']  for model in model_names]
        theta = np.random.beta(a, b)
        next_model = self.models[np.argmax(theta)]
        print(f'bandit choice: {next_model}')


        return next_model(self.user, self.sex)

