from django.contrib import admin
from django import forms
from search.models import *
from search.widgets import TagInput


class TagAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "alias_of":
            kwargs["queryset"] = Tag.objects.filter(alias_of=None)
        s = super(TagAdmin, self)
        return s.formfield_for_foreignkey(db_field, request, **kwargs)


class TaggableItemAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
#        if db_field.name == "tags":
#            kwargs["widget"] = TagInput()
        s = super(TaggableItemAdmin, self)
        return s.formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Person)
admin.site.register(Tag, TagAdmin)
admin.site.register(GoodPractice, TaggableItemAdmin)
admin.site.register(Information)
admin.site.register(Project)
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Glossary)

