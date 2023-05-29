from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import UserProfile,User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(created)
    if created:
        print("user profile created")
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance) 
        print("user is updated")

@receiver(pre_save, sender=User)
def pre_save_user_profile(sender, instance, **kwargs):
    print(f"{instance.username}, user created.")
    