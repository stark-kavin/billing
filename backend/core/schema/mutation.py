from core.models import SiteConfiguration
import graphene
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from core.schema.query import SiteConfigurationType

class UpdateSiteConfiguration(graphene.Mutation):
    class Arguments:
        site_name = graphene.String(required=False)
        address = graphene.String(required=False)
        phone1 = graphene.String(required=False)
        phone2 = graphene.String(required=False)
        site_logo = Upload(required=False)

    site_config = graphene.Field(SiteConfigurationType)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        # Load the singleton instance
        site_config = SiteConfiguration.load()

        # Handle file upload separately
        site_logo = kwargs.pop('site_logo', None)
        
        # Update regular fields
        for field, value in kwargs.items():
            setattr(site_config, field, value)

        # Handle file upload if provided
        if site_logo is not None:
            site_config.site_logo.save(site_logo.name, site_logo, save=False)

        site_config.full_clean()  # runs validators
        site_config.save()

        return UpdateSiteConfiguration(site_config=site_config)