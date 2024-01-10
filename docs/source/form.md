# Form Validation

The most common pattern for server-side validation in a Django view consists of:

1. Render the initial form
2. Validate on POST
3. If any validation errors, re-render the form with errors and user input
4. If no validation errors, save to the database (and/or any other actions) and redirect

In order to make this work with Turbo you can do one of two things (**Note**: requires minimum **@hotwired/turbo 7.0.0-beta.3**):

1. When the form is invalid, return with a 4** status response.
2. Add *data-turbo="false"* to your `<form>` tag.

If neither of these options are set, Turbo will throw an error if your view returns any response that isn't a redirect.

Note that if you set *data-turbo="false"* on your form like so:

```html
<form method="post" action="..." data-turbo="false">
```

Turbo will force a full-page refresh, just as the same attribute does to link behavior. This might be acceptable however when working with views and forms e.g. in 3rd party packages where you don't want to change the default workflow.

If you want to continue using forms with Turbo just change the response status to a 4**, e.g. 422:

```python
import http

from django.shortcuts import redirect
from django.template.response import TemplateResponse

from myapp import MyForm

def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # save data etc...
            return redirect("/")
        status = http.HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        form = MyForm()
        status = http.HTTPStatus.OK
    return TemplateResponse(request, "my_form.html", {"form": my_form}, status=status)
```

As this is such a common pattern, we provide for convenience the **turbo_response.render_form_response** shortcut function which automatically sets the correct status depending on the form state (and adds "form" to the template context):

```python
from django.shortcuts import redirect

from turbo_helper import render_form_response

from myapp import MyForm


def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # save data etc...
            return redirect("/")
    else:
        form = MyForm()
    return render_form_response(request, form, "my_form.html")
```

If you are using CBVs, this package has a mixin class, **turbo_response.mixins.TurboFormMixin** that sets the correct status automatically to 422 for an invalid form:

```python
from django.views.generic import FormView

from turbo_helper import redirect_303
from turbo_helper.mixins import TurboFormMixin

from myapp import MyForm


class MyView(TurboFormMixin, FormView):
    template_name = "my_form.html"

    def form_valid(self, form):
        return redirect_303("/")
```

In addition you can just subclass these views for common cases:

- **turbo_response.views.TurboFormView**
- **turbo_response.views.TurboCreateView**
- **turbo_response.views.TurboUpdateView**

In some cases you may wish to return a turbo-stream response containing just the form when the form is invalid instead of a full page visit. In this case just return a stream rendering the form partial in the usual manner. For example:

```python
from django.shortcuts import redirect_303
from django.template.response import TemplateResponse
from django.views.generic import FormView

from turbo_helper import TurboStream

from myapp import MyForm


def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # save data etc...
            return redirect_303("/")
        return TurboStream("form-target").replace.template("_my_form.html").render(request=request)
    else:
        form = MyForm()
    return TemplateResponse(request, "my_form.html", {"form": my_form})
```

Or CBV:

```python
class MyView(TurboFormMixin, FormView):
    template_name = "my_form.html"

    def form_valid(self, form):
        return redirect_303("/")

    def form_invalid(self, form):
        return TurboStream("form-target").replace.template("_my_form.html").render(request=request)
```

And your templates would look like this:

*my_form.html*

```html
{% extends "base.html" %}

{% block content %}
<h1>my form goes here..</h1>
{% include "_my_form.html" %}
{% endblock content %}
```

*_my_form.html*

```html
<form method="POST" id="form-target" action="/my-form">
  {% csrf_token %}
  {{ form.as_p }}
</form>
```

As this is a useful pattern in many situations, for example when handling forms inside modals, this package provides a mixin class **turbo_response.mixins.TurboStreamFormMixin**:

```python
from django.views.generic import FormView
from turbo_helper.mixins import TurboStreamFormMixin


class MyView(TurboStreamFormMixin, FormView):
    turbo_stream_target = "form-target"
    template_name = "my_form.html"
    # action = Action.REPLACE
```

This mixin will automatically add the target name to the template context as *turbo_stream_target*. The partial template will be automatically resolved as the template name prefixed with an underscore: in this example, *_my_form.html*. You can also set it explicitly with the *turbo_stream_template_name* class attribute. The default action is "replace".

As with the form mixin above, the package includes a number of view classes using this mixin:

- **turbo_response.views.TurboStreamFormView**
- **turbo_response.views.TurboStreamCreateView**
- **turbo_response.views.TurboStreamUpdateView**

So the above example could be rewritten as:

```python
from turbo_helper.views import TurboStreamFormView


class MyView(TurboStreamFormView):
    turbo_stream_target = "form-target"
    template_name = "my_form.html"
```

The model-based classes automatically set the target DOM ID based on the model. The pattern for **TurboStreamCreateView** is *form-<model_name>* and for **TurboStreamUpdateView** *form-<model-name>-<pk>*. You can override this by setting the *target* attribute explicitly or overriding the *get_turbo_stream_target* method.

A final point re: forms: Turbo processes forms using the FormData API and only includes inputs with a value. This means all buttons, inputs etc. must have a value. For example suppose you have a button like this:

```html
<button name="send_action">Do this</button>
```

If your view code checks for this value:

```python
if "send_action" in request.POST:
    ...
```

it will consistently fail. You should have something like:

```html
<button name="send_action" value="true">Do this</button>
```

to ensure the FormData object includes the button value.
