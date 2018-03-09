# Aggregate.Py
An RSS feed aggregator written in python.

Introduction
----------------------
This aggregator was written due to the lack of utility that other aggregator or feed readers possess. Specifically, an auto-updating RSS feed aggregator that can handle more than one feed and parse them correctly does not exist. The original version of this aggregator was written in PHP, but was limited in the number of feeds that could be aggregated due to the time needed to parse through them. This script does away with that because it generates a static HTML file that can be hosted on any webserver and takes significantly less time to load than the PHP version. Because of the nature of Deep Mountain Security, this project has been oriented towards cyber security, and as such the feeds currently used in the project generally consist of cyber security topics and news. A hosted version of the output may be found (for demonstration purposes) at http://D33PM7N.com/feeds.

Requirements
---------------
- Python (tested in 3.6)
- feedparser library
- pytz library

feedparser and pytz can by installed with pip
