function make_tagit(id, delim){
    $("#"+id).tagit({
        caseSensitive: false,
        singleFieldDelimiter: delim,
        autocomplete:{
            source: function(search, cb){
                $.ajax({
                    url: "/autocomplete?q="+encodeURIComponent(search.term),
                    context: this
                }).done(
                    function(choices){
                        cb(this._subtractArray(choices, this.assignedTags()))
                    })
            }
        }
    })
}
