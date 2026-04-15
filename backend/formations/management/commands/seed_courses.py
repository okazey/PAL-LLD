from django.core.management.base import BaseCommand

from formations.models import Course


COURSES = [
    {
        "title": "Comment préparer le sol",
        "description": "Les bases pour préparer ton sol avant la saison.",
        "language": "FR",
        "type": "audio",
        "content_url": "https://www.w3schools.com/html/horse.mp3",
        "thumbnail_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=400&h=250&fit=crop",
        "duration_minutes": 15,
        "difficulty": "beginner",
    },
    {
        "title": "Réduire les pesticides",
        "description": "3 gestes simples pour réduire les pesticides au champ.",
        "language": "FR",
        "type": "video",
        "content_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "thumbnail_url": "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400&h=250&fit=crop",
        "duration_minutes": 25,
        "difficulty": "intermediate",
    },
    {
        "title": "Bien arroser",
        "description": "Quand et comment arroser pour limiter le stress hydrique.",
        "language": "FR",
        "type": "audio",
        "content_url": "https://www.w3schools.com/html/horse.mp3",
        "thumbnail_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=250&fit=crop",
        "duration_minutes": 10,
        "difficulty": "beginner",
    },
    {
        "title": "Suq na suuf bi",
        "description": "Njàngu ngir waññi suuf bi ba tey jëfandikoo pesticide yu bari.",
        "language": "WOLOF",
        "type": "audio",
        "content_url": "https://www.w3schools.com/html/horse.mp3",
        "thumbnail_url": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=400&h=250&fit=crop",
        "duration_minutes": 20,
        "difficulty": "beginner",
    },
]


class Command(BaseCommand):
    help = "Seed the database with default courses (FR + WOLOF)"

    def handle(self, *args, **options):
        updated = 0
        created = 0
        for data in COURSES:
            course, is_new = Course.objects.get_or_create(
                title=data["title"],
                defaults=data,
            )
            if is_new:
                created += 1
            else:
                # Update existing course with new fields
                for key, value in data.items():
                    setattr(course, key, value)
                course.save(update_fields=list(data.keys()))
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"{created} course(s) created, {updated} updated."))
