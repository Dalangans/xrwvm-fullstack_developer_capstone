import os  # noqa: E402
import django  # noqa: E402

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()

from djangoapp.models import CarMake, CarModel

print("CarMake count:", CarMake.objects.count())
print("CarModel count:", CarModel.objects.count())
for cm in CarModel.objects.all():
    print(f"  - {cm.name} ({cm.make.name})")
