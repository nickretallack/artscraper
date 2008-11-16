map_users = """
function(doc){
  emit(doc.user,null)
}"""

reduce_nothing = """
function(keys,values){return 0}"""

map_things = """
function(doc){
  emit(doc.user,{"thumb":doc.thumb, "source":doc.source, "title":doc.title, "site":doc.site})
}"""
