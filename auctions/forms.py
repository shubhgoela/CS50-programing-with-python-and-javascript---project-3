from django import forms
from .models import Listing, Bid, Comment, Category, User, Watchlist
from django.utils.translation import gettext_lazy as _
from django.db.models import Max

class BidForm(forms.ModelForm):
    #user = forms.ModelChoiceField(queryset = User.objects.all(), widget = forms.HiddenInput())
    #listing = forms.ModelChoiceField(queryset = Listing.objects.all(), empty_label="Category", required=False)
    class Meta:
        model = Bid
        fields = ['user','listing', 'bid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bid'].widget.attrs.update({'class': 'form-control', 'placeholder': "Bid."})
        self.fields['bid'].label=""
        self.fields['user'].widget.attrs.update({'hidden' : 'True'})
        self.fields['user'].label=""
        self.fields['listing'].widget.attrs.update({'hidden' : 'True'})
        self.fields['listing'].label=""
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        bid = cleaned_data.get("bid")
        listing = cleaned_data.get("listing")
        print(listing,"  id :  ", listing.id)
        #print(self)
        #crrbid = self.bid
        #listing = self.listing
        bids = Listing.objects.get(pk = listing.id).bids.all()
        if bids.count() > 0:
            crrnt_bid = bids.aggregate(Max('bid'))
            if bid <= crrnt_bid['bid__max']:
                msg = f"The bid must be greater than $ {crrnt_bid['bid__max']}."
                self.add_error('bid', msg)
        else:
            if bid <= Listing.objects.get(pk = listing.id).price:
                msg = f"The bid must be greater than {Listing.objects.get(pk = listing).price}."
                self.add_error('bid', msg)
        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user','listing', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': 'Comment'})
        self.fields['comment'].label=""
        self.fields['user'].widget.attrs.update({'hidden' : 'True'})
        self.fields['user'].label=""
        self.fields['listing'].widget.attrs.update({'hidden' : 'True'})
        self.fields['listing'].label=""

class ListingForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset = User.objects.all(), widget = forms.HiddenInput())
    category = forms.ModelChoiceField(queryset = Category.objects.all(), empty_label="Category", required=False)
    description = forms.CharField(required = False)
    class Meta:
        model = Listing
        fields = '__all__'
        widgets = {
            'status' : forms.HiddenInput()
        }
        error_messages = {
            'title': {
                'max_length': _("Try a shorter title"),
                'required': _("Title is a required field")
            },
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label=""
        self.fields['title'].widget.attrs.update({'class' : 'form-control form-control-lg', 'placeholder':'Title'})
        self.fields['price'].label=""
        self.fields['price'].widget.attrs.update({'class' : 'form-control form-control-lg', 'placeholder':'$ Base Price'})
        self.fields['description'].label=""
        self.fields['description'].widget.attrs.update({'class' : 'form-control form-control-lg', 'placeholder':'Description'})
        self.fields['category'].label=""
        self.fields['category'].widget.attrs.update({'class' : 'form-control form-control-lg mb-3', 'placeholder':'Category'})
        self.fields['image'].label=""
        self.fields['image'].widget.attrs.update({'class' : 'form-control form-control-lg', 'placeholder':'Image url'})

class WatchlistForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label = ""
        self.fields['user'].widget.attrs.update({'hidden':'True'})
        self.fields['listing'].label=""
        self.fields['listing'].widget.attrs.update({'hidden': 'True'})