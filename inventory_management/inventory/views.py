from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, ItemFilterForm
from .models import InventoryItem, Category
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
    template_name = 'inventory/index.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

        low_inventory = InventoryItem.objects.filter(
            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY
        )
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item have low inventory')
        low_inventory_ids = InventoryItem.objects.filter(
            user = self.request.user.id,
            quantity__lte = LOW_QUANTITY
        ).values_list('id', flat = True)
    
        return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})
        
    def post(self, request):
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            
            login(request, user)
            return redirect('index')
        
        return render(request, 'inventory/signup.html', {'form':form})
    
class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')
    
class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'


class ItemFilter(LoginRequiredMixin, View):
    def get(self, request):
        # Captura o valor do parâmetro 'name' da URL
        name = request.GET.get('name', '')

        # Filtra os itens com base no usuário
        items = InventoryItem.objects.filter(user=request.user).order_by('id')

        # Aplica o filtro de nome, se o valor 'name' for fornecido
        if name:
            items = items.filter(name__icontains=name)

        # Obtém IDs de itens com baixo estoque
        low_inventory_ids = items.filter(quantity__lte=LOW_QUANTITY).values_list('id', flat=True)

        context = {
            'items': items,
            'low_inventory_ids': low_inventory_ids,
            'name': name,  # Passa o valor do campo de input para o template
        }
        
        return render(request, 'inventory/item_filter.html', context)