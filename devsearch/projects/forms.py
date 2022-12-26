from django.forms import ModelForm, widgets
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "featured_image",
            "demo_link",
            "source_link",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs) -> None:
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add Title'}) Individual way to update input field

        for name, field in self.fields.items():
            # for loop to update through all fields' classes
            field.widget.attrs.update({"class": "input"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            "value",
            "review",
        ]

        labels = {
            "value": "Place your vote.",
            "review": "Add a comment with your vote.",
        }

    def __init__(self, *args, **kwargs) -> None:
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
