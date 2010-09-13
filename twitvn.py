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
#
# This program uses the Tweepy library (http://joshthecoder.github.com/tweepy)

from optparse import OptionParser
import svn.repos
import svn.fs
import svn.core
import tweepy

name = 'twitvn'
version = '2.0'

CONSUMER_KEY = 'Ck4MU5UrHqKvHpl9fLhCzw'
CONSUMER_SECRET = 'F0uhzfE58VdSuZhqgEkFknFQCdDDFKapYKL8C9LCJU'
ACCESS_KEY = 'Enter access key here'
ACCESS_SECRET = 'Enter access secret here'

class TwitOAuth:
	"This class tweets via OAuth"
	__tweet = None

	def __init__(self, message):
		self.__tweet = message
		
	def sendTwitter(self):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		api.update_status(self.__tweet)

class SVNHelper:
	"This class interacts with SVN for us"
	def __init__(self, path, revision, pool):
		repos_ptr = svn.repos.svn_repos_open(path, pool)
		fs_ptr = svn.repos.svn_repos_fs(repos_ptr)
		self.message = svn.fs.revision_prop(fs_ptr, revision, svn.core.SVN_PROP_REVISION_LOG, pool)
		self.author = svn.fs.revision_prop(fs_ptr, revision, svn.core.SVN_PROP_REVISION_AUTHOR, pool)


def generateTwitter(author, revision, comment, domain=''):
	tweet = ''
	tracurl = ''
	trimLength = 140 - (len(author)+1) - 5

	# if there's a trac domain, count that as well
	if domain:
		tracurl = '/'.join([domain,'changeset',str(revision)])
		trimLength -= len(tracurl)
		
	if len(comment) > trimLength:
		comment = comment[0:trimLength].rstrip(' ') + '...'
		
	tweet = '%s: %s %s' % (author, comment, tracurl)
	return tweet

def main(pool, options):
	# Get SVN info
	svnHelper = SVNHelper(options.PATH, options.REVISION, pool)
	# Generate a tweet
	twitter = generateTwitter(svnHelper.author, options.REVISION, svnHelper.message, options.DOMAIN)
	# Send it to twitter
	TwitOAuth(twitter).sendTwitter()

if __name__ == '__main__':
	# get arguments from the command line
	# important arguments are username, password, comment

	usage = 'usage: %prog -f<svn_path> -r<svn_revision> [-t<trac_url>]'

	parser = OptionParser(usage=usage,version='%prog: ' + version)
	
	parser.add_option('-f', '--svn-path', dest='PATH', type='string',
		help='SVN Repository Path', action='store')
		
	parser.add_option('-r', '--svn-revision', dest='REVISION', type='int',
		help='SVN Revision', action='store')
		
	parser.add_option('-t', '--tracurl', dest='DOMAIN', type='string',
		help='Trac URL', action='store')

	(options, args) = parser.parse_args()

	if options.PATH is None:
		parser.error('Subversion repo path must be set')

	if options.REVISION is None:
		parser.error('subversion revision must be set')

#	if options.DOMAIN is None:
#		parser.error('Trac Domain Name must be set')

	svn.core.run_app(main, options=options)
