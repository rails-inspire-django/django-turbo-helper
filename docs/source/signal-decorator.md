# Signal Decorator

In Django, developer usually use `post_save` signal to perform certain actions after a model instance is saved.

Even `created` parameter indicates whether the instance is newly created or an existing one, this is not that straightforward.

With `turbo_helper`, we provide **syntax suger** to make it more clear, just like Rails.

```python
from turbo_helper import after_create_commit, after_update_commit, after_delete_commit


@after_create_commit(sender=Message)
def create_message_content(sender, instance, created, **kwargs):
    broadcast_action_to(
        "chat",
        instance.chat_id,
        action="append",
        template="demo_openai/message_content.html",
        context={
            "instance": instance,
        },
        target=dom_id(instance.chat_id, "message_list"),
    )
```

Notes:

1. `after_create_commit`, `after_update_commit`, `after_delete_commit`, are decorators, they are used to decorate a function, which will be called after the model instance is created, updated or deleted.
2. The function decorated by `after_create_commit`, `after_update_commit`, receive the same arguments as `post_save` signal handler.
3. The function decorated by `after_delete_commit` receive the same arguments as `post_delete` signal handler.
4. This can make our code more clear, especially when we need to some broadcasts.
