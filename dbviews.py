reduce_nothing = "function(keys,values){return 0}"

map_things = """
function(doc){
  if(doc.type == 'image'){
    emit([doc.account,doc.site],{"thumb":doc.thumb, "source":doc.source, "title":doc.title, "site":doc.site})
  }
}"""

map_users = """
function(doc){
  if(doc.type == 'user'){
    emit(doc.name, {"name":doc.name, "accounts":doc.accounts})
  }
}"""


map_things = """
function(doc){
  if(doc.type == 'thing'){
    emit([doc.account,doc.site], {"thumb":doc.thumb, "source":doc.source})
  }
}"""