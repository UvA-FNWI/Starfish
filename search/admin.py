from django.contrib import admin
from django import forms
from search.models import *
from search.widgets import TagInput


class ItemAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        # Additional save necessary to store new connections in save method
        obj.save()
        return super(ItemAdmin, self).response_add(request, obj,
                                                   post_url_continue)

    def response_change(self, request, obj):
        # Additional save necessary to store new connections in save method
        obj.save()
        return super(ItemAdmin, self).response_change(request, obj)


class TagAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "alias_of":
            kwargs["queryset"] = Tag.objects.filter(alias_of=None)
        s = super(TagAdmin, self)
        return s.formfield_for_foreignkey(db_field, request, **kwargs)


class TaggableItemAdmin(ItemAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
#        if db_field.name == "tags":
#            kwargs["widget"] = TagInput()
        s = super(TaggableItemAdmin, self)
        return s.formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Person, ItemAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(GoodPractice, TaggableItemAdmin)
admin.site.register(Information, ItemAdmin)
admin.site.register(Project, ItemAdmin)
admin.site.register(Event, ItemAdmin)
admin.site.register(Question, ItemAdmin)
admin.site.register(Comment)
admin.site.register(Glossary, ItemAdmin)
