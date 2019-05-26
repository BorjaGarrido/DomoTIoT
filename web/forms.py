from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class registroForm(UserCreationForm):
    class Meta:
        model = User
        field = ['username',
                'first_name',
                'last_name',
                'email',]
        labels = {'username': 'Nickname' ,
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'email': 'Correo electronico',}
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined' ,'password']
