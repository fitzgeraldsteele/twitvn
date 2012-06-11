Twitter Setup

You need to set up your own Twitter app for this script to work.

    Go to this site: https://dev.twitter.com/apps/new
    Set up an app, and then enter the consumer secret/consumer key into twitvn.py and auth.py 

Pre-installation

You will need to install tweepy (and simpleJSON if you have python 2.5, it's included with 2.6)

    easy_install simplejson (python 2.5 only)
    easy_install tweepy
    For GIT: easy_install gitpython 

Installation

    Make a TwitVN folder in the SVN or GIT hooks folder
    Put twitvn.py (or twitvn-git.py) and auth.py into the TwitVN folder
    For SVN:
        Add the following line to post-commit in the SVN hooks folder (trac is optional)

        python /path/to/svn/repo/hooks/TwitVN/twitvn.py -f "${REPOS}" -r "${REV}" -t "<url for trac>"

    For GIT:
        Add the following line to update in the GIT hooks folder

        echo "-o ${2} -n ${3}" > twitvn.tmp

        Add the following line to post-update in the GIT hooks folder

        DIR=$(cd `dirname $0` && pwd)
        PARENT=`dirname $DIR`
        python "${PARENT}"/hooks/twitvn/twitvn-git.py -f "${PARENT}" `cat twitvn.tmp`
        rm twitvn.tmp

OAuth Setup

In order for TwitVN to post to Twitter it must be authorized to your account. To do this follow the instructions below.

    Go into the TwitVN folder, and launch the auth.py script

    python auth.py

    The script will print a URL, copy and paste that into your browser
    Login to twitter, and authorize the TwitVN app
    Enter the PIN number given in the browser into the python script
    The python script will print out an Access Key and an Access Secret
    Copy these 2 keys into the twitvn.py script: