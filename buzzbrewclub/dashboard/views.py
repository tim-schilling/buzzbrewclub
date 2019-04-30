
from django.utils import timezone
from django.views.generic import TemplateView

from machina.core.db.models import get_model

from buzzbrewclub.timezone import tz
from buzzbrewclub.events.models import (
    Event,
    HappyHour,
    Meeting,
)

Post = get_model('forum_conversation', 'Post')


class LandingView(TemplateView):
    template_name = 'dashboard/landing.html'

    def get_context_data(self, **kwargs):
        def get_event_qs(model):
            return model.objects.filter(
                published=True,
                date__gte=timezone.now().astimezone(tz).date(),
            ).order_by('start')

        upcoming = {
            'events': get_event_qs(Event),
            'happy_hours': get_event_qs(HappyHour),
            'meetings': get_event_qs(Meeting),
        }
        recent_posts = Post.objects.filter(
            approved=True,
            topic__approved=True,
        ).order_by('-created')[:5]
        return super().get_context_data(
            recent_posts=recent_posts,
            upcoming=upcoming,
            **kwargs)


landing_view = LandingView.as_view()
