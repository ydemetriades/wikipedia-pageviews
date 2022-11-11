#!/usr/bin/env python
from ast import parse
import argparse
import requests

""" 
Unix Philosophy
1. Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new "features".
2. Expect the output of every program to become the input to another, as yet unknown, program. Don't clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don't insist on interactive input.
3. Design and build software, even operating systems, to be tried early, ideally within weeks. Don't hesitate to throw away the clumsy parts and rebuild them.
4. Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them.
"""

# Parse Arguments
parser = argparse.ArgumentParser(
    prog='wikipv',
    description='Wikipedia Pageviews; the easy way',
    epilog="And that's how we retrieve Wikipedia Pageviews easily!"
)

# Required Arguments
# Page ID
parser.add_argument('-p', '--page', type=str, required=True,
                    help='The title of any article in the specified project. Any spaces should be replaced with underscores. It also should be URI-encoded, so that non-URI-safe characters like %%, / or ? are accepted. Example: Are_You_the_One%%3F')

# Contact Email
parser.add_argument('--email', type=str, required=True,
                    help='Contact Email Address required for the Wikipedia API')

# Optional Arguments
# Project Name
parser.add_argument('--project', type=str, required=False, default='en.wikipedia',
                    help='If you want to filter by project, use the domain of any Wikimedia project, for example "en.wikipedia.org", "www.mediawiki.org" or "commons.wikimedia.org". [Default: en.wikipedia]')

# Access
parser.add_argument('--access', type=str, required=False, default='all-access',
                    choices=['all-access', 'desktop',
                             'mobile-app', 'mobile-web'],
                    help='If you want to filter by access method, use one of desktop, mobile-app or mobile-web. If you are interested in pageviews regardless of access method, use all-access. [Default: all-access]')

# Agent
parser.add_argument('--agent', type=str, required=False, default='user',
                    choices=['all-agents', 'user', 'spider', 'automated'],
                    help='If you want to filter by agent type, use one of user, automated or spider. If you are interested in pageviews regardless of agent type, use all-agents. [Default: user]')

# Granularity
parser.add_argument('--granularity', type=str, required=False, default='monthly',
                    choices=['daily', 'monthly'],
                    help='The time unit for the response data. As of today, the only supported granularity for this endpoint is daily and monthly. [Default: monthly]')

# Start Date
parser.add_argument('--start', type=str, required=False, default='2016010100',
                    help='The date of the first day to include, in YYYYMMDD or YYYYMMDDHH format. [Default: 2016010100]'
                    )

# End Date
parser.add_argument('--end', type=str, required=False, default='2016020100',
                    help='The date of the first day to include, in YYYYMMDD or YYYYMMDDHH format. [Default: 2016020100]'
                    )

args = parser.parse_args()

user_agent = ('wikipv/1.0 (%(email)s) generic-library/1.0' %
              {'email': args.email})

url = (
    'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/%(project)s/%(access)s/%(agent)s/%(page)s/%(granularity)s/%(start)s/%(end)s' %
    {
        'project': args.project,
        'access': args.access,
        'agent': args.agent,
        'page': args.page,
        'granularity': args.granularity,
        'start': args.start,
        'end': args.end
    }
)

headers = {
    "User-Agent": user_agent,
    "Api-User-Agent": user_agent
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    content = response.text
    print(content),
    exit(0)
elif response.status_code == 434:
    exit(434, 'Request threshold limit [HTTP Status Code: 434]')
else:
    exit(1, 'Failed with [HTTP Status Code: %(code)s]' % {'code': response.status_code})