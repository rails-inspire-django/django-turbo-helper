# Hints on testing

When testing, it's useful to be able to simulate Turbo headers.

If you wish to test the result of a response within a Turbo frame, use the header **HTTP_TURBO_FRAME**:

```python
from django.test import TestCase

class TestViews(TestCase):

    def test_my_frame_view(self):
        response = self.client.get("/", HTTP_TURBO_FRAME="some-dom-id")
        self.assertEqual(response.status_code, 200)
```

To simulate the Turbo-Stream header, you should set **HTTP_ACCEPT**.

```python
from django.test import TestCase
from turbo_helper.constants import TURBO_STREAM_MIME_TYPE


class TestViews(TestCase):

    def test_my_stream_view(self):
        response = self.client.post("/", HTTP_ACCEPT=TURBO_STREAM_MIME_TYPE)
        self.assertEqual(response.status_code, 200)
```
