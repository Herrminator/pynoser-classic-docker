from __future__ import print_function
import os, sys, argparse, socket; sys.path = [os.path.realpath("..")]+sys.path

from pip._vendor      import html5lib
from urlparse         import urlsplit, urlunsplit
from runtime          import settings #@UnusedImport
from reader.models    import Feed
from reader           import feed

DEBUG   = True
LOGFILE = sys.stderr

class PseudoFeed(object):
    etag = None
    lastMod = None

def fetch(url, debug=None):
    if debug is None: debug = DEBUG
    pseudo = PseudoFeed()
    if debug:
        print("FETCH:", url, file=LOGFILE)
    return feed.fetchPage(pseudo, url)

def find_icon(f):
    
    page = f.link if f.feedType != feed.HTML else f.url
    if not page:
        return None
    split = urlsplit(page)

    # first, try the simple favicon.ico - that's enough for me
    icon = urlunsplit((split.scheme, split.netloc, "favicon.ico", None, None))
    data, info, err = fetch(icon)
    if data and not err:
        return icon
    elif DEBUG:
        print(data, err, file=LOGFILE)

    # now, try to parse the web page
    data, info, err = fetch(page)
    if data and not err:
        # html = html5lib.parse(data, treebuilder="etree")
        # https://stackoverflow.com/a/20817495/10545609
        import xml.etree.ElementTree as etree
        tb = html5lib.getTreeBuilder("etree", implementation=etree)
        parser = html5lib.HTMLParser(tb, namespaceHTMLElements=False)
        html = parser.parse(data)

        for attr in [ "icon", "shortcut icon", ]:
            link = html.find("./head/link[@rel='{0}']".format(attr))
            if link is not None:
                lsplit = list(urlsplit(link.attrib["href"]))
                if not lsplit[0]: lsplit[0] = split.scheme
                if not lsplit[1]: lsplit[1] = split.netloc
                icon = urlunsplit(lsplit)
                data, info, err = fetch(icon)
                if data and not err:
                    return icon
                elif DEBUG:
                    print(data, err, file=LOGFILE)
        return None
    elif DEBUG:
        print(data, err, file=LOGFILE)
    
    return None

def main(argv=sys.argv):
    ap = argparse.ArgumentParser()
    ap.add_argument(      "feeds",   nargs="*", type=int)
    ap.add_argument("-a", "--all",   default=False, action="store_true")
    ap.add_argument("-c", "--clear", default=False, action="store_true", help="Clear missing or erroneous icons")
    ap.add_argument("-d", "--debug", default=False, action="store_true")
    ap.add_argument("-D", "--dry",   default=False, action="store_true")
    args = ap.parse_args()

    global DEBUG
    DEBUG = args.debug

    socket.setdefaulttimeout(20.0)

    feeds = Feed.objects.select_related().order_by("id")
    if args.feeds:
        feeds = feeds.filter(id__in=args.feeds)

    for f in feeds:
        if f.isActive() or args.all:
            fstatus = f.status()
            icon = fstatus.icon
            print("{0.id:4} {0.title:40.40} {1:72.72}".format(f, icon), end="")
            status = "ok"
            if f.feedType not in [ feed.FEED, feed.HTML ]:
                status = "no" # Only for RSS and HTML feeds
            elif icon is None or icon == "":
                status = "empty"
            else:
                fetched, info, err = fetch(icon, debug=False)
                if err:
                    status = "ERROR"
                elif not fetched:
                    status = "empty"
            print("{0}.".format(status))
            if status not in  [ "ok", "no" ]:
                neew = find_icon(f)
                print("{0.id:4} {1:40.40} {2:72.72}".format(f, "-->", neew), end="")
                if neew is not None:
                    status = "new"
                if (neew is not None or args.clear) and not args.dry:
                    fstatus.icon = neew
                    fstatus.save()
                print("{0}.".format(status))


if __name__ == "__main__":
  main()
