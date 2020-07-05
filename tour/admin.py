from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

from weasyprint import HTML
import tempfile

from .models import *

@admin.register(Booking)
class BookingAdmin(ImportExportModelAdmin):
  list_display = ('id', 'profile', 'tour', 'status_booking', 'booking_time', 'people_number', 'total_price')
  list_per_page = 10
  actions = ['print_bill', ]

  def print_bill(self, request, queryset):
    booking = queryset.first
    # Rendered
    html_string = render_to_string('bill.html', {'booking': booking})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response

  print_bill.short_description = "Print bill"

@admin.register(Photo)
class PhotoAdmin(ImportExportModelAdmin):
  list_display = ('tour', 'image')

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
  list_display = ('content', 'date')
  list_per_page = 10

@admin.register(Destination)
class DestinationAdmin(ImportExportModelAdmin):
 list_display = ('id', 'location_from', 'location_to',
                 'destination_name', 'area')
 list_per_page = 10

@admin.register(Tour)
class TourAdmin(ImportExportModelAdmin):
 list_display = ('id', 'tour_name', 'experience_time', 'price', 'start_day',
                 'end_day', 'min_age', 'max_people', 'status_evaluete', 'short_tour_detail')
 list_per_page = 10

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
  list_display = ('id', 'slider_image', 'title', 'teaser')
  list_per_page = 10

@admin.register(Area)
class AreaAdmin(ImportExportModelAdmin):
 list_display = ('area_name', 'image')


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
  list_display = ('title', 'content', 'date', 'tag', 'image')
  list_per_page = 10

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
