from os import getenv


class Constant:
    LIST_SOCIAL_NETWORK = [
        "tiktok",
        "instagram",
        "facebook",
        "youtube",
        "facebook_page",
    ]
    LIST_SOCIAL_NETWORK_QUICK_ANALYTICS = ["tiktok", "instagram", "facebook", "youtube"]
    REQUEST_TYPE_POST_PERFORMANCE = "post_performance"
    REQUEST_TYPE_BASIC_INFO = "basic_info"
    REQUEST_TYPE_LANDING_PAGE_INFO = "landing_page_info"
    REQUEST_TYPE_ML_BIO_INFO = "ml_bio_info"
    REQUEST_TYPE_TRANSCRIPT = "transcript"
    LIST_REQUEST_TYPE = [REQUEST_TYPE_POST_PERFORMANCE, REQUEST_TYPE_BASIC_INFO]

    AM_MAX_REQUEST = 3
    AM_DEFAULT_SLEEP_TIME = 3
    DEFAULT_LOAD_LIMIT_NUM_ITEM = 10
    DEFAULT_MAXIMUM_DAYS_AFTER_TAKEN = 7
    SERVICE_CONFIG_FOLDER_NAME = "service_config_samples"

    TOP_LEVEL_SCOPE = "__main__"
    LOG_FORMAT = "%(asctime)s - %(name)s: [%(levelname)s]: %(message)s"

    COLLECTION_SERVICE_ERROR_NAME = "collection_service_error_name"

    MONGODB_FIND_TYPE_FIND_ONE = "find_one"
    MONGODB_FIND_TYPE_FIND_MANY = "find"

    DEFAULT_TRANSFORM_ITEM_BATCH = 50

    COLLECTION_NAME_REPORT = "reports"
    COLLECTION_NAME_KOL = "kols"
    COLLECTION_NAME_USER = "users"
    COLLECTION_NAME_PAGE = "pages"
    COLLECTION_NAME_CHANNEL = "channels"
    COLLECTION_NAME_MEDIA = "medias"
    COLLECTION_NAME_COMMENT = "comments"
    COLLECTION_NAME_POST_COMMENT = "post_comments"
    COLLECTION_NAME_POST = "posts"
    COLLECTION_NAME_REELS_POST = "reels_posts"
    EXTENSION_DEFAULT = ".jpeg"

    MEDIA_TYPE_POST = "post"
    MEDIA_TYPE_AVATAR = "avatar"
    LIST_SUPPORT_MARKET = [
        market.strip()
        for market in getenv(
            "LIST_SUPPORTED_MARKET", "vi,id,th,ph,sg,my,platform"
        ).split(",")
    ]
    LIST_VIDEO_TYPE_FOR_ALL_SOCIAL = ["video", "livestream", "reels", "igtv"]
    LIST_ENGAGEMENT_CHART = ["Med. Engagement Rate", "Med. Engagements", "Med. Views"]
    USER_MED_LIKE_PATH = [
        "interaction",
        "all",
        "performance",
        "average_reaction_approximate",
    ]
    USER_MED_VIEW_PATH = [
        "interaction",
        "all",
        "performance",
        "average_view_approximate",
    ]
    # PRIORITY_CHART_BY_COUNTRY = {
    #     "id": [{"title": "Med. Views", "fields": ["view"]},
    #            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
    #            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]}
    #            ],
    #     "vi": [{"title": "Med. Views", "fields": ["view"]},
    #            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
    #            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]}
    #            ],
    #     "sg": [{"title": "Med. Views", "fields": ["view"]},
    #            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
    #            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]}
    #            ],
    #     "ph": [{"title": "Med. Views", "fields": ["view"]},
    #            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
    #            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]}
    #            ],
    #     "th": [{"title": "Med. Views", "fields": ["view"]},
    #            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
    #            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]}
    #            ],
    # }
    QUICK_VIEW_LIST_ENGAGEMENT_CHART = [
        "Med. Engagement Rate",
        "Med. Engagements",
        "Med. Views",
        "Avg. Engagement Rate",
        "Avg. Engagements",
        "Avg. Views",
    ]
    PRIORITY_CHART_BY_COUNTRY = {
        "vi": [
            {"title": "Med. Views", "fields": ["view"]},
            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]},
            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
        ],
        "id": [
            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
            {"title": "Med. Views", "fields": ["view"]},
            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]},
        ],
        "sg": [
            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
            {"title": "Med. Views", "fields": ["view"]},
            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]},
        ],
        "ph": [
            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]},
            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
            {"title": "Med. Views", "fields": ["view"]},
        ],
        "th": [
            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]},
            {"title": "Med. Views", "fields": ["view"]},
        ],
        "my": [
            {"title": "Med. Engagement Rate", "fields": ["engagement_rate"]},
            {"title": "Med. Views", "fields": ["view"]},
            {"title": "Med. Engagements", "fields": ["like", "comment", "share"]},
        ],
    }
    REQUEST_TYPE_QUICK_ANALYTICS = "quick_analytics"
    REQUEST_TYPES = ["post_list", "reels_list"]
    SOCIAL_TYPE_INSTAGRAM = "instagram"
    SOCIAL_TYPE_TIKTOK = "tiktok"
    SOCIAL_TYPE_YOUTUBE = "youtube"
    SOCIAL_TYPE_FACEBOOK = "facebook"
    SOCIAL_TYPE_FACEBOOK_PAGE = "facebook_page"
    SOCIAL_TYPES = [
        SOCIAL_TYPE_INSTAGRAM,
        SOCIAL_TYPE_TIKTOK,
        SOCIAL_TYPE_YOUTUBE,
        SOCIAL_TYPE_FACEBOOK,
        SOCIAL_TYPE_FACEBOOK_PAGE,
    ]

    EMAIL_NEED_CLEAN = ["<<not-applicable>>"]

    SOCIAL_LEVEL_THRESHOLD = {
        "tiktok": {
            "vi": [
                ("macro", 1.5e5, float("inf")),
                ("micro", 5e4, float("inf")),
                ("nano", 1e4, float("inf")),
                ("normal", 0, float("inf")),
            ],
            "sg": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1.5e5, float("inf")),
                ("micro", 5e4, float("inf")),
                ("nano", 5e3, float("inf")),
                ("normal", 0, float("inf")),
            ],
            "id": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1.5e5, float("inf")),
                ("micro", 5e4, float("inf")),
                ("nano", 5e3, float("inf")),
                ("normal", 0, float("inf")),
            ],
            "th": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1.5e5, float("inf")),
                ("micro", 5e4, float("inf")),
                ("nano", 5e3, float("inf")),
                ("normal", 0, float("inf")),
            ],
            "ph": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 1e4, float("inf")),
                ("nano", 1e3, float("inf")),
                ("normal", 0, float("inf")),
            ],
        },
        "instagram": {
            "vi": [
                ("macro", 2e5, float("inf")),
                ("micro", 1e3, 1e2),
                ("normal", 0, float("inf")),
            ],
            "sg": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 5e4, float("inf")),
                ("micro", 1e4, 1e2),
                ("nano", 5e2, 2e1),
                ("normal", 0, float("inf")),
            ],
            "id": [
                ("celebrity", 5e5, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 2e3, 1e2),
                ("normal", 0, float("inf")),
            ],
            "th": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 1e3, 1e2),
                ("normal", 0, float("inf")),
            ],
            "ph": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 1e4, 1e2),
                ("nano", 1e3, float("inf")),
                ("normal", 0, float("inf")),
            ],
        },
        "youtube": {
            "vi": [
                ("macro", 2e5, float("inf")),
                ("micro", 5e3, 5e3),
                ("normal", 0, float("inf")),
            ],
            "sg": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 2e5, float("inf")),
                ("micro", 5e3, 5e3),
                ("normal", 0, float("inf")),
            ],
            "id": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 2e5, float("inf")),
                ("micro", 3e3, 5e3),
                ("normal", 0, float("inf")),
            ],
            "th": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 2e5, float("inf")),
                ("micro", 3e3, 5e3),
                ("normal", 0, float("inf")),
            ],
            "ph": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 1e4, 5e3),
                ("nano", 1e3, float("inf")),
                ("normal", 0, float("inf")),
            ],
        },
        "facebook": {
            "vi": [
                ("macro", 2e5, float("inf")),
                ("micro", 1e3, 1e2),
                ("normal", 0, float("inf")),
            ],
            "sg": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 5e4, float("inf")),
                ("micro", 1e4, 1e2),
                ("nano", 5e2, 2e1),
                ("normal", 0, float("inf")),
            ],
            "id": [
                ("celebrity", 5e5, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 2e3, 1e2),
                ("normal", 0, float("inf")),
            ],
            "th": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 1e3, 1e2),
                ("normal", 0, float("inf")),
            ],
            "ph": [
                ("celebrity", 1e6, float("inf")),
                ("macro", 1e5, float("inf")),
                ("micro", 1e4, 1e2),
                ("nano", 1e3, float("inf")),
                ("normal", 0, float("inf")),
            ],
        },
    }

    LOG_GROUP_NAME_HASHTAG_ANALYTICS = getenv(
        "LOG_GROUP_NAME_HASHTAG_ANALYTICS", "ds/hashtag-analytics-staging"
    )
    LOG_GROUP_NAME_QA_PROFILE_SYNC = getenv(
        "LOG_GROUP_NAME_QA_PROFILE_SYNC", "ds/staging-qa-profiles"
    )
    LOG_REGION_QA_PROFILE_SYNC = getenv("LOG_REGION_QA_PROFILE_SYNC", "us-west-2")
    LOG_STREAM_TIME_FORMAT = getenv("LOG_STREAM_TIME_FORMAT", "%Y-%m-%d")
    APPLY_REGION_CONTENT_SEARCH_MARKETS = [
        market.strip()
        for market in getenv(
            "APPLY_REGION_CONTENT_SEARCH_MARKETS", "vi,id,th,ph,sg,my"
        ).split(",")
    ]
    REGION_CONTENT_SEARCH_MARKET_MAPPING = {
        "VI": "VN",
        "ID": "ID",
        "PH": "PH",
        "TH": "TH",
        "SG": "SG",
        "MY": "MY",
        "AR": "AR",
        "BR": "BR",
        "KH": "KH",
        "CA": "CA",
        "CN": "CN",
        "DK": "DK",
        "FI": "FI",
        "FR": "FR",
        "DE": "DE",
        "HK": "HK",
        "IT": "IT",
        "JP": "JP",
        "KG": "KG",
        "LA": "LA",
        "MX": "MX",
        "MM": "MM",
        "NL": "NL",
        "KP": "KP",
        "NO": "NO",
        "PT": "PT",
        "PL": "PL",
        "RU": "RU",
        "KR": "KR",
        "ES": "ES",
        "SE": "SE",
        "CH": "CH",
        "TW": "TW",
        "UA": "UA",
        "GB": "GB",
        "US": "US",
        "VN": "VN",
        "IN": "IN",
    }

    TIKTOK_PERCENT_EST_REACH = int(getenv("TIKTOK_PERCENT_EST_REACH", 80))
    YOUTUBE_PERCENT_EST_REACH = int(getenv("YOUTUBE_PERCENT_EST_REACH", 80))
    DEFAULT_PERCENT_EST_REACH = int(getenv("DEFAULT_PERCENT_EST_REACH", 80))

    CACHE_ENABLED = bool(getenv("CACHE_ENABLED", "true"))
    CACHE_EXPIRE_TIME = int(getenv("CACHE_EXPIRE_TIME", 86400))  # hour(s)
    CACHE_PROVIDER = getenv("CACHE_PROVIDER", "redis")
    CACHE_HOST = getenv("CACHE_HOST", "127.0.0.1")
    CACHE_PORT = getenv("CACHE_PORT", "6379")
    CACHE_PASSWORD = getenv("CACHE_PASSWORD", None)

    REDIS_HOST = getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PREFIX = getenv("REDIS_PREFIX", "hiip_stag.orgs")
    REDIS_PORT = getenv("REDIS_PORT", "6379")
    REDIS_PASSWORD = getenv("REDIS_PASSWORD", None)

    QUICK_ANALYTICS_CLIENT_KEY = getenv("QUICK_ANALYTICS_CLIENT_KEY", "")
    QUICK_ANALYTICS_TOKEN_LENGTH = int(getenv("QUICK_ANALYTICS_TOKEN_LENGTH", "32"))

    SUBSCRIPTION_X_HIIP_API_REQUIRED = bool(
        int(getenv("SUBSCRIPTION_X_HIIP_API_REQUIRED", "0"))
    )

    SCRAPINGBEE_API_KEY = getenv(
        "SCRAPINGBEE_API_KEY",
        "K72YVNZ7J5WXQER1INHI1FXKW7GH3XX69VGSPOODX5PIG1TUV2TD6X9IJT1NDECVKLV9BM7242EOG4HX",
    )
