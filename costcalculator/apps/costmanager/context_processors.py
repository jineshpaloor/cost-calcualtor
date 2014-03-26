from .forms import BillForm


def bill_form(request):
    billform = BillForm()
    return {'bill_form': billform}
