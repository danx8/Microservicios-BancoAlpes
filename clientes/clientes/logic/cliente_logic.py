from ..models import Cliente

def get_cliente():
    queryset = Cliente.objects.all()
    return (queryset)

def create_cliente(form):
    cliente = form.save()
    cliente.save()
    return ()

