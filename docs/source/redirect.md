# Redirects

As per the [documentation](https://turbo.hotwire.dev/handbook/drive#redirecting-after-a-form-submission), Turbo expects a 303 redirect after a form submission.

If your project has `PUT`, `PATCH`, `DELETE` requests, then you should take a look at this [Clarification on redirect status code (303)](https://github.com/hotwired/turbo/issues/84#issuecomment-862656931)

```python
from turbo_response import redirect_303

return redirect_303("/")
```
