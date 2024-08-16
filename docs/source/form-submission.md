# Form Submission

By default, Turbo will intercept all clicks on links and form submission, as for form submission, if the form validation fail on the server side, Turbo expects the server return `422 Unprocessable Entity`.

In Django, however, failed form submission would still return HTTP `200`, which would cause some issues when working with Turbo Drive.

[https://turbo.hotwired.dev/handbook/drive#redirecting-after-a-form-submission](https://turbo.hotwired.dev/handbook/drive#redirecting-after-a-form-submission)

How to solve this issue?

`turbo_helper.middleware.TurboMiddleware` can detect POST request from Turbo and change the response status code to `422` if the form validation failed.

It should work out of the box for `Turbo 8+` on the frontend.

So developers do not need to manually set the status code to `422` in the view.
