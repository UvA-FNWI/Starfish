from django.forms import widgets
from search.utils import parse_query
from search.models import Tag
from steep.settings import SEARCH_SETTINGS

class TagInput(widgets.Widget):
    class Media:
        js = ('jquery-2.0.3.min.js','jquery-ui.min.js', 'tag-it.js', 'tagit_search_input.js')
        css = {'all': ('jquery-ui-1.10.3.custom.css', 'jquery.tagit.css')}

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        tid = "id_" + name
        delim = SEARCH_SETTINGS['syntax']['DELIM']
        tsymb = SEARCH_SETTINGS['syntax']['TAG']
        if value is None:
            value = ''
        else:
            value = delim.join([tsymb+t.handle for t in \
                    Tag.objects.filter(id__in=value)])
        script = "<script type='text/javascript'>"
        script += "$(function(){make_tagit(\"%s\",\"%s\");})" % (tid, delim)
        script += "</script>"
        return script+"<input type='text' name='%s' id='%s' value='%s' />" %\
            (name, tid, value)

    def value_from_datadict(self, data, files, name):
        raw_value = data.get(name, None)
        if raw_value is not None:
            tag_tokens, person_tokens, literal_tokens = parse_query(raw_value)
            tags = Tag.objects.filter(handle__in = tag_tokens)
            return [ tag.id for tag in tags ]
        else:
            return None
