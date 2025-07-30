# Import libs
import base64
import hashlib
import json
import re
import statistics
import time
import urllib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from .constant import Constant
import requests


class Common:
    @staticmethod
    def warning_when_retry(self, retry_object, sleep, last_result):
        self.logger.warning(
            "Retrying %s: last_result=%s, retrying in %s seconds...",
            retry_object.fn,
            last_result,
            sleep,
        )

    @classmethod
    def md5_hash(cls, str_input):
        if isinstance(str_input, str):
            str_input = str_input.encode()

        hash_object = base64.b64encode(hashlib.md5(str_input).digest())
        result = hash_object.decode()
        return result

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parents[2]

    @staticmethod
    def validate_schema(data, schema):
        error = {}
        try:
            schema().load(data)
        except Exception as e:
            error = e
        return data, error

    @staticmethod
    def parse_base_64_json_string_to_dict(input_str):
        return json.loads(base64.b64decode(input_str))

    @staticmethod
    def transform_dict_with_mapping(dict_, mapping, default_value=None):
        transformed_dict = {k: dict_.get(v, default_value) for k, v in mapping.items()}
        return transformed_dict

    @staticmethod
    def calculate_interaction(
        list_post: [dict], num_follower: int, reaction_key: str = "num_reaction"
    ) -> dict:
        """
        Calculate interaction from list post.\n
        Input:
            - list_post (list): List post need to calculate.
            - num_follower (int): Num follower of "user".

        Output:
            - summary_interaction (dict): Interaction from list post
        """
        summary_interaction = dict(all={"last_time_analyze": int(time.time())})
        _, summary_dict = Common._collect_interaction_from_list_post(
            list_post, reaction_key
        )
        Common._summarize_interaction(summary_dict, summary_interaction, num_follower)
        return summary_interaction

    @staticmethod
    def calculate_rate(average, total):
        if total is None or total == 0:
            return 0

        return int(average / total * 100)

    @staticmethod
    def calculate_rate_decimal(average, total, round_up=0):
        if total is None or total == 0:
            return 0

        return round(average / total * 100, round_up)

    @staticmethod
    def calculate_avg(total, number):
        if number is None or number == 0:
            return 0

        return int(total / number)

    @staticmethod
    def build_tiktok_video_link(username: str, _id: str):
        return f"https://www.tiktok.com/@{username}/video/{_id}"

    @classmethod
    def get_dict_data_by_path(cls, _dict, keys):
        return cls.get_dict_data_by_path(_dict[keys[0]], keys[1:]) if keys else _dict

    @staticmethod
    def calculate_ratio(quantity, total, round_up=4):
        if total is None or total == 0:
            return 0

        return round(quantity / total, round_up)

    @staticmethod
    def _check_post_time(post, post_type, summary_dict):
        post_time = post.get("taken_at_timestamp", post.get("published_at", 0))
        if (
            summary_dict["all"]["analyzed_post_from"] is None
            or summary_dict["all"]["analyzed_post_from"] > post_time
        ):
            summary_dict["all"]["analyzed_post_from"] = post_time

        if (
            summary_dict["all"]["analyzed_post_to"] is None
            or summary_dict["all"]["analyzed_post_to"] < post_time
        ):
            summary_dict["all"]["analyzed_post_to"] = post_time

        if (
            summary_dict[post_type]["analyzed_post_from"] is None
            or summary_dict[post_type]["analyzed_post_from"] > post_time
        ):
            summary_dict[post_type]["analyzed_post_from"] = post_time
        if (
            summary_dict[post_type]["analyzed_post_to"] is None
            or summary_dict[post_type]["analyzed_post_to"] < post_time
        ):
            summary_dict[post_type]["analyzed_post_to"] = post_time

    @staticmethod
    def _detect_special_engagement_value(post, post_type, summary_dict):
        if isinstance(post.get("num_share"), int):
            try:
                summary_dict[post_type]["share"] += post["num_share"]
                summary_dict["all"]["share"] += post["num_share"]

            except KeyError:
                summary_dict[post_type]["share"] = post["num_share"]
                summary_dict["all"]["share"] = post["num_share"]

            summary_dict[post_type]["share_list"].append(post["num_share"])
            summary_dict["all"]["share_list"].append(post["num_share"])
        else:
            summary_dict[post_type]["share_list"].append(0)
            summary_dict["all"]["share_list"].append(0)

        if isinstance(post.get("num_est_reach"), int):
            try:
                summary_dict[post_type]["reach"] += post["num_est_reach"]
                summary_dict["all"]["reach"] += post["num_est_reach"]
            except KeyError:
                summary_dict[post_type]["reach"] = post["num_est_reach"]
                summary_dict["all"]["reach"] = post["num_est_reach"]

        if isinstance(post.get("num_save"), int):
            try:
                summary_dict[post_type]["save"] += post["num_save"]
                summary_dict["all"]["save"] += post["num_save"]
            except KeyError:
                summary_dict[post_type]["save"] = post["num_save"]
                summary_dict["all"]["save"] = post["num_save"]

            summary_dict[post_type]["save_list"].append(post["num_save"])
            summary_dict["all"]["save_list"].append(post["num_save"])

    @staticmethod
    def _collect_interaction_from_list_post(list_post: list, reaction_key: str):
        """
        Collect interaction from each post.\n
        Input:
            - list_post (list): List post need to collect.
            - reaction_key (str): Reaction key in post (FB: num_reaction, IG + YT: num_like)

        Output:
            - num_video_post (int): Number "video" from list post.
            - summary_dict (dict): Interaction for list post.
        """
        num_video_post = 0
        summary_dict = {
            "all": {
                "reaction": 0,
                "comment": 0,
                "quantity": 0,
                "view_count": 0,
                "post_ids": [],
                "analyzed_post_from": None,
                "analyzed_post_to": None,
                "view_list": [],
                "reaction_list": [],
                "comment_list": [],
                "engagement_list": [],
                "share_list": [],
                "save_list": [],
            },
        }
        for post in list_post:
            post_type = post.get("hiip_post_type") or post.get("post_type", "photo")
            if post_type not in summary_dict:
                summary_dict[post_type] = {
                    "reaction": 0,
                    "comment": 0,
                    "quantity": 0,
                    "post_ids": [],
                    "analyzed_post_from": None,
                    "analyzed_post_to": None,
                    "reaction_list": [],
                    "comment_list": [],
                    "engagement_list": [],
                    "share_list": [],
                    "save_list": [],
                }
                if post_type in Constant.LIST_VIDEO_TYPE_FOR_ALL_SOCIAL:
                    summary_dict[post_type]["view_count"] = 0
                    summary_dict[post_type]["view_list"] = []

            Common._check_post_time(post, post_type, summary_dict)

            if isinstance(post.get("num_comment"), int):
                summary_dict[post_type]["comment"] += post.get("num_comment", 0)
                summary_dict["all"]["comment"] += post["num_comment"]

                summary_dict[post_type]["comment_list"].append(post["num_comment"])
                summary_dict["all"]["comment_list"].append(post["num_comment"])

            if isinstance(post.get(reaction_key), int):
                summary_dict[post_type]["reaction"] += post[reaction_key]
                summary_dict["all"]["reaction"] += post[reaction_key]

                summary_dict[post_type]["reaction_list"].append(post[reaction_key])
                summary_dict["all"]["reaction_list"].append(post[reaction_key])

            Common._detect_special_engagement_value(post, post_type, summary_dict)
            summary_dict[post_type]["quantity"] += 1
            summary_dict[post_type]["post_ids"].append(post["_id"])
            summary_dict["all"]["quantity"] += 1
            summary_dict["all"]["post_ids"].append(post["_id"])
            num_video_post = Common._calculate_view_count(
                num_video_post, post, post_type, summary_dict
            )
        return num_video_post, summary_dict

    @staticmethod
    def _calculate_view_count(num_video_post, post, post_type, summary_dict):
        if post_type in Constant.LIST_VIDEO_TYPE_FOR_ALL_SOCIAL:
            if post.get("view_count") and isinstance(post.get("view_count"), int):
                summary_dict[post_type]["view_count"] += post["view_count"]
                summary_dict["all"]["view_count"] += post["view_count"]

                summary_dict[post_type]["view_list"].append(post["view_count"])
                summary_dict["all"]["view_list"].append(post["view_count"])

            elif post.get("video_view_count") and isinstance(
                post.get("video_view_count"), int
            ):
                summary_dict[post_type]["view_count"] += post["video_view_count"]
                summary_dict["all"]["view_count"] += post["video_view_count"]

                summary_dict[post_type]["view_list"].append(post["video_view_count"])
                summary_dict["all"]["view_list"].append(post["video_view_count"])

            elif post.get("num_view") and isinstance(post.get("num_view"), int):
                summary_dict[post_type]["view_count"] += post["num_view"]
                summary_dict["all"]["view_count"] += post["num_view"]

                summary_dict[post_type]["view_list"].append(post["num_view"])
                summary_dict["all"]["view_list"].append(post["num_view"])

            num_video_post += 1
        return num_video_post

    @staticmethod
    def _summarize_interaction(summary_dict, summary_interaction, num_follower):
        for post_type, summary_type in summary_dict.items():
            Common._calculate_avg_interaction_by_post_type(
                num_follower, post_type, summary_dict, summary_interaction, summary_type
            )

    @staticmethod
    def _calculate_avg_interaction_by_post_type(
        num_follower, post_type, summary_dict, summary_interaction, summary_type
    ):
        summary_interaction[post_type] = {"last_time_analyze": int(time.time())}
        summary_interaction[post_type]["analyzed_post_from"] = summary_type[
            "analyzed_post_from"
        ]
        summary_interaction[post_type]["analyzed_post_to"] = summary_type[
            "analyzed_post_to"
        ]
        summary_interaction[post_type]["post_ids"] = summary_type["post_ids"]
        summary_interaction[post_type]["quantity"] = summary_type["quantity"]
        summary_interaction[post_type]["rate"] = round(
            Common.calculate_ratio(
                summary_type["quantity"], summary_dict["all"]["quantity"]
            )
            * 100,
            2,
        )
        avg_reaction = Common.calculate_avg(
            summary_type["reaction"], summary_type["quantity"]
        )
        avg_comment = Common.calculate_avg(
            summary_type["comment"], summary_type["quantity"]
        )

        avg_share = (
            Common.calculate_avg(summary_type["share"], summary_type["quantity"])
            if isinstance(summary_type.get("share"), int)
            else 0
        )
        avg_reach = (
            Common.calculate_avg(summary_type["reach"], summary_type["quantity"])
            if isinstance(summary_type.get("reach"), int)
            else 0
        )
        avg_save = (
            Common.calculate_avg(summary_type["save"], summary_type["quantity"])
            if isinstance(summary_type.get("save"), int)
            else 0
        )

        if avg_reaction == -1 or avg_comment == -1 or avg_share == -1 or avg_save == -1:
            avg_engagement = -1
        else:
            avg_engagement = avg_reaction + avg_comment + avg_share + avg_save

        avg_buzz = avg_comment + avg_share

        average_comment_approximate = None
        average_reaction_approximate = None
        average_engagement_approximate = None
        average_share_approximate = None
        average_save_approximate = None
        if len(summary_dict[post_type]["comment_list"]) > 0:
            average_comment_approximate = statistics.median(
                summary_dict[post_type]["comment_list"]
            )
        if len(summary_dict[post_type]["reaction_list"]) > 0:
            average_reaction_approximate = statistics.median(
                summary_dict[post_type]["reaction_list"]
            )
        if len(summary_dict[post_type]["save_list"]) > 0:
            average_save_approximate = statistics.median(
                summary_dict[post_type]["save_list"]
            )
        if avg_share is not None and len(summary_dict[post_type]["share_list"]) > 0:
            average_share_approximate = statistics.median(
                summary_dict[post_type]["share_list"]
            )
        if (
            average_comment_approximate is not None
            or average_reaction_approximate is not None
            or average_share_approximate is not None
        ):
            average_engagement_approximate = (
                int(average_comment_approximate or 0)
                + int(average_reaction_approximate or 0)
                + int(average_share_approximate or 0)
            )
        summary_interaction[post_type]["performance"] = {
            "average_reaction": avg_reaction,
            "average_reaction_rate": round(
                Common.calculate_ratio(avg_reaction, num_follower) * 100, 2
            ),
            "average_comment": avg_comment,
            "average_comment_rate": round(
                Common.calculate_ratio(avg_comment, num_follower) * 100, 2
            ),
            "average_engagement": avg_engagement,
            "average_engagement_rate": (
                round(Common.calculate_ratio(avg_engagement, num_follower) * 100, 2)
                if avg_engagement != -1
                else -1
            ),
            "average_buzz": avg_buzz,
            "average_buzz_rate": round(
                Common.calculate_ratio(avg_buzz, num_follower) * 100, 2
            ),
            "average_comment_approximate": average_comment_approximate,
            "average_reaction_approximate": average_reaction_approximate,
            "average_engagement_approximate": average_engagement_approximate,
            "average_engagement_rate_approximate": (
                round(
                    Common.calculate_ratio(average_engagement_approximate, num_follower)
                    * 100,
                    2,
                )
                if average_engagement_approximate is not None
                else None
            ),
        }
        if summary_type.get("view_count"):
            avg_view = Common.calculate_avg(
                summary_type["view_count"], len(summary_dict[post_type]["view_list"])
            )
            summary_interaction[post_type]["performance"]["average_view"] = avg_view
            summary_interaction[post_type]["performance"]["average_view_rate"] = round(
                Common.calculate_ratio(avg_view, num_follower) * 100, 2
            )
            if len(summary_dict[post_type]["view_list"]) > 0:
                summary_interaction[post_type]["performance"][
                    "average_view_approximate"
                ] = statistics.median(summary_dict[post_type]["view_list"])
            else:
                summary_interaction[post_type]["performance"][
                    "average_view_approximate"
                ] = None
        else:
            summary_interaction[post_type]["performance"]["average_view"] = None
            summary_interaction[post_type]["performance"]["average_view_rate"] = None
            summary_interaction[post_type]["performance"][
                "average_view_approximate"
            ] = None

        if avg_share is not None:
            summary_interaction[post_type]["performance"]["average_share"] = avg_share
            summary_interaction[post_type]["performance"]["average_share_rate"] = round(
                Common.calculate_ratio(avg_share, num_follower) * 100, 2
            )
            summary_interaction[post_type]["performance"][
                "average_share_approximate"
            ] = average_share_approximate
            average_buzz_approximate = (
                average_share_approximate + average_comment_approximate
                if average_share_approximate is not None
                and average_comment_approximate is not None
                else None
            )
            summary_interaction[post_type]["performance"][
                "average_buzz_approximate"
            ] = average_buzz_approximate

        if avg_reach:
            summary_interaction[post_type]["performance"][
                "average_est_reach"
            ] = avg_reach
            summary_interaction[post_type]["performance"]["average_est_reach_rate"] = (
                round(Common.calculate_ratio(avg_reach, num_follower) * 100, 2)
            )
        if avg_save:
            summary_interaction[post_type]["performance"]["average_save"] = avg_save
            summary_interaction[post_type]["performance"]["average_save_rate"] = round(
                Common.calculate_ratio(avg_save, num_follower) * 100, 2
            )
            summary_interaction[post_type]["performance"][
                "average_save_approximate"
            ] = average_save_approximate

    @classmethod
    def convert_timestamp_to_datetime(cls, timestamp_string, datetime_format):
        date = datetime.fromtimestamp(timestamp_string)
        return date.strftime(datetime_format)

    @staticmethod
    def convert_datetime_to_timestamp(datetime_string, datetime_format):
        date = datetime.strptime(datetime_string, datetime_format)
        return int(date.timestamp())

    @classmethod
    def run_io_tasks_in_parallel(cls, tasks, max_workers=3):
        data = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            running_tasks = [executor.submit(*task) for task in tasks]
            for running_task in running_tasks:
                data.append(running_task.result())
            return data

    @classmethod
    def get_hashtags(cls, text):
        hashtags = re.findall(r"#(\w+)", text)
        return [f"#{hashtag}" for hashtag in hashtags]

    @classmethod
    def get_variable_name_from_string(cls, string):
        variable_names = re.findall(r"{(\w+)}", string)
        return variable_names

    @staticmethod
    def mapping_data(data: dict, mapping_fields: dict, remove_fields: list = None):
        """
        Mapping collected data to stored data format

        Input:
            - data (dict): dota collected
            - mapping_fields (dict): key-value pairs
               + key: field name of data after mapping
               + value (list): list keys as a path to direct to target value
        """
        mapped_data = dict()

        for key, value in mapping_fields.items():
            if isinstance(value, str):
                mapped_data[key] = data.get(value)
            elif isinstance(value, list):
                mapped_data[key] = Common.get_nested_value(data, value)
        mapped_data.update(data)
        if remove_fields:
            [mapped_data.pop(key) for key in remove_fields if mapped_data.get(key)]
        return mapped_data

    @staticmethod
    def convert_s3_uri_to_url(s3_uri: str, bucket: str, s3_url_name: str):
        base_uri = "s3://{bucket}".format(bucket=bucket)
        base_url = "https://{url_name}".format(url_name=s3_url_name)
        return s3_uri.replace(base_uri, base_url)

    @classmethod
    def get_nested_value(cls, data, keys):
        try:
            result = cls.get_nested_value(data[keys[0]], keys[1:]) if keys else data
            return result
        except Exception:
            return None

    @classmethod
    def remove_key(cls, dict_: dict, list_key: list):
        """
        Remove key replaced
        Input:
            - dict (dict): dict to remove key
        Output:
            - list_key (list): key list want to remove
        """
        for key in list_key:
            try:
                del dict_[key]
            except KeyError:
                continue

    @staticmethod
    def encode_file_name(file_url: str):
        if not file_url:
            return file_url
        pies = file_url.split("/")
        if len(pies) <= 1:
            return file_url
        last_element = pies.pop()
        last_element_encoded = urllib.parse.quote(last_element)
        pies.append(last_element_encoded)

        return "/".join(pies)

    @staticmethod
    def get_top_hashtags_from_list_post(post_list: list, limit: int = 0):
        list_hashtag = []
        for post in post_list:
            content = (
                (post.get("content") or "") + "\n" + (post.get("description") or "")
            )
            post_hashtags = Common.get_hashtags(content)
            list_hashtag += post_hashtags
            post["hashtags"] = post_hashtags

        dict_hashtags = Counter(list_hashtag)
        num_hashtags_taken = limit if limit else len(dict_hashtags)
        top_hashtags = sorted(
            dict_hashtags.items(), key=lambda pair: pair[1], reverse=True
        )[:num_hashtags_taken]
        calculated_top_hashtags = []
        total_hashtag = sum([hashtag[1] for hashtag in top_hashtags])
        total_percent = 0

        for index, hashtag in enumerate(top_hashtags):
            if index == len(top_hashtags) - 1:
                hashtag_percent = round(100 - total_percent, 1)
            else:
                hashtag_percent = (
                    int(Common.calculate_ratio(hashtag[1], total_hashtag) * 100 * 10)
                    / 10
                )
                total_percent += hashtag_percent
            calculated_top_hashtags.append(
                {"name": hashtag[0], "count": hashtag[1], "percent": hashtag_percent}
            )

        return calculated_top_hashtags

    @staticmethod
    def get_social_level(country, social, follower, median=0):
        level_threshold = Constant.SOCIAL_LEVEL_THRESHOLD.get(social, {}).get(country)
        if not level_threshold:
            level_threshold = Constant.SOCIAL_LEVEL_THRESHOLD.get(social, {}).get(
                "sg", {}
            )
        if len(level_threshold) == 0:
            return None
        level = next(
            (
                level
                for level, thr1, thr2 in level_threshold
                if (follower >= thr1 or median >= thr2)
            ),
            "normal",
        )
        return level

    @staticmethod
    def generate_log_stream_name(application_name="", time_format="%Y-%m-%d"):
        date = datetime.now().strftime(time_format)
        log_stream_name = f"{application_name}-{date}"
        return log_stream_name

    @classmethod
    def deserialize_dict_to_valid_json(cls, dict_data: dict):
        """
        transform python special type to valid json
        """
        if type(dict_data) in [list]:
            for index, item in enumerate(dict_data):
                dict_data[index] = cls.deserialize_dict_to_valid_json(item)

        elif type(dict_data) in [dict]:
            for key, value in dict_data.items():
                dict_data[key] = cls.deserialize_dict_to_valid_json(value)

        elif type(dict_data) in [set]:
            dict_data = list(dict_data)

        return dict_data

    @staticmethod
    def get_text_by_request(url):
        response = requests.get(url)
        return response.text


class Dict2Obj:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        """"""
        return "<Dict2Obj: %s>" % self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]
