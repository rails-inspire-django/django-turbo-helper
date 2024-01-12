# dom_id

`dom_id` is a helper method that returns a unique DOM ID based on the object's class name and ID

```html
{% load turbo_helper %}

{% dom_id instance %}               ->  task_1
{% dom_id instance 'detail' %}      ->  detail_task_1
{% dom_id Task %}                   ->  new_task
```

1. `dom_id` first argument can be string, instance or Model class
2. `dom_id` second argument is optional string that will be used as `prefix`.
3. The `dom_id` can help make the id generation behavior consistent across the project, and save our time to update it in `turbo-stream` or `turbo-frame` element.
4. You can also use it in your Django view code.

Use in Django view

```python
from turbo_helper import dom_id

target = dom_id(instance, "detail_container")
```
