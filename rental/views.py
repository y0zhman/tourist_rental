from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Equipment, Booking
from .forms import RegisterForm, BookingForm


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
    """Детальная страница снаряжения с формой бронирования"""
    item = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        # Пользователь должен быть авторизован
        if not request.user.is_authenticated:
            messages.error(request, 'Войдите, чтобы забронировать снаряжение.')
            return redirect('login')
        
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.equipment = item
            
            # Проверка: свободно ли на выбранные даты
            if not is_equipment_available(item, booking.start_date, booking.end_date):
                messages.error(
                    request, 
                    'К сожалению, на выбранные даты снаряжение уже забронировано.'
                )
            else:
                # Расчёт стоимости
                days = (booking.end_date - booking.start_date).days + 1
                booking.total_price = item.price_per_day * days
                booking.status = 'pending'
                booking.save()
                
                messages.success(
                    request, 
                    f'Бронирование создано! Сумма: {booking.total_price} ₽ за {days} дн.'
                )
                return redirect('rental:my_bookings')
        else:
            messages.error(request, 'Проверьте правильность заполнения формы.')
    else:
        form = BookingForm()
    
    context = {
        'equipment': item,
        'form': form,
    }
    return render(request, 'rental/equipment_detail.html', context)


def is_equipment_available(equipment, start_date, end_date):
    """Проверка: свободно ли снаряжение на указанные даты"""
    overlapping = Booking.objects.filter(
        equipment=equipment,
        status__in=['pending', 'confirmed', 'active'],
        start_date__lte=end_date,
        end_date__gte=start_date,
    ).exists()
    return not overlapping


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


@login_required
def my_bookings(request):
    """Страница со списком бронирований текущего пользователя"""
    bookings = Booking.objects.filter(user=request.user).select_related('equipment')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'rental/my_bookings.html', context)