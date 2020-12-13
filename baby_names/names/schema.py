import graphene
from graphene_django.types import DjangoObjectType, DjangoObjectType

from .models import (
    BabyName,
    UserNameReaction,
    Reaction
)


class BabyNameType(DjangoObjectType):
    class Meta:
        model = BabyName


class UserNameReactionType(DjangoObjectType):
    class Meta:
        model = UserNameReaction


class ReactionType(DjangoObjectType):
    class Meta:
        model = Reaction


def get_name_rec(user, sex):
    user_reactions = (
        UserNameReaction
        .objects
        .filter(user=user)

    )
    qs = (
        BabyName
        .objects
        .filter(sex=sex)
        .exclude(
            baby_name_reaction__in=user_reactions
        )
        .order_by('?')
    )
    return qs.first()


class Query(graphene.ObjectType):
    nameRecommendation = graphene.Field(BabyNameType, sex=graphene.String())
    reactions = graphene.List(ReactionType)
    userReactions = graphene.List(
        UserNameReactionType, reaction_id=graphene.Int()
    )

    def resolve_reactions(self, info, *kwargs):
        return Reaction.objects.all()

    def resolve_nameRecommendation(self, info, **kwargs):
        sex = kwargs.get('sex')
        user = info.context.user
        if not user.is_authenticated:
            return None
        elif sex in ('boy', 'girl'):
            return get_name_rec(user, sex)
        return None

    def resolve_userReactions(self, info, **kwargs):
        reaction_id = kwargs.get('reaction_id')
        if not info.context.user.is_authenticated:
            return None
        else:
            reation = Reaction.objects.get(pk=reaction_id)
            reactions = (
                UserNameReaction
                .objects
                .filter(
                    user=info.context.user,
                    reaction=reation
                )
                .all()
            )
            return reactions
        return None


class UserNameReactionInput(graphene.InputObjectType):
    babyName_id = graphene.ID()
    reaction_id = graphene.ID()

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
        name = BabyName.objects.get(pk=babyName_id)
        reaction = Reaction.objects.get(pk=reaction_id)
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
