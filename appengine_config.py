import os
import sys
from google.appengine.ext import vendor

vendor.add('lib')

if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine'):
  sys.path.insert(0, 'lib.zip')
else:
  if os.name == 'nt':
    os.name = None
    sys.platform = ''

  import re
 # from google.appengine.tools.devappserver2.python import stubs
 # from google.appengine.tools.devappserver2.python.runtime import stubs
  from google.appengine.tools.devappserver2.python import runtime

#  re_ = stubs.FakeFile._skip_files.pattern.replace('|^lib/.*', '')
  re_ = runtime.stubs.FakeFile._skip_files.pattern.replace('|^lib/.*', '')
  re_ = re.compile(re_)
#  stubs.FakeFile._skip_files = re_
  runtime.stubs.FakeFile._skip_files = re_
  sys.path.insert(0, 'lib')
sys.path.insert(0, 'libx')


def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = recording.appstats_wsgi_middleware(app)
  return app