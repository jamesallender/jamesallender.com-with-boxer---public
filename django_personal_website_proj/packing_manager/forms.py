from django import forms
from .models import Box


class GetCreateUpdateBox(forms.Form):
    box_id = forms.IntegerField()
    box_num = forms.IntegerField()
    box_dest = forms.MultipleChoiceField(choices=[('bedroom_master', 'Master-Bedroom'), ('bedroom_2', 'Bedroom-2'),
                                                  ('kitchen', 'Kitchen'), ('living_room', 'Living-Room'),
                                                  ('bathroom', 'Bathroom'), ('office', 'Office'),
                                                  ('garage', 'Garage'), ('storage', 'Storage')])
    contents = forms.CharField(widget=forms.Textarea)
    box_warnings = forms.ChoiceField(choices=[('fragile', 'Fragile'), ('private', 'Private'),
                                              ('flammable', 'Flammable'), ('explosive', 'Explosive')],
                                     required=False)

    class Meta:
        model = Box
        # fields = ['username', 'display_name', 'email', 'password1', 'password2', 'authorize']
        fields = ['box_num', 'box_dest', 'contents', 'box_warnings', 'box_id']
