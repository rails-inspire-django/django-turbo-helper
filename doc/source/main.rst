This package provides helpers for server-side rendering of `Hotwired/Turbo <https://turbo.hotwire.dev/>`_ streams and frames.

**Disclaimer**: the Hotwired/Turbo client libraries are, at time of writing, still in Beta. We expect there will be breaking changes until the first stable release. This package, and the Turbo client, should therefore be used with caution in a production environment. The version used in testing is *@hotwired/turbo==7.0.0-beta.1*.

============
Requirements
============

This library is tested for Python 3.8+.

===============
Getting Started
===============

``pip install django-turbo-response``

To install from Git:

``git clone https://github.com/danjac/django-turbo-response``

``cd django-turbo-response``

``python setup.py install``

**Note**: This library does not include any client libraries (Turbo or Stimulus). You may wish to add these yourself using your preferred Javascript build tool, or use a CDN. Please refer to the Hotwire documentation on installing these libraries.

==========
Middleware
==========

You can optionally install **turbo_response.middleware.TurboStreamMiddleware**. This adds the attribute *accept_turbo_stream* to your request if the Turbo client adds *Accept: text/html; turbo-stream;* to the header:


.. code-block:: python

  MIDDLEWARE = [
      ...
      "turbo_response.middleware.TurboStreamMiddleware",
      "django.middleware.common.CommonMiddleware",
      ...
  ]


This is useful if you want to check if a stream is requested, so you can optionally return a stream or a normal response:

.. code-block:: python

  if request.accept_turbo_stream:
      return TurboStreamResponse(action=Action.REPLACE, target="item")
  else:
      return redirect("index")

===============
Form Validation
===============

The most common pattern for server-side validation in a Django view consists of:

1. Render the initial form
2. Validate on POST
3. If any validation errors, re-render the form with errors and user input
4. If no validation errors, save to the database (and/or any other actions) and redirect

This pattern however does not work with Turbo. If you return HTML from a form post, a Javascript error will be thrown by the Turbo Drive library as it only accepts a redirect. Furthermore, you cannot exempt a form with the *data-turbo="false"* attribute as you can with links. Both of these issues, as of writing, are being addressed by the Hotwire team and should be fixed in a future release. In the meantime, the acceptable approach for "traditional" form validation is:

1. Render the initial form. The form, or surrounding tag, must have an "id".
2. Validate on POST as usual
3. If any validation errors, pass back an HTML fragment containing the errors and user input in a Turbo Stream response with a target matching the HTML id and a "replace" or "update" action.
4. If no validation errors, save and redirect as usual.

As an example, let's take a typical function-based view (FBV):

.. code-block:: python

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

Our template *todos/todo_form.html* looks something like this:

.. code-block:: html

  {% extends "base.html" %}
  {% block content %}
  <h1>Add your todo here!</h1>
  <form method="post" action="{% url 'todos:create_todo' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
  </form>
  {% endblock content %}

To make this work with Turbo, you would have to make these changes:

.. code-block:: python

  from django.contrib.auth.decorators import login_required
  from django.template.response import TemplateResponse

  from turbo_response import Action, TurboStreamTemplateResponse

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
              action=Action.REPLACE,
              target="todo-form",
            )

      else:
          form = TodoForm()
      return TemplateResponse(request, "todos/todo_form.html", {"form": form})


We break up our *todo_form.html* template, extracting the HTML into a partial include containing the form. A common convention is to use an initial underscore to distinguish partial templates but you can use any naming scheme you wish:

*todos/todo_form.html*

.. code-block:: html

  {% extends "base.html" %}
  {% block content %}
  <h1>Add your todo here!</h1>
  {% include "todos/_todo_form.html" %}
  {% endblock content %}

*todos/_todo_form.html*

.. code-block:: html

  <form method="post" action="{% url 'todos:create_todo' %}" id="todo-form">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
  </form>

Notice the ID on the form tag. In addition, the template must render with a single top-level tag.

If the form contains errors, the response should look something like this:

.. code-block:: html

  <turbo-stream action="replace" target="todo-form">
    <template>
      <form method="post" ...>
      form body with error messages goes here...
      </form>
    </template>
  </turbo-stream>

If you prefer class-based views (CBVs) you can do the same with the **TurboStreamFormMixin** class:

.. code-block:: python

  from django.contrib.auth.mixins import LoginRequiredMixin
  from django.views.generic.edit import CreateView

  from turbo_response.mixins import TurboStreamFormMixin

  from myapp.todos.forms import TodoForm
  from myapp.todos.models import Todo


  class CreateTodoView(TurboStreamFormMixin, LoginRequiredMixin, CreateView):
      template_name = "todos/todo_form.html"
      turbo_stream_template_name = "todos/_todo_form.html"
      turbo_stream_target = "todo-form"

  create_todo_view = CreateTodoView.as_view()

Note that the default action for this mixin is "replace", so you don't need to set it here.

To save typing you can just use **TurboStreamCreateView**:


