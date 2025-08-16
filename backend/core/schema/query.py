from core.models import SiteConfiguration
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username",)

class SiteConfigurationType(DjangoObjectType):
    class Meta:
        model = SiteConfiguration
        fields = (
            "id",
            "site_name",
            "address",
            "phone1",
            "phone2",
            "site_logo",
        )
    
class CoreQuery(graphene.ObjectType):

    site_config = graphene.Field(SiteConfigurationType)
    me = graphene.Field(UserType)
    
    def resolve_site_config(self, info):
        if SiteConfiguration.objects.all().count() == 0:
            SiteConfiguration.objects.create()
        return SiteConfiguration.load()
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")
        return user