from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from machina.core.db.models import get_model
from machina.core.loading import get_class

from .models import NotificationSettings

Forum = get_model('forum', 'Forum')
Topic = get_model('forum_conversation', 'Topic')
ForumProfile = get_model('forum_member', 'ForumProfile')

TrackingHandler = get_class('forum_tracking.handler', 'TrackingHandler')
track_handler = TrackingHandler()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_user_post_save(instance, created, raw, **kwargs):
    if not raw and not created:
        ns, _ = NotificationSettings.objects.get_or_create(user=instance)
        if ns.auto_subscribe:
            profile, _ = ForumProfile.objects.get_or_create(user=instance)
            profile.auto_subscribe_topics = True
            profile.auto_subscribe_posts = True
            profile.notify_subscribed_topics = True
            profile.save()
            forums = Forum.objects.all()
            instance.forum_subscriptions.set(Forum.objects.all())
            instance.topic_subscriptions.set(Topic.objects.all())
            track_handler.mark_forums_read(forums, instance)


@receiver(post_save, sender=NotificationSettings)
def on_settings_post_save(instance, created, raw, **kwargs):
    if not raw:
        profile, _ = ForumProfile.objects.get_or_create(user=instance.user)
        profile.notify_subscribed_topics = instance.auto_subscribe
        profile.save(update_fields=['notify_subscribed_topics'])


@receiver(post_save, sender=Forum)
def on_forum_create(instance, created, raw, **kwargs):
    if not raw and not created:
        users = [
            fs.user for fs in
            NotificationSettings.objects.filter(
                auto_subscribe=True).select_related('user')
        ]
        instance.subscribers.add(*users)
