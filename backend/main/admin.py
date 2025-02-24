from django.contrib import admin
from .models import Profile, Store, MoneyCode,Galeri,Quiz,Product

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'achived', 'code', 'display_image')

    # Görselin küçük bir önizlemesini admin panelinde göster
    def display_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50"/>'
        return "No Image"
    display_image.allow_tags = True
    display_image.short_description = "Image"

admin.site.register(Profile)
admin.site.register(MoneyCode)
admin.site.register(Galeri)
admin.site.register(Quiz)
admin.site.register(Product)