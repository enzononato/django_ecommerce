from django.contrib import admin
from .models import Product
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag', 'created_by')
    readonly_fields = ('created_by', 'slug',)  # torna o campo 'created_by' somente leitura, evitando alteração por parte do usuário
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def image_tag(self, obj): #Renderiza a imagem em miniatura na lista de produtos.
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Image'
    
    def delete_image_button(self, obj): #Renderiza o botão de exclusão da imagem ao lado do produto.
        if obj.image:
            return format_html('<a class="button" href="{}">Delete Image</a>', self.get_delete_image_url(obj.id))
        return "-"
    delete_image_button.short_description = 'Delete Image'
    delete_image_button.allow_tags = True

    def get_delete_image_url(self, obj_id): #Gera a URL para a ação de exclusão da imagem.
        return reverse('admin:delete_product_image', args=[obj_id])
    
    def get_urls(self): #Adiciona uma URL personalizada para a ação de exclusão da imagem.
        urls = super().get_urls()
        custom_urls = [
            path('delete-image/<int:product_id>/', self.admin_site.admin_view(self.delete_image), name='delete_product_image'),
        ]
        return custom_urls + urls

    def delete_image(self, request, product_id): #Lida com a lógica de exclusão da imagem do produto e exibe uma mensagem de sucesso.
        product = self.get_object(request, product_id)
        if product.image:
            product.image.delete()
            product.save()
            self.message_user(request, "Image deleted successfully.")
        return redirect('admin:products_product_changelist')

admin.site.register(Product, ProductAdmin)