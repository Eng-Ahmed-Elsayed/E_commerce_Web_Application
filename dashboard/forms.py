from django.forms import ModelForm
from base.models import Ad, Review
from django import forms


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['name', 'price', 'category', 'brand', 'model_year', 'location', 'details', 'img']
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control bg-white"}),
            'price': forms.NumberInput(attrs={'class': "col-lg-4 ml-lg-4 my-2 pt-2 pb-1 rounded bg-white "}),
            'model_year': forms.NumberInput(attrs={'class': "col-lg-4 ml-lg-4 my-2 pt-2 pb-1 rounded bg-white "}),
            'category': forms.Select(attrs={'class': "form-control w-100 bg-white"}),
            'brand': forms.TextInput(attrs={'class': "form-control bg-white"}),
            'location': forms.TextInput(attrs={'class': "form-control bg-white"}),
            'details': forms.Textarea(attrs={'class': "form-control bg-white",}),
            'img': forms.FileInput(attrs={'class': "form-control-file d-none ", 'id': "file-upload", 'oninput': "getImgName()"})
        }


review_choices =(
    ("1", "(1) Very Bad"),
    ("2", "(2) Bad"),
    ("3", "(3) Good"),
    ("4", "(4) Very Good"),
    ("5", "(5) Great"),
)
class ReviewForm(ModelForm):
    rating = forms.ChoiceField(choices=review_choices)
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            
            'review': forms.Textarea(attrs={'class': "form-control", 'id':"review", "placeholder":"Message", 'rows':"6"}),
        }
