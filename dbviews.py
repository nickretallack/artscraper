reduce_nothing = "function(keys,values){return 0}"

# this should be replaced with ?include_docs eventually
map_users = """
function(doc){
  if(doc.type == 'user'){
    emit(doc.slug, {"name":doc.name, "accounts":doc.accounts, "thumb":doc.thumb, "slug":doc.slug})
  }
}"""


map_things = """
function(doc){
  if(doc.type == 'thing'){
    emit(doc.account, {"thumb":doc.thumb, "source":doc.source})
  }
}"""

map_slugs = """
function(doc){
  if(doc.type == 'user'){
    emit(doc.slug,null)
  }
}"""

from couchdb.design import ViewDefinition as View
users  = View('users','show',map_users)
slugs  = View('users','slugs',map_slugs)
things = View('things','show',map_things)

views = [users,slugs,things]