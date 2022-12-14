from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Skill, Profile, Message


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
        fields = "__all__"
        exclude = [
            "owner",
            "created",
            "id",
        ]

    def __init__(self, *args: any, **kwargs: any) -> None:
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # for loop to update through all fields' classes
            field.widget.attrs.update({"class": "input"})


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

    def __init__(self, *args: any, **kwargs: any) -> None:
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # for loop to update through all fields' classes
            field.widget.attrs.update({"class": "input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            "sender",
            "recipient",
            "name",
            "email",
            "subject",
            "body",
        ]
