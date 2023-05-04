from django.contrib import admin
from .models import *

# Этот файл служит для того, чтобы регистрировать в админ-панели наши созданные модели
# Поясню: так мы сможем добавлять, редактировать и удалять все модели которые только могут быть в нашей базе данных
# Перейдя по http://127.0.0.1:8000/admin/ точно всё поймёшь)

admin.site.register(Client)
admin.site.register(Deposit)
admin.site.register(DepositType)
admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(Passport)
admin.site.register(Address)
admin.site.register(Registration)

