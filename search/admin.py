from django.contrib import admin
from models import *

class TagAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "alias_of":
            kwargs["queryset"] = Tag.objects.filter(alias_of=None)
        return super(TagAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Person)
admin.site.register(Tag, TagAdmin)
admin.site.register(GoodPractice)
admin.site.register(Information)
admin.site.register(Project)
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Comment)
