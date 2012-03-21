from django import forms

markdown_textarea_attrs = {'class':'wmd-input', 'id':'wmd-input', 'rows':'20', 'cols':'100'}

class QuestionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs = {'size':'80'}), max_length=256)
    contents = forms.CharField(widget=forms.Textarea(attrs=markdown_textarea_attrs))

class AnswerForm(forms.Form):
    contents = forms.CharField(widget=forms.Textarea(attrs=markdown_textarea_attrs))
    
#TODO: Change the name to ActivityResponseForm
class ActivityForm(forms.Form):
    contents = forms.CharField(widget=forms.Textarea(attrs=markdown_textarea_attrs))

class ActivityResponseReviewForm(forms.Form):
    contents = forms.CharField(widget=forms.Textarea(attrs=markdown_textarea_attrs))
