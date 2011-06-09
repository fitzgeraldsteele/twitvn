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
import git
import tweepy

name = 'twitvn-git'
version = '2.1'

CONSUMER_KEY = 'Enter consumer key here'
CONSUMER_SECRET = 'Enter consumer secret here'
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

class GITHelper:
	"This class interacts with GIT for us"
	def __init__(self, path):
		repo = git.Repo(path)
		headcommit = repo.head.commit
		self.message = headcommit.message
		self.author = headcommit.author.name


def generateTwitter(author, comment):
	tweet = ''
	tracurl = ''
	trimLength = 140 - (len(author)+1) - 5
		
	if len(comment) > trimLength:
		comment = comment[0:trimLength].rstrip(' ') + '...'
		
	tweet = '%s: %s %s' % (author, comment, tracurl)
	return tweet

def main(options):
	# Get SVN info
	gitHelper = GITHelper(options.PATH)
	# Generate a tweet
	twitter = generateTwitter(gitHelper.author, gitHelper.message)
	# Send it to twitter
	TwitOAuth(twitter).sendTwitter()

if __name__ == '__main__':
	# get arguments from the command line

	usage = 'usage: %prog -f<git_path>'

	parser = OptionParser(usage=usage,version='%prog: ' + version)
	
	parser.add_option('-f', '--git-path', dest='PATH', type='string',
		help='GIT Repository Path', action='store')

	(options, args) = parser.parse_args()

	if options.PATH is None:
		parser.error('GIT repo path must be set')

	main(options)
