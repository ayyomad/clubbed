from django.db import models
from django.conf import settings



class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    tagline = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=False)
    is_active = models.BooleanField(default=True, help_text="Is this club active and functional or not")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ClubMembership(models.Model):

    class RoleChoices(models.TextChoices):
        MEMBER = 'MEMBER', 'Member'
        ADMIN = 'ADMIN', 'Admin'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='club_memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.MEMBER)
    title = models.CharField(max_length=50, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

        constraints = [models.UniqueConstraint(fields=['user','club'],name='unique_user_club_membership')]

    def __str__(self):
        display_title = f"({self.title})" if self.title else ""
        return f"{self.user} - {self.club} [{self.get_role_display()}{display_title}]"