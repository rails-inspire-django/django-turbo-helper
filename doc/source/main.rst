This package provides helpers for server-side rendering of `Hotwired/Turbo <https://hotwired.dev/>`_ streams and frames.

**Disclaimer**: the Hotwired/Turbo client libraries are, at time of writing, still in Beta. We expect there will be breaking changes both to the client library and this package until the first stable release. This package, and the Turbo client, should therefore be used with caution in a production environment. The version used in testing is *@hotwired/turbo==7.0.0-beta.8*.

============
Requirements
============

This library requires Python 3.8+ and Django 3.0+.

===============
Getting Started
===============

``pip install django-turbo-response``

To install from Git:

``git clone https://github.com/hotwire-django/django-turbo-response``

``cd django-turbo-response``

``python setup.py install``


Next update **INSTALLED_APPS**:

.. code-block:: python

  INSTALLED_APPS = [
    "turbo_response",
    ...
  ]

**Note**: This install does not include any client libraries (e.g. Turbo or Stimulus). You may wish to add these yourself using your preferred Javascript build tool, or use a CDN. Please refer to the Hotwire documentation on installing these libraries.


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

  if request.turbo:
      return TurboStream("item").replace.response("OK")
  else:
      return redirect("index")

If the request originates from a turbo-frame it will also set the *frame* property:


.. code-block:: python

  if request.turbo.frame == "my-playlist":
      return TurboFrame(request.turbo.frame).response("OK")

===========================
TurboFrame and TurboStream
===========================

A couple of classes, **TurboFrame** and **TurboStream**, provide the basic API for rendering streams and frames.

To render plain strings:

.. code-block:: python

  from turbo_response import TurboFrame, TurboStream, Action

  # returns <turbo-stream action="replace" target="msg"><template>OK</template></turbo-stream>
  TurboStream("msg").replace.render("OK")

  # returns <turbo-stream action="replace" targets=".msg"><template>OK</template></turbo-stream>
  TurboStream(".msg", is_multiple=True).replace.render("OK")

  # set action dynamically
  TurboStream("msg").action(Action.REPLACE).render("OK")

  # returns <turbo-stream action="remove" target="msg"><template></template></turbo-stream>
  TurboStream("msg").remove.render()

  # returns <turbo-frame id="msg">OK</turbo-frame>
  TurboFrame("msg").render("OK")

You can also render templates:

.. code-block:: python

  TurboStream("msg").replace.template("msg.html", {"msg": "hello"}).render()

  TurboStream(".msg", is_multiple=True).replace.template("msg.html", {"msg": "hello"}).render()

  TurboFrame("msg").template("msg.html", {"msg": "hello"}).render()

You can also return an *HTTPResponse* subclass. The content type *text/html; turbo-stream;* will be added to turbo stream responses.

.. code-block:: python

  def my_stream(request):
      return TurboStream("msg").replace.response("OK")

  def my_frame(request):
      return TurboFrame("msg").response("OK")

  def my_tmpl_stream(request):
      return TurboStream("msg").replace.template("msg.html", {"msg": "OK"}).response(request)

  def my_tmpl_frame(request):
      return TurboFrame("msg").template("msg.html", {"msg": "OK"}).response(request)


**Note** if you are using the plain TurboStream or TurboFrame *render()* and *response()* non-template methods, any HTML will be automatically escaped. To prevent this pass **is_safe** (assuming you know the HTML is safe, of course):

.. code-block:: python

      TurboStream("msg").replace.render("<b>OK</b>", is_safe=True)

      TurboFrame("msg").response("<b>OK</b>", is_safe=True)

You don't need to do this with the template methods as HTML output is assumed:

.. code-block:: python

      TurboFrame("msg").template("msg.html", {"msg": "OK"}).response(request)

See the API docs for more details.


===============
Form Validation
===============

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
          return TurboStream("form-target").replace.template("_my_form.html").render(request=request)
      else:
          form = MyForm()
      return TemplateResponse(request, "my_form.html", {"form": my_form})

  # or CBV...

  class MyView(TurboFormMixin, FormView):
      template_name = "my_form.html"

      def form_valid(self, form):
          return redirect_303("/")

      def form_invalid(self, form):
          return TurboStream("form-target").replace.template("_my_form.html").render(request=request)

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


As this is a useful pattern in many situations, for example when handling forms inside modals, this package provides a mixin class **turbo_response.mixins.TurboStreamFormMixin**:

.. code-block:: python


  from django.views.generic import FormView
  from turbo_response.mixins import TurboStreamFormMixin

  class MyView(TurboStreamFormMixin, FormView):
      turbo_stream_target = "form-target"
      template_name = "my_form.html"
      # action = Action.REPLACE


This mixin will automatically add the target name to the template context as *turbo_stream_target*. The partial template will be automatically resolved as the template name prefixed with an underscore: in this example, *_my_form.html*. You can also set it explicitly with the *turbo_stream_template_name* class attribute.  The default action is "replace".

As with the form mixin above, the package includes a number of view classes using this mixin:

- **turbo_response.views.TurboStreamFormView**
- **turbo_response.views.TurboStreamCreateView**
- **turbo_response.views.TurboStreamUpdateView**


