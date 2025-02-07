from .models import User

class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
             user = User.objects.get(email=username)
             if user.check_password(password):
                 return user
        except (User.DoesNotExist.MultipleObjectsReturned):
            return None
        

def get_user(self, slug_user):
    try:
        return User.objects.get(pk = slug_user)
    except User.DoesNotExist:
        return None
