import pytest

from tests.utils import assert_dom_equal
from turbo_helper import turbo_stream

pytestmark = pytest.mark.django_db


class TestGraft:
    def test_graft(self):
        stream = '<turbo-stream targets="#input" action="graft" parent="#parent"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.graft("#input", "#parent"))

    def test_graft_with_targets_and_html_as_kwargs(self):
        stream = '<turbo-stream targets="#input" action="graft" parent="#parent"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.graft(targets="#input", parent="#parent"))

        stream = '<turbo-stream targets="#input" action="graft" parent="#parent"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.graft(parent="#parent", targets="#input"))

    def test_graft_with_targets_as_positional_arg_and_html_as_kwarg(self):
        stream = '<turbo-stream targets="#input" action="graft" parent="#parent"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.graft("#input", parent="#parent"))

    def test_graft_with_additional_arguments(self):
        stream = '<turbo-stream targets="#input" action="graft" parent="#parent" something="else"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.graft("#input", parent="#parent", something="else")
        )


class TestAddCssClass:
    def test_add_css_class(self):
        stream = '<turbo-stream targets="#element" action="add_css_class" classes="container text-center"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.add_css_class("#element", "container text-center")
        )

    def test_add_css_class_with_targets_and_classes_as_kwargs(self):
        stream = '<turbo-stream targets="#element" action="add_css_class" classes="container text-center"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.add_css_class(
                targets="#element", classes="container text-center"
            ),
        )

    def test_add_css_class_with_classes_and_targets_as_kwargs(self):
        stream = '<turbo-stream targets="#element" action="add_css_class" classes="container text-center"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.add_css_class(
                classes="container text-center", targets="#element"
            ),
        )

    def test_add_css_class_with_targets_as_positional_arg_and_classes_as_kwarg(self):
        stream = '<turbo-stream targets="#element" action="add_css_class" classes="container text-center"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.add_css_class("#element", classes="container text-center"),
        )

    def test_add_css_class_with_additional_arguments(self):
        stream = '<turbo-stream targets="#element" action="add_css_class" classes="container text-center" something="else"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.add_css_class(
                "#element", classes="container text-center", something="else"
            ),
        )

    def test_add_css_class_with_classes_as_array(self):
        stream = '<turbo-stream targets="#element" action="add_css_class" classes="container text-center"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.add_css_class("#element", ["container", "text-center"])
        )

    def test_add_css_class_with_classes_as_array_and_kwarg(self):
        stream = '<turbo-stream targets="#element" action="add_css_class" classes="container text-center"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.add_css_class(
                "#element", classes=["container", "text-center"]
            ),
        )


class TestDispatchEvent:
    def test_dispatch_event(self):
        stream = '<turbo-stream name="custom-event" action="dispatch_event" targets="#element"><template>{}</template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.dispatch_event("#element", "custom-event")
        )

    def test_dispatch_event_with_detail(self):
        stream = '<turbo-stream name="custom-event" action="dispatch_event" targets="#element"><template>{"count":1,"type":"custom","enabled":true,"ids":[1,2,3]}</template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.dispatch_event(
                "#element",
                "custom-event",
                detail={
                    "count": 1,
                    "type": "custom",
                    "enabled": True,
                    "ids": [1, 2, 3],
                },
            ),
        )

    def test_dispatch_event_with_name_as_kwarg(self):
        stream = '<turbo-stream name="custom-event" action="dispatch_event" targets="#element"><template>{}</template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.dispatch_event("#element", name="custom-event")
        )

    def test_dispatch_event_with_targets_and_name_as_kwarg(self):
        stream = '<turbo-stream name="custom-event" action="dispatch_event" targets="#element"><template>{}</template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.dispatch_event(targets="#element", name="custom-event")
        )

    def test_dispatch_event_with_target_and_name_as_kwarg(self):
        stream = '<turbo-stream name="custom-event" action="dispatch_event" target="element"><template>{}</template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.dispatch_event(target="element", name="custom-event")
        )

    def test_dispatch_event_with_targets_name_and_detail_as_kwargs(self):
        stream = '<turbo-stream name="custom-event" action="dispatch_event" targets="#element"><template>{"count":1,"type":"custom","enabled":true,"ids":[1,2,3]}</template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.dispatch_event(
                targets="#element",
                name="custom-event",
                detail={
                    "count": 1,
                    "type": "custom",
                    "enabled": True,
                    "ids": [1, 2, 3],
                },
            ),
        )

    def test_dispatch_event_with_additional_attributes(self):
        stream = '<turbo-stream name="custom-event" action="dispatch_event" targets="#element" something="else"><template>{}</template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.dispatch_event(
                "#element", name="custom-event", something="else"
            ),
        )


