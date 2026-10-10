from django.shortcuts import render, get_object_or_404
from .models import Category, Equipment


def home(request):
    """Главная страница"""
    return render(request, 'rental/home.html')


def equipment_list(request):
    """Каталог снаряжения с фильтром по категориям"""
    categories = Category.objects.all()
    equipment = Equipment.objects.filter(is_active=True)
    
    category_id = request.GET.get('category')
    current_category = None
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        equipment = equipment.filter(category=current_category)
    
    context = {
        'categories': categories,
        'equipment_list': equipment,
        'current_category': current_category,
    }
    return render(request, 'rental/equipment_list.html', context)


def equipment_detail(request, pk):
    """Детальная страница снаряжения"""
    item = get_object_or_404(Equipment, pk=pk)
    context = {
        'equipment': item,
    }
    return render(request, 'rental/equipment_detail.html', context)

from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import RegisterForm


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect('rental:home')
    else:
        form = RegisterForm()
    
    return render(request, 'rental/register.html', {'form': form})