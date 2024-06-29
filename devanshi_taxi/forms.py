from django import forms

CAR_CHOICES =( 
    ("1", "Kia"), 
    ("2", "Audi"), 
    ("3", "Thar"), 
    ("4", "Xuv"), 
    ("5", "Bmw"), 
)
class BookingForm(forms.Form):
    type = forms.ChoiceField( choices = CAR_CHOICES)
    pick_up = forms.CharField( max_length=255)
    drop =  forms.CharField( max_length=255)
    mobail = forms.IntegerField()