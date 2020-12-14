"""
This file contains the base class that we can build our name models from and 
the recommendation runner that will serve the recommendations to
the app.
"""
import random
from ..models import UserNameReaction
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
prep_folder = os.path.join(current_dir, 'model_store')

if not os.path.exists(prep_folder):
    os.makedirs(prep_folder)

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

    def set_models(self):
        return [], None

    def get_next_name(self):
        modelToUse = random.choice(self.models)(self.user, self.sex)
        print('using model {}'.format(modelToUse.model_name))
        rec = modelToUse.get_name_recommendation()
        print(rec)
        if rec is None:
            print('using default model')
            rec = self.default_model(self.user, self.sex).get_name_recommendation()
        return rec

    def prep_models(self):
        for model in models:
            model_instance = model(user=None, sex=None)
            model_instance.prep_model()
