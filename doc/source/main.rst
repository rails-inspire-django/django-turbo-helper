This package provides helpers for server-side rendering of `Hotwired/Turbo <https://turbo.hotwire.dev/>`_ streams and frames.

**Disclaimer**: the Hotwired/Turbo client libraries are, at time of writing, still in Beta. We expect there will be breaking changes until the first stable release. This package, and the Turbo client, should therefore be used with caution in a production environment. The version used in testing is *@hotwired/turbo==7.0.0-beta.3*.

============
Requirements
============

This library is tested for Python 3.8+.

===============
Getting Started
===============

``pip install django-turbo-response``

To install from Git:

``git clone https://github.com/hotwire-django/django-turbo-response``

``cd django-turbo-response``

``python setup.py install``

**Note**: This install does not include any client libraries (Turbo or Stimulus). You may wish to add these yourself using your preferred Javascript build tool, or use a CDN. Please refer to the Hotwire documentation on installing these libraries.

==========
Middleware
==========

You can optionally install **turbo_response.middleware.TurboMiddleware**. This adds the attribute *turbo* to your request if the Turbo client adds *Accept: text/vnd.turbo-stream.html;* to the header:


.. code-block:: python

  MIDDLEWARE = [
      ...
      "turbo_response.middleware.TurboMiddleware",
      "django.middleware.common.CommonMiddleware",
      ...
  ]


This is useful if you want to check if a stream is requested, so you can optionally return a stream or a normal response:

.. code-block:: python

  from turbo_response import redirect_303

  if request.turbo:
      return TurboStreamResponse(action=Action.REPLACE, target="item")
  else:
      return redirect_303("index")

If the request originates from a turbo-frame it will also set the *frame* property:


.. code-block:: python

  if request.turbo.frame == "my-playlist":
      return TurboFrame(request.turbo.frame).response("OK")


============================
Rendering streams and frames
============================


To render a *<turbo-stream>* or *<turbo-frame>* tag, you can use two functions, **render_turbo_stream()** and **render_turbo_frame()** respectively:


.. code-block:: python

   from turbo_response import Action, render_turbo_stream, render_turbo_frame

   # returns <turbo-stream action="replace" target="msg><template>OK</template></turbo-stream>
   render_turbo_stream(action=Action.REPLACE, target="msg", content="OK")

   # returns <turbo-frame id="msg>OK</turbo-frame>
   render_turbo_frame(dom_id="msg", content="OK")

Note that "content" can be empty, for example:

.. code-block:: python

   render_turbo_stream(action=Action.REMOVE, target="msg")


If you want to render a Django template, use **render_turbo_stream_template()** and **render_turbo_frame_template()** instead:

.. code-block:: python

   from turbo_response import Action, render_turbo_stream_template, render_turbo_frame_template

   render_turbo_stream_template("msg.html", {"msg": "hello"}, action=Action.REPLACE, target="msg")

   render_turbo_frame_template("msg.html", {"msg": "hello"}, dom_id="msg")

If you want to render a stream or target to an HTTP response, use the classes **TurboStreamResponse** and **TurboFrameResponse**:


.. code-block:: python

  from turbo_response import Action, TurboStreamResponse, TurboFrameResponse

  def my_stream(request):
      return TurboStreamResponse(action=Action.REPLACE, target="msg", content="OK")

  def my_frame(request):
      return TurboFrameResponse(dom_id="msg", content="OK")


Finally if you wish to render Django templates in the response, use **TurboStreamTemplateResponse** and **TurboFrameTemplateResponse**:

.. code-block:: python

  from turbo_response import Action, TurboStreamTemplateResponse, TurboFrameTemplateResponse

  def my_tmpl_stream(request):
      return TurboStreamTemplateResponse(request, "msg.html", {"msg": "OK"}, action=Action.REPLACE, target="msg")

  def my_tmpl_frame(request):
      return TurboFrameTemplateResponse(request, "msg.html", {"msg": "OK"}, dom_id="msg")

Note that these two classes subclass **django.template.response.TemplateResponse**.

The response classes will ensure the correct content type header *text/html; turbo-stream;* is added to the response, so the Turbo client library knows how to handle these responses correctly.

===========================
TurboFrame and TurboStream
===========================

The classes and functions above are a bit verbose for common operations. A couple of helper classes, **TurboFrame** and **TurboStream**, provide a more ergonomic API. Let's rewrite the above examples using these helpers:

