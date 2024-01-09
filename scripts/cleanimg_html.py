#!/usr/bin/env python
#@PydevCodeAnalysisIgnore
__revision__ = "None!"
import sys,os; sys.path = [os.path.realpath(".."),os.path.realpath("../../svn")]+sys.path
os.environ["DJANGO_SETTINGS_MODULE"] = "pynoser.localsettings"
import localsettings
localsettings.finish()
import re
from reader.models    import *
from django.db.models import Q
from djutil           import db, dt

FEEDS    = [ 338, 57 ]

IMG_CONT = 'src="data:'
IMG_PATT = re.compile(r'(.*src=")(data:[^"]+?)(".*)', re.I)
IMG_FILT = Q(feed__in=FEEDS) & ( Q(text__icontains=IMG_CONT) | Q(summary__icontains=IMG_CONT))
IMG_REPL = "\\1/favicon.ico\\3"

# ...but delete Article objects do remove alle dependent objects
art = Article.objects.filter(IMG_FILT)

s = 0
for a in art:
  print(a.title)
  s += len(a.text) + len(a.summary)
  
if art.count() > 0:
  ok = raw_input("Changing {0} articles ({1}k). Continue? ".format(art.count(), s / 1024))
  if ok == 'y':
    s = 0
    for a in art:
      new, snew = IMG_PATT.sub(IMG_REPL, a.text), IMG_PATT.sub(IMG_REPL, a.summary)
      a.text = new
      a.summary = snew
      a.save()
      s += len(new) + len(snew)

    print "Modfied ({0}k left). Reorganizing...".format(s / 1024)
    db.reorg()
