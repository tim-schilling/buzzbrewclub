from machina.core.db.models import get_model


ForumProfile = get_model('forum_member', 'ForumProfile')


def merge_users_posts_threads(final, other):
    other.post_set.all().update(updated_by=final)
    other.posts.all().update(poster=final)
    other.topic_set.all().update(poster=final)
    ForumProfile.objects.update_or_create(
        user=final,
        defaults={
            'posts_count': final.posts.all().count()
        }
    )
    other.delete()
