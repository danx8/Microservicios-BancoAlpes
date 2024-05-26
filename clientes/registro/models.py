import hashlib
from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=50, default='')
    apellido = models.CharField(max_length=50, default='')
    cedula = models.CharField(max_length=10, default='')
    celular = models.CharField(max_length=12, default='')
    correo = models.CharField(max_length=100, default='')
    pais = models.CharField(max_length=100, default='')
    ciudad = models.CharField(max_length=100, default='')
    fechaNacimiento = models.DateField()
    integridad_hash = models.CharField(max_length=64, editable=False)
    #data = json
    def calcular_hash(self):
        data = f"{self.nombre}{self.apellido}{self.cedula}{self.celular}{self.correo}{self.pais}{self.ciudad}{self.fechaNacimiento}".encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def save(self, *args, **kwargs):
        data = f"{self.nombre}{self.apellido}{self.cedula}{self.celular}{self.correo}{self.pais}{self.ciudad}{self.fechaNacimiento}".encode('utf-8')
        self.integridad_hash = hashlib.sha256(data).hexdigest()
        super().save(*args, **kwargs)  

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.cedula}'
    
    @property
    def validar_integridad(self):
        data = f"{self.nombre}{self.apellido}{self.cedula}{self.celular}{self.correo}{self.pais}{self.ciudad}{self.fechaNacimiento}".encode('utf-8')
        current_hash = hashlib.sha256(data).hexdigest()
        return current_hash == self.integridad_hash

class InformacionAdicional(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    profesion = models.CharField(max_length=100)
    actEconomica = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    ingresos = models.FloatField(default=0)
    egresos = models.FloatField(default=0)
    deuda = models.FloatField(default=0)

    def __str__(self):
        return f"Información adicional de {self.cliente.nombre} {self.cliente.apellido}"


#class Cliente(models.Model):
#    variable = models.IntegerField(null=False, default=None)
#    value = models.FloatField(null=True, blank=True, default=None)
#    unit = models.CharField(max_length=50)
#    place = models.CharField(max_length=50)
#    dateTime = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
 #       return '%s %s' % (self.value, self.unit)