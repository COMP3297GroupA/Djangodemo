from django.contrib import admin
from  .models import *

class AccommodationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.fetch_location_data()
        obj.distance = obj.calculate_distance()
        super().save_model(request, obj, form, change)


admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(Reservation)



