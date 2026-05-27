from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from django.dispatch import receiver


@receiver(user_signed_up)
def assign_learning_group(sender, request, user, **kwargs):
    group, _ = Group.objects.get_or_create(name="Learning User")
    user.groups.add(group)
