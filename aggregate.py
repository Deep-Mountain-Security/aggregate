########################################################################################
#
#                                                   _         _____       
#             /\                                   | |       |  __ \      
#            /  \   __ _  __ _ _ __ ___  __ _  __ _| |_ ___  | |__) |   _ 
#           / /\ \ / _` |/ _` | '__/ _ \/ _` |/ _` | __/ _ \ |  ___/ | | |
#          / ____ \ (_| | (_| | | |  __/ (_| | (_| | ||  __/_| |   | |_| |
#         /_/    \_\__, |\__, |_|  \___|\__, |\__,_|\__\___(_)_|    \__, |
#                   __/ | __/ |          __/ |                       __/ |
#                  |___/ |___/          |___/                       |___/ 
#
########################################################################################
#
# AGGREGATE.PY
#
# Jordan Jenkins
# Deep Mountain Security
# 
# 03.01.2018
#
#
#
# An RSS feeds aggregator in Python that outputs an HTML file. It is reccommended that
# it be run on a cron job, etc.
#
#
#
########################################################################################
#
# REQUIREMENTS:
#
#       Python (duh)
#       feedparser library (for retrieving and parsing rss feeds)
#       pytz library (for working with timezones)
#       a webserver (if you want to host your html file)
#
########################################################################################
#
# NOTES:
#
#       When running this script, make sure that it executes in the web server folder,
#   or modify it to use custom file paths to make sure that the output is in the
#   correct location.
#
########################################################################################
########################################################################################
########################################################################################

# import important stuff
import feedparser                           # needed for parsing of RSS feeds
from datetime import datetime               # for date and time display
import socket                               # for timeouts
import time                                 # for localtime
from operator import attrgetter             # for sorting lists
from pytz import timezone                   # for timezone conversion

# Variable that determines how many most recent posts will be in the HTML output
postsToDisplay = 75

# time zone config - currently using mountain time, or MST
mountain = timezone('US/Mountain')
gmt = timezone('GMT')

# LIST of feeds to aggregate (Change this as needed):
feedsList = ['https://krebsonsecurity.com/feed/',\
'http://www.f-secure.com/weblog/weblog.rss',\
'https://technet.microsoft.com/en-us/security/rss/bulletin',\
'https://www.darkreading.com/rss_simple.asp',\
'https://www.schneier.com/blog/atom.xml',\
'https://www.grahmcluley.com/feed/',\
'http://securityaffairs.co/wordpress/feed',\
'https://www.us-cert.gov/ncas/all.xml',\
'http://feeds.feedburner.com/TheHackersNews',\
'https://www.itproportal.com/rss/',\
'http://zdnet.com/blog/security/rss.xml',\
'https://hotforsecurity.bitdefender.com/feed',\
'http://feeds.feedburner.com/GoogleOnlineSecurityBlog',\
'https://blogs.technet.microsoft.com/mmpc/feed/',\
'https://www.trustwave.com/rss.aspx?type=slblog',\
'https://blog.threattrack.com/feed/',\
'https://www.bleepingcomputer.com/feed/',\
'http://www.hackingarticles.in/feed/',\
'http://rss.packetstormsecurity.com/news/',\
'https://www.kali.org/feed/',\
'http://seclists.org/rss/cert.rss',\
'https://nakedsecurity.sophos.com/feed/',\
'https://www.wired.com/feed/category/security/latest/rss',\
'https://securityboulevard.com/feed/',\
'http://feeds.arstechnica.com/arstechnica/security',\
'https://www.hackread.com/feed/',\
'https://www.cyberscoop.com/feed/',\
'http://feeds.feedburner.com/SecurityIntelligence',\
'https://threatpost.com/feed/',\
'https://cybersins.com/rss/']

# get the current date and time
now = datetime.now()
localtime = time.localtime()

# the first part of the HTML for the output code
topHtml = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>D33PM7N Cybersecurity Feeds Aggregator</title>
    <link rel="stylesheet" href="rss.css" type="text/css">
    <meta http-equiv="refresh" content="30"/>
  </head>
  <body>
    <div class="pageheader">
        <h1>RSS Feed Aggregator</h1>
        <div class="time">
            <p>"""
# add the time
topHtml += now.strftime("%d %b %Y | %I:%M %p")
# finish the first part of the HTML
topHtml +="""</p>
        </div>
    </div>
    <div class="content">
"""

# set a timeout for open sockets (This can be changed if feeds need more time)
socket.setdefaulttimeout(5)

# this is the variable that will hold all the parsed feeds
everything = []

# parse all sites in the feedsList
for site in feedsList:
    raw = feedparser.parse(site)
    everything += [raw]

# start sorting, parsing, and removing old posts (etc.)

# variables to hold sorted lists, etc.
allPosts = []
sortedPosts = []

# merge all posts into one big list
for site in everything:
    for post in site.entries:
        allPosts.append(post)

# variable to hold only this  years posts
thisYearsPosts = []

# get rid of last years posts (For rss feeds that go on forever. Can be removed)
for post in allPosts:
    if post.published_parsed.tm_year == now.year:
        thisYearsPosts.append(post)

# sort by time (So we see the most recent posts first)
sortedPosts = sorted(thisYearsPosts, key=attrgetter('published_parsed'), reverse=True)

# variable to store generated HTML data into
htm = """
"""

# counter for how many posts have been added to HTML
i = 0

# generate HTML content from the parsed feeds
for post in sortedPosts:
    if i < postsToDisplay:
        htm += """
        <div class="post">
            <div class="title">
                <h3>"""
        # add the post title
        htm += str(post.title)
        htm += """</h3>
            </div>
            <div class="postLink">
                <a href=\""""
        # add the link to the post
        htm += str(post.link)
        htm += """\">"""
        htm += str(post.link)
        htm += """</a>
            </div>
            <div class="summary">
                <p>"""
        # add the summary
        htm += str(post.summary)
        htm += """</p>
            </div>
            <div class="postTime">
                <p>Posted on """
        # time conversion into localtime (Set to MST right now)
        t = datetime.fromtimestamp(time.mktime(post.published_parsed))
        dategmt = gmt.localize(t)
        date = dategmt.astimezone(mountain)
        # add the published date
        htm += date.strftime("%d %b %Y | %I:%M %p %Z")
        htm += """</p>
            </div>
        </div>
        """
        i += 1

# HTML for the bottom of the output
bottomHtml = """</div>
    
  </body>
</html>
"""

# properly encode our output, so we don't break things
content = str(htm.encode('utf-8', 'ignore').decode('ascii', 'ignore'))

# open the file for writing
f = open('index.html','w')

# write the HTML to the file
f.write(topHtml)
f.write(content)
f.write(bottomHtml)

# close the file, and we're done!
f.close()

########################################################################################
#
# END of AGGREGATE.PY
#
########################################################################################
