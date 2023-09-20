# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import CustomUser

# @receiver(pre_save, sender=CustomUser)
# def set_default_profile_picture(sender, instance, **kwargs):
#     if not instance.display_pic:
#         if instance.gender == 'Male':
#             instance.display_pic = 'male_default.png'
#         elif instance.gender == 'Female':
#             instance.display_pic = 'female_default.png'
#         else:
#             instance.display_pic = 'default.png'
