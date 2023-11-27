from django.contrib.auth.models import User as DjangoUser
from .models import User as CustomUser


def sync_users():
    user_count = CustomUser.objects.count()
    django_users = DjangoUser.objects.all()

    # check custom user list and adds users from django user list if not already in custom users
    for index, django_user in enumerate(django_users):
        existing_user = CustomUser.objects.filter(username=django_user.username).exists()
        if existing_user:
            return
        new_user_id = user_count + index
        custom_user = CustomUser.objects.create(
            user_ID=new_user_id,
            username=django_user.username,
            email=django_user.email,
        )
        custom_user.save()
