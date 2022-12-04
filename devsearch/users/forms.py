from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Skill, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "email",
            "username",
            "password1",
            "password2",
        ]
        labels = {
            "first_name": "Name",
        }

    def __init__(self, *args: any, **kwargs: any) -> None:
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {" class": "input input--text", "id": "formInput#text"}
        )

        self.fields["email"].widget.attrs.update(
            {" class": "input input--email", "id": "formInput#email"}
        )

        self.fields["username"].widget.attrs.update(
            {" class": "input input--text", "id": "formInput#text"}
        )

        self.fields["password1"].widget.attrs.update(
            {" class": "input input--password", "id": "formInput#password"}
        )

        self.fields["password2"].widget.attrs.update(
            {" class": "input input--password", "id": "formInput#password"}
        )


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name",
            "description",
        ]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "location",
            "email",
            "short_intro",
            "bio",
            "profile_image",
            "social_github",
            "social_twitter",
            "social_linkedin",
            "social_youtube",
            "social_website",
        ]
