"""
This file contains the base class that we can build our name models from and 
the recommendation runner that will serve the recommendations to
the app.
"""
import random
from ..models import UserNameReaction
import os
import pandas as pd
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
prep_folder = os.path.join(current_dir, 'model_store')
log_folder = os.path.join(current_dir, 'model_logs')


if not os.path.exists(prep_folder):
    os.makedirs(prep_folder)

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

class NameModel:
    def __init__(self, user, sex):
        self.model_name = self.__class__.__name__
        self.user = user
        self.sex = sex
        self.user_reactions = self.get_reactions()
        self.prep_folder = prep_folder
        

    def get_name_recommendation(self):
        return None

    def get_reactions(self):
        if self.user is not None:
            reactions = (
                UserNameReaction
                .objects
                .filter(user=self.user)

            )
            return reactions

    def prep_model(self):
        """
        Some calculations can be done before and saved in a 
        json object that can be imported.
        Returns:
            success (bool): if the model correctly prepared
        """
        return True


class ServeModels:
    def __init__(self, user, sex):
        self.user = user
        self.sex = sex
        self.models, self.default_model = self.set_models()
        self.log_folder = log_folder

    def set_models(self):
        return [], None

    def get_model_to_use(self):
        modelToUse = (
            random
            .choice(self.models)(self.user, self.sex)
        )
        return modelToUse


    def get_next_name(self):
        modelToUse = self.get_model_to_use()
        model_name = modelToUse.model_name
        print('using model {}'.format(modelToUse.model_name))
        rec = modelToUse.get_name_recommendation()
        print(rec)
        if rec is None:
            print('using default model')
            model_instance = self.default_model(self.user, self.sex)
            rec = model_instance.get_name_recommendation()
            model_name = model_instance.model_name
        return rec, model_name

    def prep_models(self):
        print('Prepping models....')
        for model in self.models:
            model_instance = model(user=None, sex=None)
            model_instance.prep_model()

    def log_result(
        self, baby_name_id,
        baby_name, reaction_id,
        reaction, recommendation_type
        ):
        reaction_data = pd.DataFrame([{
            'baby_name_id': baby_name_id,
            'baby_name': baby_name,
            'reaction_id': reaction_id,
            'reaction': reaction,
            'recommendation_type': recommendation_type,
            'user': self.user.id,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        }])
        log_file = os.path.join(
            self.log_folder,
            'reaction_logs.csv'
        )
        with open(log_file, 'a') as f:
            reaction_data.to_csv(
                f,
                mode='a',
                index=False,
                header= not f.tell()
            )

        print(f'Logging: {self.user.id} {recommendation_type}, {reaction}')
