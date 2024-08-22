from rest_framework.routers import DefaultRouter, SimpleRouter, BaseRouter, Route


class OwnerViewRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update'
            },
            name='{basename}-retrieve',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/create{trailing_slash}$',
            mapping={
                'post': 'create'
            },
            name='{basename}-create',
            detail=False,
            initkwargs={}
        )
    ]