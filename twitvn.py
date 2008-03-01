#!/usr/bin/python

from optparse import OptionParser
from urllib2 import Request, urlopen, URLError, HTTPError, HTTPBasicAuthHandler, build_opener, install_opener, HTTPPasswordMgrWithDefaultRealm
import urllib
import os
from pysvn import Revision, Client, opt_revision_kind

version = '0.1a'

class TwitHTTP:
        "This class twitters @ twitter"
        __username = None
        __password = None

        def __init__(self, username, password):
                self.__username = username
                self.__password = password

        def sendTwitter(self, message):
                twitAuth = HTTPBasicAuthHandler()
                twitAuth.add_password('Twitter API', 'http://twitter.com/statuses/',username, password)
                opener = build_opener(twitAuth)
                install_opener(opener)
                values = {'status' : message}
                data = urllib.urlencode(values)
                try:
                        f = urlopen(req)
                except IOError, e:
                        print 'We got an error'
                        print e.code

class SVNHelper:
        "This class interacts with SVN for us"
        author = None
        message = None

        def __init__(self, path, revision):
                client = Client(path)
                log_message = client.log('/', revision_start=Revision(opt_revision_kind.number, revision), limit=1).pop()
                self.auth = log_message.author
                self.message = log_message.message


# All the main stuff happens here meng.. 

def generateTwitter(author, revision, comment, domain):
        trimLength = 140 - (len(author)+1) - len(domain) - len('/changeset/') - len(revision) - 5
        if len(comment) > trimLength:
                comment = comment[0:trimLength].rstrip(' ') + '...'
        return '%s: %s %s/changeset/%s' % (author, comment, domain, revision)

def processArgs():
        # get arguments from the command line
        # important arguments are username, password, comment

        usage = 'usage: %prog -u<username> -p<password> -f<svn_path> -r<svn_revision> -t<trac_url>'

        parser = OptionParser(usage=usage,version='%prog: ' + version)
        parser.add_option('-u', '--twitter-username', dest='username', type='string',
                help='Twitter Account Username',
                action='store')
        parser.add_option('-p', '--twitter-password', dest='password', type='string',
                help='Twitter Account Password',
                action='store')
        parser.add_option('-f', '--svn-path', dest='path', type='string',
                help='SVN Repository Path',
                action='store')
        parser.add_option('-r', '--svn-revision', dest='revision', type='string',
                help='SVN Revision',
                action='store')
        parser.add_option('-t', '--tracurl', dest='domain', type='string',
                help='Trac URL',
                action='store')

        (options, args) = parser.parse_args()

        if options.username is None:
                parser.error('Twitter username must be set')
        else:
                username = options.username

        if options.password is None:
                parser.error('Twitter password must be set')
        else:
                password = options.password

        if options.path is None:
                parser.error('Subversion repo path must be set')
        else:
                path = options.path

        if options.revision is None:
                parser.error('subversion revision must be set')
        else:
                revision = options.revision

        if options.domain is None:
                parser.error('Trac Domain Name must be set')
        else:
                domain = options.domain

        return (username, password, path, revision, domain)

(username, password, path, revision, domain) = processArgs()
svnHelper = SVNHelper(path, revision)
if svnHelper.author is None:
        svnHelper.author = os.environ['USER']

twitter = generateTwitter(svnHelper.author, revision, svnHelper.message, domain)

print twitter

#TwitHTTP(username, password).sendTwitter(twitter)
