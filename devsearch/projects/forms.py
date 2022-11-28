from django.forms import ModelForm, widgets
from .models import Project
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title',
                  'description',
                  'featured_image',
                  'demo_link',
                  'source_link',
                  'tags',
                  ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs) -> None:
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add Title'}) Individual way to update input field

        for name, field in self.fields.items():
            # for loop to update through all fields' classes
            field.widget.attrs.update({'class': 'input'})
