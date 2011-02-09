#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Unicode test pangrams_ and optional unidecode_ module testing.

    .. _pangrams:  http://en.wikipedia.org/wiki/Pangram
    .. _unidecode: http://www.tablix.org/~avian/blog/archives/2009/01/unicode_transliteration_in_python/

>>> import sys, os, logging
>>> logging.basicConfig(level=logging.INFO)
>>> L = logging.getLogger('unicodetest.doctest')

>>> pwd = os.path.dirname(__file__)
>>>
>>> def add_sys_path(name, path, index=0):
...     path = os.path.abspath(os.path.realpath(path))
...     if not os.path.exists(path):
...         logging.warning('missing sys.path: %s [%s] (%d)' % (name, path, index))
...     elif not path in sys.path:
...         logging.info('updated sys.path: %s [%s] (%d)' % (name, path, index))
...         sys.path.insert(index, path)
...         try:
...             __import__(name) # better check via immediate zipimport
...         except ImportError:
...             logging.warning('invalid sys.path: %s [%s] (%d)' % (name, path, index))
...             sys.path.pop(index)
>>>
>>> # optionally insert $PWD/unidecode*.zip into sys.path
>>> for m in os.listdir(pwd):
...     if m.startswith('unidecode') and m.endswith('.zip'):
...         add_sys_path(os.path.splitext(m)[0][:m.find('-')], os.path.join(pwd, m))
>>>
>>> # optionally insert $PWD/unidecode/ or $PWD/../unidecode/ into sys.path
>>> for p in (pwd, os.path.join(pwd, '..')):
...     if os.path.exists(os.path.join(p, 'unidecode')):
...         add_sys_path('unidecode', p)
>>>

>>> try:
...     from unidecode import unidecode
... except ImportError, e:
...     L.warning(e)
...     unidecode = None

>>> D = locals()
>>> K = sorted(D.keys())
>>> def C(key, expected, got):
...     if expected != got:
...         L.error("Failed '%s':\\nVal: %r\\nExp: %r\\nGot: %r" % (key, D[key], expected, got))

>>> for k in K:
...     if len(k) == 2 and isinstance(D[k], basestring):
...         L.info("Testing '%s'" % k)
...         if k.islower():
...             C(k, D[k.upper()], D[k].upper()) 
...             if unidecode: C(k, D['%s_' % k.lower()], unidecode(D[k]))
...         elif k.isupper():
...             C(k, D[k.lower()], D[k].lower()) 
...             if unidecode: C(k, D['%s_' % k.lower()].upper(), unidecode(D[k]))

>>> try:
...     import os.path, yaml
...     F = '%s.yaml' % os.path.splitext(__file__)[0]
...     for k, v in yaml.load(file(F)).iteritems():   # .read().decode('utf-8')
...         C(k, D[k], v)
... except (ImportError, IOError), e:
...     L.warning(e)
"""

cz  = u'příliš žluťoučký kůň pěl ďábelské ódy'
CZ  = u'PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ PĚL ĎÁBELSKÉ ÓDY'
cz_ = u'prilis zlutoucky kun pel dabelske ody'
    # see http://cs.wikipedia.org/wiki/Pangram

if __name__ == "__main__":
    import sys, doctest
    failures, tests = doctest.testmod() 
    sys.exit(failures)
