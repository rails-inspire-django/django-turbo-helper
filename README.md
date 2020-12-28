## Introduction

This package offers helpers for server-side rendering of hotwire-turbo streams and frames.

## Requirements

## Getting Started

Note: This library does not include any client libraries (Turbo or Stimulus). You may wish to add these yourself using your preferred Javascript build tool, or use a CDN. Please refer to the Hotwire documentation on installing these libraries.

## Middleware

You can optionally install *turbo_response.middleware.TurboStreamMiddleware*. This adds the attribute *accept_turbo_stream* to your request:


```
MIDDLEWARE = [
    ...
    "turbo_response.middleware.TurboStreamMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
]
```

This is useful if you want to check if a stream is requested, so you can optionally return a stream or a normal response:

```
if request.accept_turbo_stream:
    return TurboStreamResponse(action="remove", target="item")
else:
    return redirect("index")
```

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
    model = Todo
    form_class = TodoForm
    template_name = "todos/todo_form.html"
    turbo_stream_template_name = "todos/_todo_form.html"
    turbo_stream_target = "todo-form"

create_todo_view = CreateTodoView.as_view()
```

This class automatically adopts the convention of using the underscore prefix for any partials, so you could save a couple lines of code and just write:

```
class CreateTodoView(TurboStreamCreateView):
    model = Todo
    form_class = TodoForm
    turbo_stream_target = "todo-form"
```
and the turbo stream template will automatically resolve to *todos/_todo_form.html* (the *CreateView* of course resolves the default template names as well, based on the model metadata).

## Response classes

## Mixins

## Responding with Multiple Streams

Suppose you want to return **multiple** Turbo Streams in a single view. For example, let's say you are building a shopping cart for an e-commerce site.  The shopping cart is presented as a list of items, and you can edit the amount in each and click a "Save" icon next to that amount. When the amount is changed, you want to recalculate the total cost of all the items, and show this total at the bottom of the cart. In addition, there is a little counter on the top navbar which shows the same total across the whole site.

To do this you can use *django.http.StreamingHttpResponse* with a generator. The generator should yield each individual turbo-stream string. To ensure the correct content type is used, this package provides a subclass, *turbo_response.TurboStreamStreamingResponse*.

Taking the example above, we have a page with the shopping cart, that has this snippet:


```
<span id="cart-summary-total">{{ total_amount }}</span>
```

and in the navbar of our base template:

```
<span id="nav-cart-total">{{ total_amount }}</span>
```

In both cases the total amount is precalculated in the initial page load, for example using a context processor.

Each item in the cart has an inline edit form that might look like this:

```
<td>
    <form method="post" action="{% url 'update_cart_item' item.id %}">
        {% csrf_token %}
        <input type="text" name="amount" value="{{ item.value }}">
        <button type="submit">Save</button>
    </form>
</td>
```

```
from turbo_response import TurboStreamStreamingResponse, render_turbo_stream

def update_cart_item(request, item_id):
    # item saved to e.g. session or db
    save_cart_item(request, item_id)

    # for brevity, assume "total amount" is returned here as a
    # correctly formatted string in the correct local currency
    total_amount = calc_total_cart_amount(request)

    def render_response():
        yield render_turbo_stream(
            total_amount,
            action="replace",
            target="nav-cart-total"
            )

        yield render_turbo_stream(
            total_amount,
            action="replace",
            target="cart-summary-total"
            )
    return TurboStreamStreamingResponse(render_response())
```

That's it! Note that here we are returning a very simple string value, so we don't need to wrap the responses in templates. If you want to do so, use *turbo_response.render_stream_template* instead.


## Using Turbo Frames

## Handling Lazy Turbo Frames

Turbo Frames have a useful feature that allows lazy loading [link to docs]. This is very easy to handle with Django. For example, our e-commerce site includes a list of recommendations at the bottom of some pages based on the customer's prior purchases. We calculate this list using our secret-sauce machine-learning algorithm. Although the results are cached for that user, the initial run can be a bit slow, and we don't want to slow down the rest of the page when the recommendations are recalculated.

This is a good use case for a lazy turbo frame. Our template looks like this, with a fancy loading gif as a placeholder:

```
<turbo-frame id="recommendations" src="{% url 'recommendations' %}">
    <img src="{% static 'fancy-loader.gif' %}">
</turbo-frame>
```

And our corresponding view:

```
def recommendations(request):
    # lazily build recommendations from algorithm and cache result
    recommended_items = get_recommendations_from_cache(request.user)
    return TurboFrameTemplateResponse(
        request,
        "_recommendations.html",
        {"items": recommended_items},
        dom_id="recommendations",
    )
```

The template returned is just a plain Django template. The response class automatically wraps the correct tags, so we don't need to include `<turbo-frame>`.


```
<div class="recommendations">
    {% for item in items %}
    <h3><a href="{{ item.get_absolute_url }}">{{ item.title }}</a></h3>
    {% endfor %}
</div>
```

## Channels

This library can also be used with django-channels Consumers. The helper functions *render_turbo_stream* and *render_turbo_stream_template* when broadcasting streams:

```
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def chat_message(self, event):

        message = await self.get_message(event["message"]["id"])
        num_unread_messages = await self.get_num_unread_messages()

        if message:
            await self.send(
                render_turbo_stream(
                    str(num_unread_messages),
                    action="replace",
                    target="unread_message_counter"
                )

            await self.send(
                render_turbo_stream_template(
                    "chat/_message.html",
                    {"message": message, "user": self.scope['user']},
                    action="append",
                    target="messages",
                )
            )
```

See the django-channels documentation for more details on setting up ASGI and channels. Note that you will need to set up your WebSockets in the client, for example in a Stimulus controller:

```
import { Controller } from 'stimulus';
import { connectStreamSource, disconnectStreamSource } from '@hotwired/turbo';

export default class extends Controller {
  static values = {
    socketUrl: String,
  };

  connect() {
    this.source = new WebSocket(this.socketUrlValue);
    connectStreamSource(this.source);
  }

  disconnect() {
    disconnectStreamSource(this.source);
    this.source = null;
  }
}
```

## Links



