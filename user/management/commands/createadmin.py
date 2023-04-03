from django.core.management.base import BaseCommand

from user.models import CustomUser


class Command(BaseCommand):
    help = 'Crea un nuovo amministratore per un\'app specifica.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--app', type=str, help='Nome dell\'applicazione.')

    def handle(self, *args, **options):
        app = str(options.get('app')).lower()
        if app:
            self.stdout.write(f"Crea un nuovo amministratore per l'app {app}.")
            self.stdout.write("Inserisci i dati richiesti.")
            email = input("Email: ")
            CustomUser.objects.create_superuser(email=email, app=app, app_role=f"admin_{app}")
            self.stdout.write(self.style.SUCCESS(f"Amministratore per l'app {app} creato con successo."))
        else:
            self.stdout.write(f"Crea un nuovo amministratore per tutte le app")
            self.stdout.write("Inserisci i dati richiesti.")
            email = input("Email: ")
            CustomUser.objects.create_superuser(email=email, app=app, app_role=f"admin_{app}")
            self.stdout.write(self.style.SUCCESS(f"Amministratore per tutte le app creato con successo."))
