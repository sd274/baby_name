import graphene
from graphene_django.types import DjangoObjectType, DjangoObjectType
from .name_models.model_server import NameModels, BanditServer

from .models import (
    BabyName,
    UserNameReaction,
    Reaction
)

class BabyNameRecommenationType(graphene.ObjectType):
    recommendation_type = graphene.String()
    sex = graphene.String()
    name = graphene.String()
    id = graphene.Int()

class BabyNameType(DjangoObjectType):
    class Meta:
        model = BabyName

    recommendation_type = graphene.String()


    def resolve_recommendation_type(root, info, **kwargs):
        print(root)
        return 'Testing'



class UserNameReactionType(DjangoObjectType):
    class Meta:
        model = UserNameReaction


class ReactionType(DjangoObjectType):
    class Meta:
        model = Reaction
    
def get_name_rec(user, sex):
    model_server = BanditServer(user, sex)
    return model_server.get_next_name()


class Query(graphene.ObjectType):
    # nameRecommendation = graphene.Field(
    #     BabyNameType,
    #     sex=graphene.String()
    # )
    nameRecommendation = graphene.Field(
        BabyNameRecommenationType,
        sex=graphene.String()
    )
    reactions = graphene.List(ReactionType)
    userReactions = graphene.List(
        UserNameReactionType
    )
    prepModel = graphene.Boolean()

    def resolve_prepModel(self, info, *kwargs):
        user = info.context.user
        model_server = NameModels(user, 'boy')
        model_server.prep_models()
        return {'result': 'Models Prepped'}

    def resolve_reactions(self, info, *kwargs):
        return Reaction.objects.all()

    def resolve_nameRecommendation(self, info, **kwargs):
        sex = kwargs.get('sex')
        user = info.context.user
        if not user.is_authenticated:
            return None
        elif sex in ('boy', 'girl'):
            name_recommendation, model = get_name_rec(user, sex)
            return BabyNameRecommenationType(
                recommendation_type = model,
                sex = sex,
                name = name_recommendation.name,
                id = name_recommendation.id
            )
        return None

    # def resolve_nameRecommendation(self, info, **kwargs):
    #     sex = kwargs.get('sex')
    #     user = info.context.user
    #     if not user.is_authenticated:
    #         return None
    #     elif sex in ('boy', 'girl'):
    #         return get_name_rec(user, sex)
    #     return None

    def resolve_userReactions(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return None
        else:
            reactions = (
                UserNameReaction
                .objects
                .filter(
                    user=info.context.user,
                )
                .all()
            )
            return reactions
        return None


class UserNameReactionInput(graphene.InputObjectType):
    babyName_id = graphene.ID()
    reaction_id = graphene.ID()
    recommendation_type = graphene.String()

class UserNameReactionMutation(graphene.Mutation):
    class Arguments:
        input = UserNameReactionInput(required=True)
    ok = graphene.Boolean()
    userNameReaction = graphene.Field(UserNameReactionType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        babyName_id = input.babyName_id
        reaction_id = input.reaction_id
        recommendation_type = input.recommendation_type
        user = info.context.user
        name = BabyName.objects.get(pk=babyName_id)
        reaction = Reaction.objects.get(pk=reaction_id)
        model_server = BanditServer(user, None)
        model_server.log_result(
            babyName_id,
            name.name,
            reaction.id,
            reaction.reaction,
            recommendation_type
        )
        
        userNameReaction, created = UserNameReaction.objects.get_or_create(
            user=info.context.user,
            name=name,
            reaction=reaction
        )
        return UserNameReactionMutation(
            ok=ok,
            userNameReaction=userNameReaction
        )


class Mutation(graphene.ObjectType):
    user_reaction = UserNameReactionMutation.Field()
