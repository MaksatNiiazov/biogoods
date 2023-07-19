from django.contrib import admin
from user_auth.models import User



@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("company", "first_name", "phone_number", 'discount', 'total_amount', 'joined_date',
                    'disabled')
    fields = ('company', 'first_name', 'last_name', 'phone_number', 'email', 'discount', 'total_amount', 'joined_date')
    list_filter = ('discount', 'total_amount', 'joined_date')
    list_display_links = ("first_name",)
    list_editable = ('disabled',)

    model = User
