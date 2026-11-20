#!/usr/bin/env python3
"""
board-poller.py — the seed of a job-board polling engine.
From https://jadebronco.com/first-prompt/ — free to copy, modify, and share.

It checks one employer's Greenhouse board, remembers what it has
already seen (seen.json), and prints only the NEW postings.
Run it on a schedule (cron, Task Scheduler) and grow it:
more boards, more ATS feeds, scoring against your fact base.

The other big public feeds (replace {company} with the board slug,
which is the segment in the employer's careers-page URL):
  Lever:           https://api.lever.co/v0/postings/{company}?mode=json
  Ashby:           https://api.ashbyhq.com/posting-api/job-board/{company}
  SmartRecruiters: https://api.smartrecruiters.com/v1/companies/{company}/postings?limit=100
"""

import json
import pathlib
import urllib.request

BOARD = "companyname"  # <-- the employer's Greenhouse board slug
SEEN = pathlib.Path("seen.json")

seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()

url = f"https://boards-api.greenhouse.io/v1/boards/{BOARD}/jobs?content=true"
with urllib.request.urlopen(url) as r:
    jobs = json.load(r)["jobs"]

for job in jobs:
    jid = str(job["id"])
    if jid not in seen:
        print("NEW:", job["title"], "-", job["absolute_url"])
        seen.add(jid)

SEEN.write_text(json.dumps(sorted(seen)))
