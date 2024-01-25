# Multi-format Response

In Ruby on Rails, `respond_to` is a method that allows you to define how your controller should respond to different types of requests.

```ruby
class PostsController < ApplicationController
  def create
    @post = Post.new(post_params)

    respond_to do |format|
      if @post.save
        format.html { redirect_to @post, notice: 'Post was successfully created.' }
        format.json { render json: @post, status: :created }
        format.turbo_stream { render turbo_stream: turbo_stream.append(@post) }
      else
        format.html { render :new }
        format.json { render json: @post.errors, status: :unprocessable_entity }
        format.turbo_stream { render turbo_stream: turbo_stream.replace('new_post', partial: 'posts/form', locals: { post: @post }) }
      end
    end
  end
end
```

In the above code, developer can return different response format based on request `Accept` header.

We can do similar approach with `turbo_helper`

```python
from turbo_helper import (
  TurboStreamResponse,
  respond_to,
)

class TaskCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        request = self.request
        messages.success(request, "Created successfully")

        with respond_to(request) as resp_format:
          if resp_format.turbo_stream:
            return TurboStreamResponse(
              render_to_string(
                "task_create_success.turbo_stream.html",
                context={
                  "form": TaskForm(),
                },
                request=self.request,
              ),
            )
          if resp_format.html:
            return response
```

Notes:

1. If the browser accepts turbo stream, we return turbo stream response.
2. If the browser accepts HTML, we return HTML response.
3. This is useful when we want to **migrate our Django app from normal web page to turbo stream gradually**.

```{note}
Please **put the non html response before html response**, and use html response as the fallback response.
```
