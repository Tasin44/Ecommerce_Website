from django import forms#Imports Django’s forms framework
from .models import Order

#Creates a form for capturing order details.

class OrderCreateForm(forms.ModelForm):#A form for creating new orders,inheriting form.modelForm, which automatically links the form to a model.
    class Meta:
        model = Order
        fields = ["full_name","email","address"]
# model: Specifies the model (Order) the form is tied to.
# fields: Lists the fields (full_name, email, address) to include in the form for the user to fill out.