# Copyright 2024 Austin Huang
# SPDX-License-Identifier: Apache-2.0

import requests, wordninja, logging
from os import path
from datetime import datetime, timedelta
from re import findall, search
from typing import List

logger = logging.getLogger(__name__)

WORKING_DIR = path.dirname(path.abspath(__file__))

class TagCaseCorrector(object):
    def __init__(
        self,
        instance: str,
        api_key: str,
        do_all_tags: bool,
        languages: List[str],
        tags_days: str,
        dictionary: str,
        cap_first_letter: bool = False,
        disable_post_analysis: bool = False,
        dry_run: bool = False,
        disable_wordninja: bool = False,
    ):
        self.instance = instance
        self.api_key = api_key
        self.do_all_tags = do_all_tags
        self.languages = [] if languages == [''] else languages
        self.tags_days = 7 if tags_days == '' else int(tags_days)
        if languages != ['']:
            today = datetime.today()
            self.today_date = today.strftime('%Y-%m-%d')
            past = today - timedelta(days=self.tags_days)
            self.past_date = past.strftime('%Y-%m-%d')
        self.model = None if disable_wordninja else self.dictionary(dictionary)
        self.do_analysis = not disable_post_analysis
        self.dry_run = dry_run
        self.cap_first_letter = cap_first_letter
        logging.basicConfig(level=logging.INFO) # TODO: make configurable
        if self.dry_run:
            logging.warning("In dry run mode!")

    @staticmethod
    def dictionary(dictionary: str | type(None)):
        if dictionary is None or dictionary == '':
            return wordninja.DEFAULT_LANGUAGE_MODEL
        return wordninja.LanguageModel(dictionary)

    def run(
        self,
        offset: int = 0, # increment by number of results (so 20 each time)
    ):
        resp = requests.get(
            f"https://{self.instance}/api/v1/admin{'' if self.do_all_tags else '/trends'}/tags?limit=20&offset={offset}",
            headers = {"Authorization": f"Bearer {self.api_key}"}
        )
        tags = resp.json()
        for tag in tags:
            if tag['requires_review'] == False:
                # note that the fix_case method, as well as changing the display name in the web interface,
                # will mark this to True, that's just how Mastodon works. It cannot be changed to False
                continue
            if not search(r"^[a-zA-Z0-9]+$", tag['name']):
                # contains non-alphanumeric characters
                continue
            if self.tags_days <= 7 and sum(map(lambda x: int(x['uses']), tag['history'])) == 0:
                logger.debug(f"#{tag['name']} is ignored as it has no posts in the past week")
                continue
            if sum(map(str.isupper, tag['name'])) > 1:
                # more than 1 capital letter => probably already good
                logger.debug(f"#{tag['name']} is ignored as it has more than 1 capital letter")
                continue
            self.fix_case(tag['id'], tag['name'])
        if len(tags) == 20:
            self.run(offset + 20)

    def check_tag_language(self, tag_id: str, tag_name: str):
        if self.languages == []:
            return True
        try:
            resp = requests.post(
                f"https://{self.instance}/api/v1/admin/dimensions",
                headers = {"Authorization": f"Bearer {self.api_key}"},
                json = {
                    "keys": ["tag_languages"],
                    "limit": 1,
                    "start_at": self.past_date,
                    "end_at": self.today_date,
                    "tag_languages": {"id": tag_id}
                }
            )
            r = resp.json()
            if len(r[0]['data']) == 0: # server has no data
                logger.debug(f"Cannot determine language for #{tag_name} because the instance has no post statistics for it")
                return False
            if r[0]['data'][0]['key'] in self.languages:
                return True
            logger.debug(f"#{tag_name}'s main language is not one of the given languages")
            return False
        except KeyError:
            logger.warning(f"Cannot determine language for #{tag_name} because of an error")
            return False
        except requests.exceptions.JSONDecodeError:
            logger.warning(f"Cannot determine language for #{tag_name} because of an error")
            return False

    def fix_case(self, tag_id: str, tag_name: str):
        wordninja_result = self.run_wordninja(tag_id, tag_name)
        post_results = self.analyze_posts(tag_name)
        logger.debug(f"Wordninja result for {tag_name} is {wordninja_result}")
        logger.debug(f"Analysis result for {tag_name} is [{', '.join(post_results)}]")
        new_name = None
        if (wordninja_result != None and wordninja_result in post_results) or len(post_results) == 0:
            # if wordninja is enabled and the wordninja result is in the result
            if self.cap_first_letter and (len(post_results) > 0 and sum(map(str.isupper, wordninja_result)) == 0 and
                    (wordninja_result.capitalize() == post_results[0] or wordninja_result.upper() == post_results[0])):
                # if wordninja returns just one word in lower case, but it's most often capitalized,
                # then capitalize it if cap_first_letter is enabled
                new_name = post_results[0]
            else:
                # otherwise, use the wordninja result
                new_name = wordninja_result
        else:
            # otherwise, use the most frequently used non-lowercase result if exists
            candidate: str | None = None
            for r in post_results:
                if sum(map(str.isupper, r)) > 1 or (sum(map(str.isupper, r)) == 1 and not r[0].isupper()):
                    # pascal or camel case found
                    new_name = f"{r[0].upper()}{r[1:len(r)]}"
                    break
                if sum(map(str.isupper, r)) == 1 and r[0].isupper():
                    # if just the first letter is capped, then it will be the new name if
                    # no pascal or camel case is found
                    candidate = r
            if new_name == None and candidate != None:
                new_name = candidate if self.cap_first_letter else tag_name
        if new_name == None:
            return
        logger.info(f"Changing #{tag_name} to #{new_name}...")
        if not self.dry_run:
            resp = requests.put(
                f"https://{self.instance}/api/v1/admin/tags/{tag_id}?display_name={new_name}",
                headers = {"Authorization": f"Bearer {self.api_key}"}
            )
    
    def run_wordninja(self, tag_id: str, tag_name: str):
        if self.model == None:
            return None
        if not self.check_tag_language(tag_id, tag_name):
            return None
        words = self.model.split(tag_name)
        if len(words) < 2: # one word or non-English
            return tag_name
        return ''.join(list(map(lambda x: x.capitalize(), words)))

    def analyze_posts(self, tag_name: str):
        if not self.do_analysis:
            return list()
        try:
            resp = requests.get(
                f"https://{self.instance}/api/v1/timelines/tag/{tag_name}?limit=40",
                headers = {"Authorization": f"Bearer {self.api_key}"},
            )
            r = resp.json()
            f = dict() # frequency table
            for post in r:
                w = self.find_casing(tag_name.lower(), post['content'])
                if w != None:
                    if w not in f:
                        f[w] = set()
                    f[w].add(post['account']['id'])
            # sort by frequency based on number of distinct authors
            return list(map(lambda f: f[0], sorted(f.items(), key=lambda w: -len(w[1]))))
        except KeyError:
            return list()
        except requests.exceptions.JSONDecodeError:
            return list()

    def find_casing(self, tag_name: str, content: str):
        for r in findall(
            r'<a href="https://(?:[^/]+)/tags/(?:[\w_]+)" class="mention hashtag"(?:[^>]*)>#<span>([\w_]+)</span></a>',
            content
        ):
            if r.lower() == tag_name:
                return r
        return None
