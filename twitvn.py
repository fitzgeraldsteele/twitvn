#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from optparse import OptionParser
from urllib2 import Request, HTTPPasswordMgrWithDefaultRealm, build_opener, install_opener, urlopen, HTTPBasicAuthHandler
import urllib
import svn.repos
import svn.fs
import svn.core

version = '0.1a'

class TwitHTTP:
        "This class twitters @ twitter"
        __username = None
        __password = None

        def __init__(self, username, password):
                self.__username = username
                self.__password = password


        def sendTwitter(self, message):
                req = Request('http://twitter.com/statuses/update.json')
                twitAuth = HTTPPasswordMgrWithDefaultRealm()
                twitAuth.add_password(None, 'twitter.com', self.__username, self.__password)
                # install the auth handler built from the HTTPPasswordMgrWithDefaultRealm password manager
                install_opener(build_opener(HTTPBasicAuthHandler(twitAuth)))
                data = urllib.urlencode({'status' : message})
                try:
                        urlopen(req, data)
                except IOError, e:
                        print 'We got an error'
                        print e.code

class SVNHelper:
        "This class interacts with SVN for us"

        def __init__(self, path, revision, pool):
                repos_ptr = svn.repos.svn_repos_open(path, pool)
                fs_ptr = svn.repos.svn_repos_fs(repos_ptr)
                self.message = svn.fs.revision_prop(fs_ptr, revision, svn.core.SVN_PROP_REVISION_LOG, pool)
                self.author = svn.fs.revision_prop(fs_ptr, revision, svn.core.SVN_PROP_REVISION_AUTHOR, pool)


def generateTwitter(author, revision, comment, domain):
        trimLength = 140 - (len(author)+1) - len(domain) - len('/changeset/') - len(str(revision)) - 5
        if len(comment) > trimLength:
                comment = comment[0:trimLength].rstrip(' ') + '...'
        return '%s: %s %s/changeset/%s' % (author, comment, domain, revision)

def main(pool, options):
        svnHelper = SVNHelper(options.PATH, options.REVISION, pool)

        twitter = generateTwitter(svnHelper.author, options.REVISION, svnHelper.message, options.DOMAIN)

        #print twitter

        TwitHTTP(options.USERNAME, options.PASSWORD).sendTwitter(twitter)

if __name__ == '__main__':
        # get arguments from the command line
        # important arguments are username, password, comment

        usage = 'usage: %prog -u<username> -p<password> -f<svn_path> -r<svn_revision> -t<trac_url>'

        parser = OptionParser(usage=usage,version='%prog: ' + version)
        parser.add_option('-u', '--twitter-username', dest='USERNAME', type='string',
                help='Twitter Account Username',
                action='store')
        parser.add_option('-p', '--twitter-password', dest='PASSWORD', type='string',
                help='Twitter Account Password',
                action='store')
        parser.add_option('-f', '--svn-path', dest='PATH', type='string',
                help='SVN Repository Path',
                action='store')
        parser.add_option('-r', '--svn-revision', dest='REVISION', type='int',
                help='SVN Revision',
                action='store')
        parser.add_option('-t', '--tracurl', dest='DOMAIN', type='string',
                help='Trac URL',
                action='store')

        (options, args) = parser.parse_args()

        if options.USERNAME is None:
                parser.error('Twitter username must be set')

        if options.PASSWORD is None:
                parser.error('Twitter password must be set')

        if options.PATH is None:
                parser.error('Subversion repo path must be set')

        if options.REVISION is None:
                parser.error('subversion revision must be set')

        if options.DOMAIN is None:
                parser.error('Trac Domain Name must be set')

        svn.core.run_app(main, options=options)
