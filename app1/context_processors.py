
from . models import Orders
                
def request_count(request):
    if request.user.is_authenticated:
        pend_order=Orders.objects.filter(ordered_to=request.user,status='Pending').count()
        comp_order=Orders.objects.filter(ordered_to=request.user,status='Complete').count()
        accept_order=Orders.objects.filter(ordered_to=request.user,status='Accept').count()
        return{
        "pend_order":pend_order,
        'comp_order':comp_order,
        'accept_order':accept_order
        }
    else:
        return{
        "pend_order":0,
        'comp_order':0,
        'accept_order':0
        }