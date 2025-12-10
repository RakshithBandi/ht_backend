import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ht_backend.settings")
django.setup()

from quiz.models import QuizSettings
from quiz.serializers import QuizSettingsSerializer

try:
    print("Checking existing settings...")
    s = QuizSettings.objects.first()
    print(f"Found: {s}")
    
    if not s:
        print("Creating settings...")
        s = QuizSettings.objects.create(is_leaderboard_visible=False)
        print(f"Created: {s} (pk={s.pk})")

    print("Toggling...")
    s.is_leaderboard_visible = not s.is_leaderboard_visible
    s.save()
    print(f"Toggled to: {s.is_leaderboard_visible}")

    print("Serializing...")
    ser = QuizSettingsSerializer(s)
    print(ser.data)
    print("SUCCESS")

except Exception as e:
    import traceback
    traceback.print_exc()