class TestNotification:
    def test_notification_with_just_title(self):
        stream = '<turbo-stream action="notification" title="A title"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.notification("A title"))

    def test_notification_with_title_and_option(self):
        stream = '<turbo-stream action="notification" title="A title" body="A body"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.notification("A title", body="A body"))

    def test_notification_with_title_and_all_options(self):
        stream = """
        <turbo-stream
          title="A title"
          dir="ltr"
          lang="EN"
          badge="https://example.com/badge.png"
          body="This is displayed below the title."
          tag="Demo"
          icon="https://example.com/icon.png"
          image="https://example.com/image.png"
          data="{&quot;arbitrary&quot;:&quot;data&quot;}"
          vibrate="[200,100,200]"
          renotify="true"
          require-interaction="true"
          actions="[{&quot;action&quot;:&quot;respond&quot;,&quot;title&quot;:&quot;Please respond&quot;,&quot;icon&quot;:&quot;https://example.com/icon.png&quot;}]"
          silent="true"
          action="notification"
        ><template></template></turbo-stream>
        """.strip()

        options = {
            "dir": "ltr",
            "lang": "EN",
            "badge": "https://example.com/badge.png",
            "body": "This is displayed below the title.",
            "tag": "Demo",
            "icon": "https://example.com/icon.png",
            "image": "https://example.com/image.png",
            "data": '{"arbitrary":"data"}',
            "vibrate": "[200,100,200]",
            "renotify": "true",
            "require-interaction": "true",
            "actions": '[{"action":"respond","title":"Please respond","icon":"https://example.com/icon.png"}]',
            "silent": "true",
        }

        assert_dom_equal(stream, turbo_stream.notification("A title", **options))

    def test_notification_with_title_kwarg(self):
        stream = '<turbo-stream action="notification" title="A title"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.notification(title="A title"))


class TestRedirectTo:
    def test_redirect_to_default(self):
        stream = '<turbo-stream action="redirect_to" turbo-action="advance" url="http://localhost:8080"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.redirect_to("http://localhost:8080"))

    def test_redirect_to_with_turbo_false(self):
        stream = '<turbo-stream turbo="false" turbo-action="advance" url="http://localhost:8080" action="redirect_to"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.redirect_to("http://localhost:8080", turbo=False)
        )

    def test_redirect_to_with_turbo_action_replace(self):
        stream = '<turbo-stream turbo-action="replace" url="http://localhost:8080" action="redirect_to"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.redirect_to("http://localhost:8080", "replace")
        )

    def test_redirect_to_with_turbo_action_replace_kwarg(self):
        stream = '<turbo-stream turbo-action="replace" url="http://localhost:8080" action="redirect_to"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.redirect_to("http://localhost:8080", turbo_action="replace"),
        )

    def test_redirect_to_with_turbo_action_replace_and_turbo_frame_modals_as_positional_arguments(
        self,
    ):
        stream = '<turbo-stream turbo-action="replace" turbo-frame="modals" url="http://localhost:8080" action="redirect_to"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.redirect_to("http://localhost:8080", "replace", "modals"),
        )

    def test_redirect_to_with_turbo_action_replace_as_positional_argument_and_turbo_frame_modals_as_kwarg(
        self,
    ):
        stream = '<turbo-stream turbo-action="replace" turbo-frame="modals" url="http://localhost:8080" action="redirect_to"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.redirect_to(
                "http://localhost:8080", "replace", turbo_frame="modals"
            ),
        )

    def test_redirect_to_with_turbo_action_replace_and_turbo_frame_modals_as_kwargs(
        self,
    ):
        stream = '<turbo-stream turbo-action="replace" turbo-frame="modals" url="http://localhost:8080" action="redirect_to"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.redirect_to(
                "http://localhost:8080", turbo_action="replace", turbo_frame="modals"
            ),
        )

    def test_redirect_to_all_kwargs(self):
        stream = '<turbo-stream turbo-action="replace" turbo-frame="modals" turbo="true" url="http://localhost:8080" action="redirect_to"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.redirect_to(
                url="http://localhost:8080",
                turbo_action="replace",
                turbo_frame="modals",
                turbo=True,
            ),
        )


class TestTurboFrameReload:
    def test_turbo_frame_reload(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_reload"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.turbo_frame_reload("user_1"))

    def test_turbo_frame_reload_with_target_kwarg(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_reload"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.turbo_frame_reload(target="user_1"))

    def test_turbo_frame_reload_with_targets_kwarg(self):
        stream = '<turbo-stream targets="#user_1" action="turbo_frame_reload"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.turbo_frame_reload(targets="#user_1"))

    def test_turbo_frame_reload_additional_attribute(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_reload" something="else"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.turbo_frame_reload("user_1", something="else")
        )


class TestTurboFrameSetSrc:
    def test_turbo_frame_set_src(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_set_src" src="/users"><template></template></turbo-stream>'
        assert_dom_equal(stream, turbo_stream.turbo_frame_set_src("user_1", "/users"))

    def test_turbo_frame_set_src_with_src_kwarg(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_set_src" src="/users"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.turbo_frame_set_src("user_1", src="/users")
        )

    def test_turbo_frame_set_src_with_target_and_src_kwarg(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_set_src" src="/users"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.turbo_frame_set_src(target="user_1", src="/users")
        )

    def test_turbo_frame_set_src_with_src_and_target_kwarg(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_set_src" src="/users"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.turbo_frame_set_src(src="/users", target="user_1")
        )

    def test_turbo_frame_set_src_with_targets_and_src_kwarg(self):
        stream = '<turbo-stream targets="#user_1" action="turbo_frame_set_src" src="/users"><template></template></turbo-stream>'
        assert_dom_equal(
            stream, turbo_stream.turbo_frame_set_src(targets="#user_1", src="/users")
        )

    def test_turbo_frame_set_src_additional_attribute(self):
        stream = '<turbo-stream target="user_1" action="turbo_frame_set_src" src="/users" something="else"><template></template></turbo-stream>'
        assert_dom_equal(
            stream,
            turbo_stream.turbo_frame_set_src("user_1", src="/users", something="else"),
        )