.. code-block:: python

  from turbo_response import TurboFrame, TurboStream

  # first argument is the target
  TurboStream("msg").replace.render("OK")

  # be resolved as string
  TurboStream("msg").remove.render()

  # first argument is the DOM ID
  TurboFrame("msg").render("OK")

  TurboStream("msg").replace.template("msg.html", {"msg": "hello"}).render()

  TurboFrame("msg").template("msg.html", {"msg": "hello"}).render()

  def my_stream(request):
      return TurboStream("msg").replace.response("OK")

  def my_frame(request):
      return TurboFrame("msg").response("OK")

  def my_tmpl_stream(request):
      return TurboStream("msg").replace.template("msg.html", {"msg": "OK"}).response(request)

  def my_tmpl_frame(request):
      return TurboFrame("msg").template("msg.html", {"msg": "OK"}).response(request)


===============
Form Validation
===============

The most common pattern for server-side validation in a Django view consists of:

1. Render the initial form
2. Validate on POST
3. If any validation errors, re-render the form with errors and user input
4. If no validation errors, save to the database (and/or any other actions) and redirect

In order to make this work with Turbo you can do one of two things (**Note**: requires **@hotwired/turbo 7.0.0-beta.3**):

1. When the form is invalid, return with a 4** status response.
2. Add *data-turbo="false"* to your `<form>` tag.

If neither of these options are set, Turbo will throw an error if your view returns any response that isn't a redirect.

Note that if you set *data-turbo="false"* on your form like so:


.. code-block:: html

   <form method="post" action="..." data-turbo="false">

Turbo will force a full-page refresh, just as the same attribute does to link behavior. This might be acceptable however when working with views and forms e.g. in 3rd party packages where you don't want to change the default workflow.

If you want to continue using forms with Turbo just change the response status to a 4**, e.g. 422:


.. code-block:: python

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

As this is such a common pattern, we provide for convenience the **turbo_response.render_form_response** shortcut function which automatically sets the correct status depending on the form state (and adds "form" to the template context):

.. code-block:: python

  from django.shortcuts import redirect

  from turbo_response import render_form_response

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



If you are using CBVs, this package has a mixin class, **turbo_response.mixins.TurboFormMixin** that sets the correct status automatically to 422 for an invalid form:


.. code-block:: python

  from django.views.generic import FormView

  from turbo_response import redirect_303
  from turbo_response.mixins import TurboFormMixin

  from myapp import MyForm

  class MyView(TurboFormMixin, FormView):
      template_name = "my_form.html"

      def form_valid(self, form):
          return redirect_303("/")

In addition you can just subclass these views for common cases:

- **turbo_response.views.TurboFormView**
- **turbo_response.views.TurboCreateView**
- **turbo_response.views.TurboUpdateView**

In some cases you may wish to return a turbo-stream response containing just the form when the form is invalid instead of a full page visit. In this case just return a stream rendering the form partial in the usual manner. For example:

.. code-block:: python

  from django.shortcuts import redirect_303
  from django.template.response import TemplateResponse
  from django.views.generic import FormView

  from turbo_response import TurboStream

  from myapp import MyForm

  def my_view(request):
      if request.method == "POST":
          form = MyForm(request.POST)
          if form.is_valid():
              # save data etc...
              return redirect_303("/")
          return TurboStream("form-target").replace.template("_my_form.html").render(request)
      else:
          form = MyForm()
      return TemplateResponse(request, "my_form.html", {"form": my_form})

  # or CBV...

  class MyView(TurboFormMixin, FormView):
      template_name = "my_form.html"

      def form_valid(self, form):
          return redirect_303("/")

      def form_invalid(self, form):
          return TurboStream("form-target").replace.template("_my_form.html").render(request)

And your templates would look like this:

*my_form.html*

.. code-block:: html

  {% extends "base.html" %}

  {% block content %}
  <h1>my form goes here..</h1>
  {% include "_my_form.html" %}
  {% endblock content %}

*_my_form.html*

.. code-block:: html

  <form method="POST" id="form-target" action="/my-form">
    {% csrf_token %}
    {{ form.as_p }}
  </form>

A further point re: forms: Turbo processes forms using the FormData API and only includes inputs with a value. This means all buttons, inputs etc. must have a value. For example suppose you have a button like this:

.. code-block:: html

  <button name="send_action">Do this</button>

If your view code checks for this value:

.. code-block:: python

  if "send_action" in request.POST:
      ...

it will consistently fail. You should have something like:

