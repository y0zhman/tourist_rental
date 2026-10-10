from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from .models import Booking


class RegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя"""
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap-классы ко всем полям
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class BookingForm(forms.ModelForm):
    """Форма бронирования снаряжения"""
    
    class Meta:
        model = Booking
        fields = ('start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
        }
        labels = {
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
        }
    
    def clean(self):
        """Валидация: проверка дат"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        # 1. Обе даты должны быть заполнены
        if not start_date or not end_date:
            raise forms.ValidationError('Заполните обе даты.')
        
        # 2. Дата начала не может быть в прошлом
        if start_date < date.today():
            self.add_error('start_date', 'Дата начала не может быть в прошлом.')
        
        # 3. Дата окончания должна быть позже даты начала
        if end_date < start_date:
            self.add_error('end_date', 'Дата окончания должна быть позже даты начала.')
        
        return cleaned_data
    
    def clean_end_date(self):
        """Проверка: не слишком длинная аренда (макс. 30 дней)"""
        end_date = self.cleaned_data.get('end_date')
        start_date = self.data.get('start_date')
        
        if end_date and start_date:
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            days = (end_date - start).days + 1
            if days > 30:
                raise forms.ValidationError('Максимальный срок аренды — 30 дней.')
        
        return end_date