So the above example could be rewritten as:

.. code-block:: python


  from turbo_response.views import TurboStreamFormView

  class MyView(TurboStreamFormView):
      turbo_stream_target = "form-target"
      template_name = "my_form.html"

The model-based classes automatically set the target DOM ID based on the model. The pattern for **TurboStreamCreateView** is *form-<model_name>* and for **TurboStreamUpdateView** *form-<model-name>-<pk>*. You can override this by setting the *target* attribute explicitly or overriding the *get_turbo_stream_target* method.

A final point re: forms: Turbo processes forms using the FormData API and only includes inputs with a value. This means all buttons, inputs etc. must have a value. For example suppose you have a button like this:

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

You can return multiple streams either in a generator with **TurboStreamStreamingResponse** or pass an iterable to **TurboStreamResponse**. In either case, you must manually wrap each item in a *<turbo-stream>* tag.

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

  from turbo_response import TurboStreamResponse, TurboStream

  def update_cart_item(request, item_id):
      # item saved to e.g. session or db
      save_cart_item(request, item_id)

      # for brevity, assume "total amount" is returned here as a
      # correctly formatted string in the correct local currency
      total_amount = calc_total_cart_amount(request)

      return TurboStreamResponse([
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

That's it! In this example are returning a very simple string value, so we don't need to wrap the responses in templates.

Note that this technique is something of an anti-pattern; if you have to update multiple parts of a page, a full refresh (i.e. a normal Turbo visit) is probably a better idea. It's useful though in some edge cases where you need to avoid this.

===================================
The turbo_stream_response decorator
===================================

You can accomplish the above using the **turbo_stream_response** decorator with your view. This will check the output and wrap the response in a **TurboStreamResponse** or **TurboStreamStreamingResponse**:

.. code-block:: python

  from turbo_response import TurboStream
  from turbo_response.decorators import turbo_stream_response

  @turbo_stream_response
  def update_cart_item(request, item_id):
      # item saved to e.g. session or db
      save_cart_item(request, item_id)

      # for brevity, assume "total amount" is returned here as a
      # correctly formatted string in the correct local currency
      total_amount = calc_total_cart_amount(request)

      return [
          TurboStream("nav-cart-total").replace.render(total_amount),
          TurboStream("cart-summary-total").replace.render(total_amount),
      ]

Or using *yield* statements:

.. code-block:: python

  @turbo_stream_response
  def update_cart_item(request, item_id):
      # item saved to e.g. session or db
      save_cart_item(request, item_id)

      # for brevity, assume "total amount" is returned here as a
      # correctly formatted string in the correct local currency
      total_amount = calc_total_cart_amount(request)

      yield TurboStream("nav-cart-total").replace.render(total_amount)
      yield TurboStream("cart-summary-total").replace.render(total_amount)


If you return an HttpResponse subclass from your view (e.g. an HttpResponseRedirect, TemplateResponse or a TurboStreamResponse) this will be ignored by the decorator and returned as normal.

==================
Using Turbo Frames
==================

Turbo frames are straightforward using the **TurboFrame** class.


For example, suppose we want to render some content inside a frame with the ID "content":

.. code-block:: html

  <div id="content"></div>
  <a href="/my-view" data-turbo-frame="content">add something here!</a>


The view looks like this:

.. code-block:: python

  def my_view(request):
    return TurboFrame("content").response("hello")


As with streams, you can also render a template:

.. code-block:: python

  def my_view(request):
      return TurboFrame("content").template("_content.html", {"message": "hello"}).response(request)


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

This library can also be used with `django-channels <https://channels.readthedocs.io/en/stable/>`_. As with multiple streams, you can use the **TurboStream** class to broadcast turbo-stream content from your consumers.

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
                  TurboStream("unread_message_counter")
                  .replace.render(str(num_unread_messages))
              )

              await self.send(
                  TurboStream("messages").append.template(
                    "chat/_message.html",
                    {"message": message, "user": self.scope['user']},
                  ).render()
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

**Note** if you want to add reactivity directly to your models, so that model changes broadcast turbo-streams automatically, we recommend the `turbo-django <https://github.com/hotwire-django/turbo-django>`_ package.

==========================
Hints on testing
==========================

When testing it's useful to be able to simulate Turbo headers.


If you wish to test the result of a response within a Turbo frame, use the header **HTTP_TURBO_FRAME**:


.. code-block:: python

  from django.test import TestCase

  class TestViews(TestCase):

      def test_my_frame_view(self):
          response = self.client.get("/", HTTP_TURBO_FRAME="some-dom-id")
          self.assertEqual(response.status_code, 200)


To simulate the Turbo-Stream header you should set **HTTP_ACCEPT**.


.. code-block:: python

  from django.test import TestCase
  from turbo_response.constants import TURBO_STREAM_MIME_TYPE

  class TestViews(TestCase):

      def test_my_stream_view(self):
          response = self.client.post("/", HTTP_ACCEPT=TURBO_STREAM_MIME_TYPE)
          self.assertEqual(response.status_code, 200)

=====
Links
=====

Hotwired: https://hotwired.dev/

=======
License
=======

This project is covered by the MIT license.
