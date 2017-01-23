from django.contrib import admin

from models import Battle, Player

admin.site.register(Battle,
    search_fields=('winner__first_name', 'winner__last_name', 'loser__last_name', 'winner__first_name'),
    list_display=('create_date', 'left', 'right', 'winner', 'loser'),
    list_display_links=('create_date', 'left', 'right', 'winner', 'loser'),
    list_filter = ('winner', 'loser')
)

admin.site.register(Player,
    search_fields=('target__first_name', 'target__last_name'),
    list_display=('judge', 'target', 'mu', 'sigma', 'elo'),
    list_display_links=('judge', 'target', 'mu', 'sigma', 'elo'),
)
# Register your models here.
