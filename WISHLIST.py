# get plone site
from plone import api
site = api.get_site()


# create content
site['foo'] = api.create_content('Folder', title='Foo')
site['bar'] = api.create_content('Folder', title='Bar')
site.bar['doc'] = api.create_content('Page', title='Doc')

# move content (works)
site.foo['doc'] = site.bar.pop('doc')

# copy content
site.bar['test'] = api.copy(site.foo.doc)

# delete content (works)
del site.bar['test']


# get user
noob = api.users['noob']

# create user
api.create_user('bob', firstname='Bob')

# delete user
del api.users['bob']
