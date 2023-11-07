# Redirects

As per the [documentation](https://turbo.hotwire.dev/handbook/drive#redirecting-after-a-form-submission), Turbo expects a 303 redirect after a form submission.

If your project has `PUT`, `PATCH`, `DELETE` requests, then you might need to take a look at this [Clarification on redirect status code (303)](https://github.com/hotwired/turbo/issues/84#issuecomment-862656931)

In Django, you can do it like this:

```python
from django.shortcuts import redirect

return redirect('https://example.com/', status=303)
```
