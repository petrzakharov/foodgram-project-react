from rest_framework import mixins, viewsets


class CustomListRetrieveMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass
