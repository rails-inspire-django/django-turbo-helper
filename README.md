## Introduction

This package offers helpers for server-side rendering of hotwire-turbo streams and frames.

## Requirements

## Getting Started

Note: This library does not include any client libraries (Turbo or Stimulus). You may wish to add these yourself using your preferred Javascript build tool, or use a CDN. Please refer to the Hotwire documentation on installing these libraries.

## Middleware

## Form Validation

The most common pattern for server-side validation in a Django view consists of:

1. Render the initial form
2. Validate on POST
3. If any validation errors, re-render the form with errors and user input
4. If no validation errors, save to the database (and/or any other actions) and redirect

This pattern however does not work with @hotwire-turbo. If you return HTML from a form post, a Javascript error will be thrown by the Turbo Drive library as it only accepts a redirect. Furthermore, you cannot exempt a form with the *data-turbo="false"* attribute as you can with links. Both of these issues, as of writing, are being addressed by the Hotwire team and should be fixed in a future release. In the meantime, the acceptable approach for "traditional" form validation is:

1. Render the initial form. The form, or surrounding tag, must have an "id".
2. Validate on POST as usual
3. If any validation errors, pass back an HTML fragment containing the errors and user input in a Turbo Stream response with a target matching the HTML id and a "replace" or "update" action.
4. If no validation errors, save and redirect as usual.

As an example, let's take a typical function-based view (FBV):

```
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from myapp.todos.forms import TodoForm

@login_required
def create_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
    else:
        form = TodoForm()

    return TemplateResponse(request, "todos/todo_form.html", {"form": form})
```

Our template *todos/todo_form.html* looks something like this:

```
{% extends "base.html" %}
{% block content %}
<h1>Add your todo here!</h1>
<form method="post" action="{% url 'todos:create_todo' %}">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>
{% endblock content %}
```

To make this work with Turbo, you would have to make these changes:

```
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from turbo_response import TurboStreamTemplateResponse

from myapp.todos.forms import TodoForm

@login_required
def create_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
        # return the invalid form in a stream
        return TurboStreamTemplateResponse(
            request,
            "todos/_todo_form.html",
            {
                "form": form,
            },
            action="replace",
            target="todo-form",
          )

    else:
        form = TodoForm()
    return TemplateResponse(request, "todos/todo_form.html", {"form": form})
```

We break up our *todo_form.html* template, extracting the HTML into a partial include containing the form. A common convention is to use an initial underscore to distinguish partial templates but you can use any naming scheme you wish:

*todos/todo_form.html*

```
{% extends "base.html" %}
{% block content %}
<h1>Add your todo here!</h1>
{% include "todos/_todo_form.html" %}
{% endblock content %}
```

*todos/_todo_form.html*

```
<form method="post" action="{% url 'todos:create_todo' %}" id="todo-form">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>
```

Notice the ID on the form tag. In addition, the template must render with a single top-level tag.

If the form contains errors, the response should look something like this:

```
<turbo-stream action="replace" target="todo-form">
  <template>
    <form method="post" ...>
    form body with error messages goes here...
    </form>
  </template>
</turbo-stream>
```

If you prefer class-based views (CBVs) you can do the same with the *TurboStreamFormMixin*:

```
from django.contrib.auth.mixins import LoginRequired
from django.views.generic.edit import CreateView

from turbo_response.mixins import TurboStreamFormMixin

from myapp.todos.forms import TodoForm
from myapp.todos.models import Todo


class CreateTodoView(TurboStreamFormMixin, CreateView):
    template_name = "todos/todo_form.html"
    turbo_stream_template_name = "todos/_todo_form.html"
    turbo_stream_target = "todo-form"

create_todo_view = CreateTodoView.as_view()
```

Note that the default target for this mixin is "replace", so you don't need to set it here.

To save typing you can just use *TurboStreamCreateView*:

```
from django.contrib.auth.mixins import LoginRequired
from django.views.generic.edit import CreateView

from turbo_response.views import TurboStreamCreateView

from myapp.todos.forms import TodoForm
from myapp.todos.models import Todo

class CreateTodoView(TurboStreamCreateView):
    template_name = "todos/todo_form.html"
    turbo_stream_template_name = "todos/_todo_form.html"
    turbo_stream_target = "todo-form"

create_todo_view = CreateTodoView.as_view()
```


## Response classes

## Mixins

## Responding with Multiple Channels

## Using Turbo Frames

## Handling Lazy Turbo Frames

## Channels

This library can also be used with django-channels Consumers. In particular, you can use the helper functions *render_turbo_stream* and *render_turbo_stream_template* when broadcasting streams:

## Links




