import os
import django
from djangoapp.models import CarMake, CarModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()

print("CarMake count:", CarMake.objects.count())
print("CarModel count:", CarModel.objects.count())
for cm in CarModel.objects.all():
    print(f"  - {cm.name} ({cm.make.name})")
