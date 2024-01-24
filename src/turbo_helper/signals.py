from django.db.models.signals import post_delete, post_save


def after_create_commit(sender):
    def decorator(handler_func):
        def wrapper(sender, instance, created, **kwargs):
            if created:
                # Call the original signal handler function
                handler_func(sender, instance, created=created, **kwargs)

        # Connect the wrapper function to the post_save signal
        post_save.connect(wrapper, sender=sender)

        # Return the wrapper function to be used as the signal handler
        return wrapper

    # Return the decorator function
    return decorator


def after_update_commit(sender):
    def decorator(handler_func):
        def wrapper(sender, instance, created, **kwargs):
            if not created:
                # Call the original signal handler function
                handler_func(sender, instance, created=created, **kwargs)

        # Connect the wrapper function to the post_save signal
        post_save.connect(wrapper, sender=sender)

        # Return the wrapper function to be used as the signal handler
        return wrapper

    # Return the decorator function
    return decorator


def after_delete_commit(sender):
    def decorator(handler_func):
        def wrapper(sender, instance, **kwargs):
            # Call the original signal handler function
            handler_func(sender, instance, **kwargs)

        # Connect the wrapper function to the post_delete signal
        post_delete.connect(wrapper, sender=sender)

        # Return the wrapper function to be used as the signal handler
        return wrapper

    # Return the decorator function
    return decorator
