from django.contrib import admin
from .models import *


admin.site.register(company)
admin.site.register(car_model)
admin.site.register(generations)
admin.site.register(engines)
admin.site.register(engine_params)

