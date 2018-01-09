from django.db import models
from django.db.models.signals import post_save,post_delete

class Weight(models.Model):
    date    = models.DateField()
    weight  = models.IntegerField()
    inc     = models.DecimalField(max_digits=6, decimal_places=1,blank=True,null=True)
    description = models.CharField(max_length=64,blank=True,default="")
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return 'Вес за %s' % (self.date)

    class Meta:
        verbose_name='Вес за день'
        verbose_name_plural='Веса'

    def save (self,*args,**kwargs):
        inc=calcInc(self)

        self.inc=inc
        super(Weight,self).save(*args,**kwargs)

def calcInc(WeightObject):
    pred = Weight.objects.filter(date__lt=WeightObject.date,is_deleted=False).order_by('-date').first()
    if pred == None:
        inc = 0
    else:
        weight_dif = WeightObject.weight - pred.weight
        days_dif = (WeightObject.date - pred.date).days
        inc = weight_dif / days_dif
    return inc

def inc_update(sender,instance,**kwargs):
    next = Weight.objects.filter(date__gt=instance.date,is_deleted=False).order_by('date').first()
    if next:
        post_save.disconnect(inc_update, sender=Weight)
        next.inc=calcInc(next)
        next.save(force_update=True)
        post_save.connect(inc_update, sender=Weight)

post_save.connect(inc_update,sender=Weight)
