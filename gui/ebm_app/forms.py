from django import forms


class QueryForm(forms.Form):
    query = forms.CharField(label="", max_length=200)
    query.widget.attrs.update({"class": "form-control mr-sm-2 ml-sm-2",
                               "required": "required",
                               "placeholder": "Enter query:",
                               "style": "width: 500px"})

