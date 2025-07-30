# Copyright 2024 Austin Huang
# SPDX-License-Identifier: Apache-2.0

from main import TagCaseCorrector
from argparse import ArgumentParser
from dotenv import load_dotenv
from os import getenv
from sys import exit

def cli():
    load_dotenv()
    parser = ArgumentParser(
        description="Convert the display names of hashtags in a Mastodon instance to PascalCase"
    )
    parser.add_argument("-i", "--instance", default=getenv("MASTODON_INSTANCE"), help="""
        API domain of the instance (NOT webfinger).
    """, nargs='?')
    parser.add_argument("-a", "--auth", default=getenv("MASTODON_API_KEY"), help="""
        API access token of the application.
    """, nargs='?')
    parser.add_argument("-t", "--all-tags", action='store_true', help="""
        Process all tags instead of just the trending ones.
    """, default=getenv("MASTODON_DO_ALL_TAGS") == '1')
    parser.add_argument("--no-wordninja", action='store_true', help="""
        Disable wordninja analysis.
    """)
    parser.add_argument("--dictionary", default=getenv("WORDNINJA_DICTIONARY", ""), help="""
        Relative path to a gzipped text file of a list of words (must be in lower case)
        to consider in descending importance. If not provided, wordninja's default corpus
        will be used (note that this does not include fediverse jargons).
    """, nargs='?')
    parser.add_argument("-l", "--languages", help="""
        A list of language codes. If supplied, the script will only feed hashtags into wordninja
        if the language with the most posts using the hashtag in the past 30 days is within the list.
    """,
    default=getenv("MASTODON_CHECK_TAG_LANGUAGE", default="").split(","), 
    nargs='*')
    parser.add_argument("-o", "--offset", default=getenv("MASTODON_TAGS_OFFSET"), help="""
        First offset to pass to the first tag-listing request. 0 by default.
    """, nargs='?')
    parser.add_argument("-c", "--cap", action='store_true', help="""
        If the hashtag is one word, but the first letter is most often capped, then cap the letter.
    """, default=getenv("MASTODON_CAP_FIRST_LETTER_WHEN_POSSIBLE") == '1')
    parser.add_argument("--no-analysis", action='store_true', help="""
        Disable hashtag posts analysis.
    """, default=getenv("MASTODON_DISABLE_POST_ANALYSIS") == '1')
    parser.add_argument("--language-days", default=getenv("MASTODON_TAGS_DAYS", default="7"), help="""
        How many days of posts to consider for each hashtag to determine its language. 7 by default.
    """, nargs='?')
    parser.add_argument("-d", "--dry-run", action='store_true', help="""
        Perform dry run; that is, only show logs and not actually modify tags.
    """, default=getenv("MASTODON_DRY_RUN") == '1')  
    args = parser.parse_args()
    if args.instance == None or args.instance == '':
        print("""
            You must specify an instance via the --instance argument or using environment variable
            MASTODON_INSTANCE. See documentation or `mastodon-tag-case-corrector -h` for details.
        """)
        exit(150)
    if args.auth == None or args.auth == '':
        print("""
            You must specify an application token via the --auth argument or using environment variable
            MASTODON_API_KEY. See documentation or `mastodon-tag-case-corrector -h` for details.
        """)
        exit(151)
    offset = 0
    if args.offset is not None and args.offset != "":
        offset = int(args.offset)
    TagCaseCorrector(
        instance=args.instance,
        api_key=args.auth,
        do_all_tags=args.all_tags,
        languages=args.languages,
        disable_wordninja=args.no_wordninja,
        dictionary=args.dictionary,
        cap_first_letter=args.cap,
        disable_post_analysis=args.no_analysis,
        tags_days=args.language_days,
        dry_run=args.dry_run,
    ).run(offset)

if __name__ == "__main__":
    cli()