.. code-block:: html

  <button name="send_action" value="true">Do this</button>

to ensure the FormData object includes the button value.

=========
Redirects
=========

As per the `documentation <https://turbo.hotwire.dev/handbook/drive#redirecting-after-a-form-submission>`_ Turbo expects a 303 redirect after a form submission. While this does not appear to be a hard-and-fast rule, you should probably have your view return a 303 instead of a 301 or 302 after a form submission. This package includes a class **turbo_response.HttpResponseSeeOther** and a shortcut **redirect_303** for returning the correct status with a redirect. The form mixin and view classes will return a 303 redirect by default.

.. code-block:: python

  from turbo_response import HttpResponseSeeOther

  def my_view(request):
      form = MyForm(request.POST)
      if form.is_valid():
          form.save()
          return HttpResponseSeeOther("/")

Note that the **redirect_303** shortcut works the same way as **django.shortcuts.redirect**: you can use a view name with arguments, a URL string, or a model which has a `get_absolute_url()` method:

.. code-block:: python

  from turbo_response import redirect_303

  redirect_303("/")
  redirect_303("blog_detail", id=1, slug=blog.title)
  redirect_303(blog)


================================
Responding with Multiple Streams
================================

Suppose you want to return **multiple** Turbo Streams in a single view. For example, let's say you are building a shopping cart for an e-commerce site.  The shopping cart is presented as a list of items, and you can edit the amount in each and click a "Save" icon next to that amount. When the amount is changed, you want to recalculate the total cost of all the items, and show this total at the bottom of the cart. In addition, there is a little counter on the top navbar which shows the same total across the whole site.

You can return multiple streams either in a generator with **TurboStreamStreamingResponse** or pass an iterable to **TurboStreamIterableResponse**. In either case, you must manually wrap each item in a *<turbo-stream>* tag.

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

  from turbo_response import TurboStreamIterableResponse, TurboStream

  def update_cart_item(request, item_id):
      # item saved to e.g. session or db
      save_cart_item(request, item_id)

      # for brevity, assume "total amount" is returned here as a
      # correctly formatted string in the correct local currency
      total_amount = calc_total_cart_amount(request)

      return TurboStreamIterableResponse([
          TurboStream("nav-cart-total").replace.render(total_amount),
          TurboStream("cart-summary-total").replace.render(total_amount),
      ])


Or using a generator:

.. code-block:: python

  from turbo_response import TurboStreamStreamingResponse, TurboStream

  def update_cart_item(request, item_id):
      # item saved to e.g. session or db
      save_cart_item(request, item_id)

      # for brevity, assume "total amount" is returned here as a
      # correctly formatted string in the correct local currency
      total_amount = calc_total_cart_amount(request)

      def render_response():
          yield TurboStream("nav-cart-total").replace.render(total_amount)
          yield TurboStream("cart-summary-total").replace.render(total_amount)
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

  from turbo_response import TurboFrame

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
      return TurboFrame("subscribe").template(
          "blogs/_subscribe.html",
          {"blog": blog, "is_subscribed": is_subscribed},
      ).response(request)

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

  <turbo-frame id="recommendations" src="{% url 'recommendations' %}" loading="lazy">
      <img src="{% static 'fancy-loader.gif' %}">
  </turbo-frame>

And our corresponding view:

.. code-block:: python

  def recommendations(request):
      # lazily build recommendations from algorithm and cache result
      recommended_items = get_recommendations_from_cache(request.user)
      return TurboFrame("recommendations").template(
          "_recommendations.html",
          {"items": recommended_items},
      ).response(request)

The template returned is just a plain Django template. The response class automatically wraps the correct tags, so we don't need to include `<turbo-frame>`.

Note that adding *loading="lazy"* will defer loading until the frame appears in the viewport.

.. code-block:: html

  <div class="recommendations">
      {% for item in items %}
      <h3><a href="{{ item.get_absolute_url }}">{{ item.title }}</a></h3>
      {% endfor %}
  </div>

When the user visits this page, they will see the loading gif at the bottom of the page, replaced by the list of recommended products when that view is ready.

========
Channels
========

This library can also be used with `django-channels <https://channels.readthedocs.io/en/stable/>`_ Consumers with the helper functions **render_turbo_stream()** and **render_turbo_stream_template()** when broadcasting streams (or the equivalent **TurboStream** methods):

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
      if (this.source) {
        disconnectStreamSource(this.source);
        this.source.close();
        this.source = null;
      }
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