.. code-block:: python

  from django.contrib.auth.mixins import LoginRequiredMixin
  from django.views.generic.edit import CreateView

  from turbo_response.views import TurboStreamCreateView

  from myapp.todos.forms import TodoForm
  from myapp.todos.models import Todo

  class CreateTodoView(LoginRequiredMixin, TurboStreamCreateView):
      model = Todo
      form_class = TodoForm
      template_name = "todos/todo_form.html"
      turbo_stream_template_name = "todos/_todo_form.html"
      turbo_stream_target = "todo-form"

  create_todo_view = CreateTodoView.as_view()

This class automatically adopts the convention of using the underscore prefix for any partials, so you could save a couple lines of code and just write:

.. code-block:: python

  class CreateTodoView(LoginRequiredMixin, TurboStreamCreateView):
      model = Todo
      form_class = TodoForm

and the turbo stream template will automatically resolve to *todos/_todo_form.html* (the *CreateView* of course resolves the default template names as well, based on the model metadata). The turbo-stream target is auto-generated based on the model meta info: in this case *myapp-todo-form*. If we use **TurboStreamUpdateView** then it will be *myapp-todo-<todo_id>-form*. If you don't want your DOM IDs autogenerated, just set **turbo_stream_target** explictly in your view, or override **get_turbo_stream_target()**. The target is passed to all templates as the variable *turbo_stream_target*, so you can use that in your form markup to keep things consistent:

.. code-block:: html

  <turbo-stream action="replace" target="{{ turbo_stream_target }}">
    <template>
      <form method="post" ...>
      form body with error messages goes here...
      </form>
    </template>
  </turbo-stream>

================================
Responding with Multiple Streams
================================

Suppose you want to return **multiple** Turbo Streams in a single view. For example, let's say you are building a shopping cart for an e-commerce site.  The shopping cart is presented as a list of items, and you can edit the amount in each and click a "Save" icon next to that amount. When the amount is changed, you want to recalculate the total cost of all the items, and show this total at the bottom of the cart. In addition, there is a little counter on the top navbar which shows the same total across the whole site.

To do this you can use *django.http.StreamingHttpResponse* with a generator. The generator should yield each individual turbo-stream string. To ensure the correct content type is used, this package provides a subclass, **turbo_response.TurboStreamStreamingResponse**.

Taking the example above, we have a page with the shopping cart, that has this snippet:


.. code-block:: html

  <span id="cart-summary-total">{{ total_amount }}</span>

and in the navbar of our base template:

.. code-block:: html

  <span id="nav-cart-total">{{ total_amount }}</span>

In both cases the total amount is precalculated in the initial page load, for example using a context processor.

Each item in the cart has an inline edit form that might look like this:

.. code-block:: html

  <td>
      <form method="post" action="{% url 'update_cart_item' item.id %}">
          {% csrf_token %}
          <input type="text" name="amount" value="{{ item.value }}">
          <button type="submit">Save</button>
      </form>
  </td>

.. code-block:: python

  from turbo_response import Action, TurboStreamStreamingResponse, render_turbo_stream

  def update_cart_item(request, item_id):
      # item saved to e.g. session or db
      save_cart_item(request, item_id)

      # for brevity, assume "total amount" is returned here as a
      # correctly formatted string in the correct local currency
      total_amount = calc_total_cart_amount(request)

      def render_response():
          yield render_turbo_stream(
              total_amount,
              action=Action.REPLACE,
              target="nav-cart-total"
              )

          yield render_turbo_stream(
              total_amount,
              action=Action.REPLACE,
              target="cart-summary-total"
              )
      return TurboStreamStreamingResponse(render_response())

That's it! In this example are returning a very simple string value, so we don't need to wrap the responses in templates. If you want to do so, use **turbo_response.render_stream_template** instead.

Note that this technique is something of an anti-pattern; if you have to update multiple parts of a page, a full refresh (i.e. a normal Turbo visit) is probably a better idea. It's useful though in some edge cases where you need to avoid this.

==================
Using Turbo Frames
==================

Rendering Turbo Frames is straightforward. Let's say you have a "Subscribe" button in your page. When the button is clicked, you want the "Subscribe" label to be changed to "Unsubscribe"; when the button is clicked again it should turn back to "Subscribe."

Our template looks something like this:

.. code-block:: html

  {% extends "base.html" %}
  {% block content %}
  <h1>Welcome to my blog</h1>
  {{ blog.description }}
  {% if user.is_authenticated %}
  <turbo-frame id="subscribe">
    {% include "_subscribe.html" %}
  </turbo-frame>
  {% endif %}
  {% endblock %}

Note that we surround the partial template with the *<turbo-frame>* tags. These will be replaced by Turbo when a Turbo Frame response matching the DOM ID "subscribe" is returned from the server.

Our partial template, *_subscribe.html* looks like this:

.. code-block:: html

  <form method="post" action="{% url 'toggle_subscribe' blog.id %}">
    {% csrf_token %}
    <button>{{ is_subscribed|yesno:"Unsubscribe,Subscribe" }}</button>
  </form>

