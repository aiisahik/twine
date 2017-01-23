from django.core.management.base import BaseCommand, CommandError
from account.tools import generate_random_accounts


class Command(BaseCommand):
    help = 'Creates a number of dummy user profiles'

    def add_arguments(self, parser):
        parser.add_argument('num_accounts', nargs='+', type=int)

    def handle(self, *args, **options):
        if len(options.get('num_accounts', [])) > 0:
            num_accounts = options['num_accounts'][0]
            generate_random_accounts(count=options['num_accounts'][0])
            self.stdout.write(self.style.SUCCESS('Successfully created "%s" accounts' % num_accounts))
        else:
            raise CommandError('Please include a count')
