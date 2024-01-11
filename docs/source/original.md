# Render in Django View

**This approach is in maintenance mode, and we recommend to use template tags instead**

## TurboFrame and TurboStream

A couple of classes, **TurboFrame** and **TurboStream**, provide the basic API for rendering streams and frames.

To render plain strings:

```python
from turbo_helper import TurboFrame, TurboStream, Action

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
```

You can also render templates:

```python
TurboStream("msg").replace.template("msg.html", {"msg": "hello"}).render()

TurboStream(".msg", is_multiple=True).replace.template("msg.html", {"msg": "hello"}).render()

TurboFrame("msg").template("msg.html", {"msg": "hello"}).render()
```

You can also return an `HTTPResponse` subclass. The content type `text/html; turbo-stream;` will be added to turbo stream responses.

```python
def my_stream(request):
    return TurboStream("msg").replace.response("OK")

def my_frame(request):
    return TurboFrame("msg").response("OK")

def my_tmpl_stream(request):
    return TurboStream("msg").replace.template("msg.html", {"msg": "OK"}).response(request)

def my_tmpl_frame(request):
    return TurboFrame("msg").template("msg.html", {"msg": "OK"}).response(request)
```

**Note** if you are using the plain TurboStream or TurboFrame `render()` and `response()` non-template methods, any HTML will be automatically escaped. To prevent this pass `is_safe` (assuming you know the HTML is safe, of course):

```python
TurboStream("msg").replace.render("<b>OK</b>", is_safe=True)

TurboFrame("msg").response("<b>OK</b>", is_safe=True)
```

You don't need to do this with the template methods as HTML output is assumed:

```python
TurboFrame("msg").template("msg.html", {"msg": "OK"}).response(request)
```

See the API docs for more details.

## Responding with Multiple Streams

Suppose you want to return **multiple** Turbo Streams in a single view. For example, let's say you are building a shopping cart for an e-commerce site.  The shopping cart is presented as a list of items, and you can edit the amount in each and click a "Save" icon next to that amount. When the amount is changed, you want to recalculate the total cost of all the items and show this total at the bottom of the cart. In addition, there is a little counter on the top navbar that shows the same total across the whole site.

You can return multiple streams either in a generator with **TurboStreamStreamingResponse** or pass an iterable to **TurboStreamResponse**. In either case, you must manually wrap each item in a `<turbo-stream>` tag.

Taking the example above, we have a page with the shopping cart that has this snippet:

```html
<span id="cart-summary-total">{{ total_amount }}</span>
```

and in the navbar of our base template:

```html
<span id="nav-cart-total">{{ total_amount }}</span>
```

In both cases, the total amount is precalculated in the initial page load, for example using a context processor.

Each item in the cart has an inline edit form that might look like this:

```html
<td>
    <form method="post" action="{% url 'update_cart_item' item.id %}">
        {% csrf_token %}
        <input type="text" name="amount" value="{{ item.value }}">
        <button type="submit">Save</button>
    </form>
</td>
```

```python
from turbo_helper import TurboStreamResponse, TurboStream


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
```

Or using a generator:

```python
from turbo_helper import TurboStreamStreamingResponse, TurboStream


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
```

That's it! In this example, we are returning a very simple string value, so we don't need to wrap the responses in templates.

Note that this technique is something of an anti-pattern; if you have to update multiple parts of a page, a full refresh (i.e., a normal Turbo visit) is probably a better idea. It's useful though in some edge cases where you need to avoid this.

## The turbo_stream_response decorator

You can accomplish the above using the **turbo_stream_response** decorator with your view. This will check the output and wrap the response in a **TurboStreamResponse** or **TurboStreamStreamingResponse**:

```python
from turbo_helper import TurboStream
from turbo_helper.decorators import turbo_stream_response


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
```

Or using *yield* statements:

```python
  @turbo_stream_response
  def update_cart_item(request, item_id):
      # item saved to e.g. session or db
      save_cart_item(request, item_id)

      # for brevity, assume "total amount" is returned here as a
      # correctly formatted string in the correct local currency
      total_amount = calc_total_cart_amount(request)

      yield TurboStream("nav-cart-total").replace.render(total_amount)
      yield TurboStream("cart-summary-total").replace.render(total_amount)
```

If you return an HttpResponse subclass from your view (e.g. an HttpResponseRedirect, TemplateResponse, or a TurboStreamResponse) this will be ignored by the decorator and returned as normal.

## Using Turbo Frames

Turbo frames are straightforward using the **TurboFrame** class.

For example, suppose we want to render some content inside a frame with the ID "content":

```html
<div id="content"></div>
<a href="/my-view" data-turbo-frame="content">add something here!</a>
```

The view looks like this:

```python
def my_view(request):
  return TurboFrame("content").response("hello")
```

As with streams, you can also render a template:

```python
def my_view(request):
    return TurboFrame("content").template("_content.html", {"message": "hello"}).response(request)
```

## Handling Lazy Turbo Frames

Turbo Frames have a useful feature that allows `lazy loading <https://turbo.hotwire.dev/handbook/frames>`_. This is very easy to handle with Django. For example, our e-commerce site includes a list of recommendations at the bottom of some pages based on the customer's prior purchases. We calculate this list using our secret-sauce machine-learning algorithm. Although the results are cached for that user, the initial run can be a bit slow, and we don't want to slow down the rest of the page when the recommendations are recalculated.

This is a good use case for a lazy turbo frame. Our template looks like this, with a fancy loading gif as a placeholder:

```html
<turbo-frame id="recommendations" src="{% url 'recommendations' %}" loading="lazy">
    <img src="{% static 'fancy-loader.gif' %}">
</turbo-frame>
```

And our corresponding view:

```python
def recommendations(request):
    # lazily build recommendations from algorithm and cache result
    recommended_items = get_recommendations_from_cache(request.user)
    return TurboFrame("recommendations").template(
        "_recommendations.html",
        {"items": recommended_items},
    ).response(request)
```

The template returned is just a plain Django template. The response class automatically wraps the correct tags, so we don't need to include `<turbo-frame>`.

Note that adding *loading="lazy"* will defer loading until the frame appears in the viewport.

```html
<div class="recommendations">
    {% for item in items %}
    <h3><a href="{{ item.get_absolute_url }}">{{ item.title }}</a></h3>
    {% endfor %}
</div>
```

When the user visits this page, they will see the loading gif at the bottom of the page, replaced by the list of recommended products when that view is ready.

