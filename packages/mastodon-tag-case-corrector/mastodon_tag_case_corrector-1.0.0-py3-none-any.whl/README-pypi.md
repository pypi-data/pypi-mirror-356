# Mastodon Tag Case Corrector

A Python script for Mastodon instance admins to convert the display names of hashtags to PascalCase, when possible.

There are two possible strategies:

* Find tagged posts to determine the most used casing, and/or
* Split words with [wordninja](https://github.com/keredson/wordninja).

## Warning

This tool **DOES NOT** replace due diligence!!! There is **NO GUARANTEE** that this tool produces correct splittings of hashtags!!! **ALWAYS** review the log!!!

(However, the tool will not revisit any tags that have been changed either by the tool or manually by the admins.)

## Usage

This tool is developed with Python 3.13. Support for previous versions will be provided on a best effort basis.

```bash
pip install mastodon-tag-case-corrector

# for all options
mastodon-tag-case-corrector -h

# sample usage
mastodon-tag-case-corrector -i mstdn.example -a MY_SECRET_TOKEN
```

### Configuration

Configuration can be done through command-line options or by specifying variables.

| Variable name | CLI option | Required | Explanation |
|---|---|---|---|
| `MASTODON_INSTANCE` | `-i`, `--instance [INSTANCE]` | Yes | The domain that the Mastodon API is on, eg. `example.com`. |
| `MASTODON_API_KEY` | `-a`, `--auth [AUTH]` | Yes | Mastodon API access token with at least `admin:read` and `admin:write` permissions. `read:statuses` is needed if tagged post analysis is used. To get one, create a new application in User Settings => Development, then navigate to the application detail page and copy "your access token." |
| `MASTODON_CHECK_TAG_LANGUAGE` | `-l, --languages [LANGUAGES ...]` | No | A list of language codes, separated by comma. If supplied, before feeding the hashtag into wordninja, the script will check the language with the most tagged posts in the last 30 days for each hashtag. If the language is one of the supplied languages, the hashtag will be processed; otherwise it will be ignored. This does not affect tagged post checking, and has no effect if `WORDNINJA_DISABLE` is enabled. Recommended to be set to `en` for optimal results (as the default corpus used by `wordninja` is intended to only cover English words), however do note that [the `/api/v1/dimensions` endpoint](https://docs.joinmastodon.org/methods/admin/dimensions/) for determining a hashtag's language tends to be quite slow on instances, so omitting it could shorten execution time, at the possible expense of accuracy. |
| `MASTODON_DO_ALL_TAGS` | `-t, --all-tags` | No | If set to 1, the script will process all tags (from `/api/v1/admin/tags`), not just trending tags (from `/api/v1/admin/trends/tags`). Not recommended due to performance issue on the instance side, and that most hashtags tend to lack post statistics for language detection or post analysis to work (even if `MASTODON_TAGS_OFFSET` is used in combination). |
| `MASTODON_TAGS_OFFSET` | `-o, --offset [OFFSET]` | No | First offset to pass to the first tag-listing request. 0 by default. |
| `MASTODON_TAGS_DAYS` | `--language-days [LANGUAGE_DAYS]` | No | How many days of posts to consider for each hashtag to determine its language. 7 by default. |
| `MASTODON_CAP_FIRST_LETTER_WHEN_POSSIBLE` | `-c, --cap` | No | For hashtags that only consist of one word, cap the first letter if it is most often capped in practice (ie. enforce strict PascalCase even for one word). |
| `MASTODON_DISABLE_POST_ANALYSIS` | `--no-analysis` | No | Disable tagged post analysis. |
| `MASTODON_DRY_RUN` | `-d, --dry-run` | No | Disable actually editing the tag in Mastodon, which is recommended for development and testing purposes. |
| `WORDNINJA_DISABLE` | `--no-wordninja` | No | Disable wordninja detection. |
| `WORDNINJA_DICTIONARY` | `--dictionary [DICTIONARY]` | No | Relative path to a gzipped text file of a list of words (must be in lower case) to consider in descending importance. If not provided, [`wordninja`'s default corpus](https://github.com/keredson/wordninja/blob/master/wordninja/wordninja_words.txt.gz) will be used (note that this does not include fediverse jargons). |

Paths are relative to the working folder. For boolean arguments, the equivalent environment variable should be set to `1` for true.

## License

Copyright 2024-2025 Austin Huang <im@austinhuang.me> (https://austinhuang.me). Apache License 2.0.