Note that the button uses a POST form to handle the toggle. As it's a POST we also need to include the CSRF token, or we'll get a 403 error.


Here are the views:

.. code-block:: python

  from django.contrib.auth.decorators import login_required
  from django.template.response import TemplateResponse
  from django.shortcuts import get_object_or_404

  from turbo_response import TurboFrameResponse

  from myapp.blogs.models import Blog

  def blog_detail(request, blog_id):
      blog = get_object_or_404(Blog, pk=blog_id)
      is_subscribed = blog.is_subscribed(request.user)
      return TemplateResponse(
          request,
          "blogs/detail.html",
          {"blog": blog, "is_subscribed": is_subscribed}
      )

  @login_required
  def subscribe(request, blog_id):
      blog = get_object_or_404(Blog, pk=blog_id)
      is_subscribed = blog.toggle_subscribe(request.user)
      return TurboFrameResponse(
           request,
          "blogs/_subscribe.html",
          {"blog": blog, "is_subscribed": is_subscribed},
          dom_id="subscribe",
      )

The *subscribe* view returns a response wrapped in the *<turbo-frame>* tag with the DOM id "subscribe". Turbo will look for a corresponding frame in the HTML body with the matching ID, and replace the frame with the one returned from the server. Unlike a full Turbo visit, we don't need to return the entire body - just the snippet we want to update.

If we wanted to use CBVs instead:

.. code-block:: python

  from django.contrib.auth.mixins import LoginRequiredMixin
  from django.views.generic.detail import DetailView, SingleObjectMixin

  from turbo_response.views import TurboFrameTemplateView

  from myapp.blogs.models import Blog

  class BlogDetail(DetailView):
      model = Blog
      template_name = "blogs/detail.html"

      def get_context_data(self, **context):
          return {
              **context,
              "is_subscribed": blog.is_subscribed(request.user)
          }

  class Subscribe(LoginRequiredMixin,
                  SingleObjectMixin,
                  TurboFrameTemplateView):

    turbo_frame_dom_id = "subscribe"
    template_name = "blogs/_subscribe.html"

    def post(request, pk):
        blog = self.get_object()
        is_subscribed = blog.toggle_subscribe(request.user)

        return self.render_to_response(
            {"blog": blog, "is_subscribed": is_subscribed},
        )


==========================
Handling Lazy Turbo Frames
==========================

Turbo Frames have a useful feature that allows `lazy loading <https://turbo.hotwire.dev/handbook/frames>`_. This is very easy to handle with Django. For example, our e-commerce site includes a list of recommendations at the bottom of some pages based on the customer's prior purchases. We calculate this list using our secret-sauce machine-learning algorithm. Although the results are cached for that user, the initial run can be a bit slow, and we don't want to slow down the rest of the page when the recommendations are recalculated.

This is a good use case for a lazy turbo frame. Our template looks like this, with a fancy loading gif as a placeholder:

.. code-block:: html

  <turbo-frame id="recommendations" src="{% url 'recommendations' %}">
      <img src="{% static 'fancy-loader.gif' %}">
  </turbo-frame>

And our corresponding view:

.. code-block:: python

  def recommendations(request):
      # lazily build recommendations from algorithm and cache result
      recommended_items = get_recommendations_from_cache(request.user)
      return TurboFrameTemplateResponse(
          request,
          "_recommendations.html",
          {"items": recommended_items},
          dom_id="recommendations",
      )

The template returned is just a plain Django template. The response class automatically wraps the correct tags, so we don't need to include `<turbo-frame>`.


.. code-block:: html

  <div class="recommendations">
      {% for item in items %}
      <h3><a href="{{ item.get_absolute_url }}">{{ item.title }}</a></h3>
      {% endfor %}
  </div>

========
Channels
========

This library can also be used with `django-channels <https://channels.readthedocs.io/en/stable/>`_ Consumers with the helper functions **render_turbo_stream** and **render_turbo_stream_template** when broadcasting streams:

.. code-block:: python

  from turbo_response import render_turbo_stream, render_turbo_stream_template
  from channels.generic.websocket import AsyncJsonWebsocketConsumer

  class ChatConsumer(AsyncJsonWebsocketConsumer):

      async def chat_message(self, event):

          # DB methods omitted for brevity
          message = await self.get_message(event["message"]["id"])
          num_unread_messages = await self.get_num_unread_messages()

          if message:
              await self.send(
                  render_turbo_stream(
                      str(num_unread_messages),
                      action=Action.REPLACE,
                      target="unread_message_counter"
                  )

              await self.send(
                  render_turbo_stream_template(
                      "chat/_message.html",
                      {"message": message, "user": self.scope['user']},
                      action=Action.APPEND,
                      target="messages",
                  )
              )

See the django-channels documentation for more details on setting up ASGI and channels. Note that you will need to set up your WebSockets in the client, for example in a Stimulus controller:

.. code-block:: javascript

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

=====
Links
=====

Hotwired: https://turbo.hotwire.dev/

=======
License
=======

This project is covered by the MIT license.
