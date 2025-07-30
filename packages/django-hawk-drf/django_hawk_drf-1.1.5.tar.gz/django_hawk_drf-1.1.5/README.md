# Django Hawk DRF

This package provides [Django Rest Framework](https://github.com/encode/django-rest-framework/) helper classes for use with [Django Hawk](https://github.com/uktrade/django-hawk).

## Installation

Read the [Django Hawk installation](https://github.com/uktrade/django-hawk#installation) documentation.

## Example usage

Read the [Django Hawk example usage](https://github.com/uktrade/django-hawk#example-usage) documentation.

Add the `HawkResponseMiddleware` to the `MIDDLEWARE` setting in your project like so:

```
MIDDLEWARE = [
    ...
    "django_hawk.middleware.HawkResponseMiddleware",
    "django_hawk_drf.middleware.HawkResponseMiddleware",
    ...
]
```

To check the you can use the `django_hawk.authentication.HawkAuthentication` authentication class.

```python
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django_hawk_drf.authentication import HawkAuthentication


class ExampleViewSet(ViewSet):
    authentication_classes = (HawkAuthentication,)
    permission_classes = ()

    def list(self, request):
        return Response([])
```

## Testing

Tests belong in the `/django_hawk_drf/tests/` directory. You can run the tests by installing the requirements like so:


```
make setup
```

Now you can run the tests using the following command:

```
poetry run python manage.py test
```

### Tox tests

We use [tox](https://pypi.org/project/tox/) to test compatibility across different Django versions.

To run these tests with tox, just run the following:

```
make tox
```

## Pushing to PyPI

- [PyPI Package](https://pypi.org/project/django-hawk-drf/)
- [Test PyPI Package](https://test.pypi.org/project/django-hawk-drf/)

Running `make build-package` will build the package into the `dist/` directory
Running `make push-pypi-test` will push the built package to Test PyPI
Running `make push-pypi` will push the built package to PyPI
