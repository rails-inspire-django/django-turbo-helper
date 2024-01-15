# Multi-format Response

In Ruby on Rails, `respond_to` is a method that allows you to define how your controller should respond to different types of requests.

```ruby
class PostsController < ApplicationController
  def create
    @post = Post.new(post_params)

    respond_to do |format|
      if @post.save
        format.turbo_stream { render turbo_stream: turbo_stream.append(@post) }
        format.json { render json: @post, status: :created }
        format.html { redirect_to @post, notice: 'Post was successfully created.' }
      else
        format.turbo_stream { render turbo_stream: turbo_stream.replace('new_post', partial: 'posts/form', locals: { post: @post }) }
        format.json { render json: @post.errors, status: :unprocessable_entity }
        format.html { render :new }
      end
    end
  end
end
```

In the above code, developer can return different response format based on request `Accept` header.

We can do similar approach with `turbo_helper`

```python
from turbo_helper import (
  ResponseFormat,
  response_format,
)

class TaskCreateView(LoginRequiredMixin, CreateView):
  def form_valid(self, form):
    response = super().form_valid(form)
    request = self.request
    messages.success(request, "Created successfully")

    with response_format(request) as resp_format:
      if resp_format == ResponseFormat.TurboStream:
        return TurboStreamResponse(
          render_to_string(
            "demo_tasks/partial/task_create_success.turbo_stream.html",
            context={
              "form": TaskForm(),
            },
            request=self.request,
          ),
        )
      else:
        return response
```

Notes:

1. If you are using Python 3.11+,
2. If the client `Accept` turbo stream, we return turbo stream response.
3. If not, we return normal HTML response as fallback solution.
4. This is useful when we want to migrate our Django app from normal web page to turbo stream gradually.
