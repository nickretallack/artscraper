def user_url(user):
  return '/%s' % user

import jinja2
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), line_statement_prefix="#")
env.filters['user_url'] = user_url


def render(template,**args):
  print env.get_template(template+'.html').render(**args)
