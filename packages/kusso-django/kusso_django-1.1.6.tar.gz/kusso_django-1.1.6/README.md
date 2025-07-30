KU SSO for Django
=================

This is a Django application written to support authentication via KU Single Sign-On (KU SSO) system.

Installation
------------

Use `pip` to install the package from PyPI.

    pip install kusso-django


Edit the project's `settings.py` to include the `kusso_django.kusso` app.

```python
INSTALLED_APPS = [
    :
    'kusso_django.kusso',
]
```

Synchronize the database with the command

    ./manage.py migrate

Edit the project's `urls.py` to include necessary paths.  A different prefix
may be used, but the redirect URI needs to be changed accordingly.

```python
from django.urls import path, include
urlpatterns = [
    :
    path('kusso', include('kusso_django.kusso.urls', namespace='kusso'))
]
```

With the example above, the redirect URI to be requested to the Office of
Computer Services will be:

    https://<host>/<subpath>/kusso/authorize/

Add `KUSSO_CONFIG` to `settings.py` with the client ID and secret given by the
Office of Computer Services.  The `create_new_user` flag indicates whether a
non-existent user will be automatically created upon successful login from KU
SSO.

```python
KUSSO_CONFIG = {
    'client_id': '<client-id>',
    'client_secret': '<client-secret>',
    'create_new_user': <True or False>,
}
```


Login/Logout Template Tags
--------------------------

Assuming the URL namespace is `kusso`, use the `url` template tag to
generate login and logout links:

* Login link
    ```django
    <a href="{% url 'kusso:login' %}?next={{ request.GET.next }}">KU All-Login</a>
    ```
* Logout link
    ```django
    <a href="{% url 'kusso:logout' %}">Logout</a>
    ```

Error Handling
--------------

When an error is encountered during the authentication process, the user will
be sent back to the login page.  A corresponding error message is also sent as
a message via [Django's messages framework](https://docs.djangoproject.com/en/4.1/ref/contrib/messages/).
To make the error message visible to the user, the login template must include
something like:

```django
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```


Deploying App with Reverse Proxy
--------------------------------

To ensure the redirect-uri for KU SSO is constructed correctly when deploying
the project behind a reverse proxy like Nginx, add the following configurations
to the project's `settings.py`.

```python
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```
