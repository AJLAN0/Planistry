import os
import django

# عشان تجهز Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planistry.settings')
django.setup()

from users.models import User, UserPreferences

def create_initial_users():
    users_data = [
        {
            "email": "admin@gmail.com",
            "username": "admin",
            "password": "Admin123",
            "first_name": "Admin",
            "last_name": "User"
        },
    ]
    for data in users_data:
        if not User.objects.filter(email=data["email"]).exists():
            user = User(
                email=data["email"],
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            user.set_password(data["password"])
            user.save()
            UserPreferences.objects.create(user=user)
            print(f"User {user.email} created.")
        else:
            print(f"User {data['email']} already exists.")

if __name__ == "__main__":
    create_initial_users()
