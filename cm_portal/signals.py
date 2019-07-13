from .models import MedicalSupply, Charge
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Charge)
def charge_medicalsupply(sender, instance, **kwargs):    
    medical_supply = MedicalSupply.objects.get(id=instance.item.id)
    medical_supply.stocks_available -= instance.quantity
    medical_supply.save()

@receiver(post_delete, sender=Charge)
def uncharge_medicalsupply(sender, instance, **kwargs):
    medical_supply = MedicalSupply.objects.get(id=instance.item.id)
    medical_supply.stocks_available += instance.quantity
    medical_supply.save()
