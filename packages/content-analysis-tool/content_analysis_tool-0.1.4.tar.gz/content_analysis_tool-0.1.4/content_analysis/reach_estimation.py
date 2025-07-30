import json

from typing import List
from .constant import Constant
from .common import Common


class ReachEstimation:
    def __init__(self, social_type: str, country_code: str) -> None:
        if social_type in Constant.LIST_SOCIAL_NETWORK:
            self.social_type = social_type
        else:
            raise ValueError("Social type is not supported")
        self.country_code = country_code

        print(f"{self.__class__.__name__} init with social_type: {self.social_type}")

    def calculate(self, data, is_print=None):
        """
        calculate reach of list of posts

        Args:
            - data: dict or list of dict that contains with the pattern:
                - "post_id": str,
                - "post_type": str *optional for instagram and facebook. default is all except reel,
                - "like": int, not use for reel, youtube and tiktok
                - "comment": int, not use for reel, youtube and tiktok
                - "share": int, not use for reel, youtube and tiktok
                - "play": int, not use for instagram and facebook
                - "view": int,
                - "follower": int,

        Returns:
            - if data is list of dict
            - if data is dict then return dict
            - with the pattern:
            {
                "post_id": str, *optional
                "reach": int,
                "reach_rate": float
            }
        """
        # try:
        if isinstance(data, dict):
            if is_print:
                print(f"{self.__class__.__name__} calculate_single_post")
            return self.calculate_single_post(data)
        elif isinstance(data, list):
            if is_print:
                print(f"{self.__class__.__name__} calculate_multiple_posts")
            return self.calculate_multiple_posts(data)
        else:
            raise ValueError("Data must be dict or list of dict")
        # except Exception as e:
        #     print(f"{self.__class__.__name__} calculate error: {e}")
        #     return None

    def calculate_multiple_posts(self, data: List[dict]) -> List[dict]:
        """
        calculate reach of list of posts

        Args:
            - data: list of dict that contains with the pattern:
                - "post_id": str,
                - "post_type": str *optional for instagram and facebook. default is all except reel,
                - "like": int, not use for reel, youtube and tiktok
                - "comment": int, not use for reel, youtube and tiktok
                - "share": int, not use for reel, youtube and tiktok
                - "num_play": int, not use for instagram and facebook
                - "view": int,
                - "follower": int,
        Returns:
            - list of post that contains with the pattern:
            {
                "post_id": str,
                "reach": int,
                "each_rate": float
            }
        """
        return self._calculate_multiple_posts(data)

    def _calculate_multiple_posts(self, data: List[dict]):
        return getattr(self, f"_calculate_multiple_posts_{self.social_type}")(data)

    def _calculate_multiple_posts_instagram(self, data: List[dict]):
        """
        - Multiple posts: Using AI to estimate reach of posts
        - Reels: Using view to estimate reach of reels
        """

        results = [{**self._calculate_single_post(post),
                    "post_id": post.get("post_id")} for post in data]

        return results

    def _calculate_multiple_posts_youtube(self, data: List[dict]):
        """
        Using View to estimate reach of posts
        """
        result = [{**self._calculate_single_post(post),
                   "post_id": post.get("post_id")} for post in data]
        return result

    def _calculate_multiple_posts_tiktok(self, data: List[dict]):
        """
        Using View to estimate reach of posts
        """
        result = [{**self._calculate_single_post(post),
                   "post_id": post.get("post_id")} for post in data]
        return result

    def _calculate_multiple_posts_facebook(self, data: List[dict]):
        """
        Using View to estimate reach of posts
        """
        result = [{**self._calculate_single_post(post),
                   "post_id": post.get("post_id")} for post in data]
        return result

    def _calculate_multiple_posts_facebook_page(self, data: List[dict]):
        return self._calculate_multiple_posts_facebook(data)

    def calculate_single_post(self, post) -> dict:
        """
        calculate reach of single post

        Args:
            - post:  dict that contains with the pattern:
                - "post_id": str,
                - "post_type": str *optional for instagram and facebook. default is all except reel,
                - "like": int, not use for reel, youtube and tiktok
                - "comment": int, not use for reel, youtube and tiktok
                - "share": int, not use for reel, youtube and tiktok
                - "num_play": int, not use for instagram and facebook
                - "view": int,
                - "follower": int,

        Returns:
            - dict: {"reach": int, "reach_rate": float}

        """
        return self._calculate_single_post(post)

    def _calculate_single_post(self, post: dict):
        return getattr(self, f"_calculate_single_post_{self.social_type}")(**post)

    def _calculate_single_post_tiktok(self, **kwargs):
        """
        calculate reach of single post using view
        """
        return self._calculate_by_view(kwargs.get("view"), kwargs.get("follower"))

    def _calculate_single_post_youtube(self, **kwargs) -> dict:
        """
           calculate reach of single post using view
        """
        return self._calculate_by_view(kwargs.get("view"), kwargs.get("follower"))

    def _calculate_single_post_instagram(self, **kwargs) -> dict:
        """
        calculate reach of single post
        if post_type is reel, use view to calculate reach
        Args:
            view (int): view of post
            follower (int): follower of page
            **kwargs: other params

        Returns:
            dict: {"reach": int, "reach_rate": float}
        """
        view = kwargs.get("play") or kwargs.get("view")
        if view:
            return self._calculate_by_view(view, kwargs.get("follower"))
        else:
            result = InstagramReachEstimation().estimate_reach([kwargs])
            return result[0]

    def _calculate_single_post_facebook(self, **kwargs) -> dict:
        """
        calculate reach of single post
        if post_type is reel, use view to calculate reach
        Args:
            - reel:
                - view (int): view of post
                - follower (int): follower of page
            - others: more params
                - comment (int): comment of post
                - share (int): share of post
                **kwargs: other params

        Returns:
            dict: {"reach": int, "reach_rate": float}
        """
        if kwargs.get("post_type") == "reel":
            return self._calculate_by_view(kwargs.get("view"), kwargs.get("follower"))
        else:
            facebook_reach_estimation = FacebookReachEstimation(self.social_type, self.country_code)
            return facebook_reach_estimation.calculate(**kwargs)
            # reach_rate = self._calculate_reach_rate(reach, kwargs.get("follower"))
            # return {"reach": reach, "reach_rate": reach_rate}

    def _calculate_single_post_facebook_page(self, **kwargs) -> dict:
        return self._calculate_single_post_facebook(**kwargs)

    def _calculate_from_ml(self, data: List[dict]):
        short_social_type = {"instagram": "ig", "facebook": "fb", "youtube": "yt", "tiktok": "tt"}

        if not hasattr(self, "lambda_collect_handler"):
            self.lambda_collect_handler = LambdaCollectHandler(
                region_name=self.system_config.ML_EST_REACH_ANALYTICS_FUNCTION_REGION)

        if len(data) > 0:
            followers = {item.get("post_id"): item.get("follower", 0) for item in data}
            data_request = []
            for item in data:
                data_request.append({"post_id": item.get("post_id"),
                                     "like": item.get("like", 0),
                                     "comment": item.get("comment", 0),
                                     "share": item.get("share", 0),
                                     "view": item.get("view", 0),
                                     "follower": item.get("follower", 0)})

            payload = {"data": data_request, "country_code": self.country_code,
                       "social_network": short_social_type[self.social_type]}
            response = self.lambda_collect_handler.get_data_from_lambda(
                payload=payload,
                function_name=self.system_config.ML_EST_REACH_ANALYTICS_FUNCTION_NAME)
            result = response.get("data", [{}])
            for item in result:
                if isinstance(item.get('reach'), float):
                    item['reach'] = int(item['reach'])
                item["reach_rate"] = self._calculate_reach_rate(item.get("reach"),
                                                                followers.get(item.get("post_id")))
        return result

    def _calculate_by_view(self, view: int, follower: int, **kwargs) -> dict:
        """
        calculate reach of single post by view

        Args:
            view (int): view of post
            follower (int): follower of page

        Returns:
            dict: {"reach": int, "reach_rate": float}
        """
        view = view or 0

        reach = 0
        reach_rate = 0
        PERCENT = getattr(Constant, f"{self.social_type.upper()}_PERCENT_EST_REACH",
                          getattr(Constant, "DEFAULT_PERCENT_EST_REACH", 0))
        reach = int(PERCENT * view / 100)
        reach_rate = self._calculate_reach_rate(reach, follower)
        return dict(reach=reach, reach_rate=reach_rate)

    def _calculate_reach_rate(self, reach: int, follower: int) -> float:
        """
        calculate reach rate of single post

        Args:
            reach (int): reach of post
            follower (int): follower of page

        Returns:
            float: reach rate
        """
        return Common.calculate_ratio(reach * 100, follower, 2) if follower else None

    def calculate_reach_rate(self, reach: int, follower: int) -> float:
        """
        calculate reach rate of single post

        Args:
            reach (int): reach of post
            follower (int): follower of page

        Returns:
            float: reach rate
        """
        return self._calculate_reach_rate(reach, follower)


class FacebookReachEstimation:
    def __init__(self, social_type: str, country_code: str):
        self.social_type = social_type
        self.country_code = country_code
        parameter_path = f"{Common.get_project_root()}/" \
            f"core/utils/facebook_reach_parameter.json"
        with open(parameter_path, 'r') as f:
            param_dict = json.load(f)
        self.param_dict = param_dict.get(self.social_type)

    def est_base_reach(self, follower):
        base_reach_rate = self.param_dict['base_reach_rate']
        base_reach = follower * base_reach_rate

        return base_reach

    def est_eng_reach(self, total_eng):
        engagement_reach_rate = self.param_dict['engagement_reach_rate']
        eng_reach = total_eng / engagement_reach_rate

        return eng_reach

    def cal_total_eng(self, like, comment, share):
        total_eng = like + comment + share
        return total_eng

    def calculate(self, like, comment, share, follower=0, **kwargs):
        base_reach = 0
        eng_reach = 0
        total_eng = self.cal_total_eng(like, comment, share)

        eng_reach = self.est_eng_reach(total_eng)
        if follower is not None and follower != 0:
            base_reach = self.est_base_reach(follower)

        base_weight = self.param_dict['base_weight']
        engagement_weight = self.param_dict['engagement_weight']
        if follower:
            total_reach = base_weight * base_reach + engagement_weight * eng_reach
            reach_rate = Common.calculate_ratio(total_reach, follower) * 100
        else:
            total_reach = eng_reach
            reach_rate = None

        return {"reach": int(total_reach), "reach_rate": reach_rate}

class InstagramReachEstimation:
    engagement_items = [53.0, 98.0, 128.0, 211.5, 270.0, 343.0, 433.0, 546.0,
                        689.5, 883.0, 1147.0, 1543.0, 2248.5,
                        3601.5, 4500, 6583.0, 8000, 9500, 11000, 13000, 15000]

    lower_bounds = [1300, 1600, 2000, 2700, 4500, 6300, 8800, 11100, 12100,
                    13200, 14800, 19200, 28800, 46600, 64200, 79200,
                    97500, 107800, 118100, 128300, 150800]
    upper_bounds = [2200, 2600, 3500, 5300, 9600, 11800, 14600, 17600, 19700,
                    21700, 26400, 34600, 58900, 83500, 129100,
                    143400, 163500, 179200, 188900, 214500, 257900]

    large_engagement_rate = [0.14, 0.25, 0.42, 0.52]
    large_reach_rate = [0.046, 0.075, 0.09, 0.115]

    def _get_bound_index(self, number, bins):
        bound_index = next((i for i, v in enumerate(bins) if v > number), -1)
        return bound_index

    def get_convert_rate(self, low_enfl, high_enfl, enfl, engagement_rate, reach_rate, engagement_std, reach_std):
        if enfl < low_enfl:
            enfl = low_enfl
        elif enfl > high_enfl:
            enfl = high_enfl

        convert_rate = (enfl - low_enfl) / (high_enfl - low_enfl)
        low_enr = engagement_rate - engagement_std
        high_enr = engagement_rate + engagement_std
        low_rer = reach_rate - reach_std
        high_rer = reach_rate + reach_std

        est_reach_rate = convert_rate * (high_enr - low_enr) + low_enr
        est_engagement_rate = convert_rate * (high_rer - low_rer) + low_rer

        return est_engagement_rate, est_reach_rate

    def estimate_reach_for_large_range(self, engagement, num_follower):
        enfl = engagement / num_follower
        bins = [0.016, 0.0465, 0.08]
        enfl_range = self._get_bound_index(enfl, bins)
        est_engagement_rate = self.large_engagement_rate[enfl_range]
        est_reach_rate = self.large_reach_rate[enfl_range]

        base_reach = num_follower * est_reach_rate
        engagement_reach = engagement / est_engagement_rate
        est_reach = 0.75 * base_reach + 0.25 * engagement_reach

        return est_reach

    def estimate_reach_for_small_range(self, engagement, num_follower):
        engagement_range = self._get_bound_index(engagement, self.engagement_items)
        low_fl = self.lower_bounds[engagement_range]
        high_fl = self.upper_bounds[engagement_range]
        enfl = (engagement / num_follower) * 100
        if num_follower < low_fl:
            est_reach_rate, est_engagement_rate = self.get_convert_rate(low_enfl=4.1, high_enfl=6.5, enfl=enfl,
                                                                        engagement_rate=0.45,
                                                                        reach_rate=0.115,
                                                                        engagement_std=0.01,
                                                                        reach_std=0.02)

        elif low_fl <= num_follower < high_fl:
            est_reach_rate, est_engagement_rate = self.get_convert_rate(low_enfl=1.6, high_enfl=4.1, enfl=enfl,
                                                                        engagement_rate=0.30,
                                                                        reach_rate=0.08,
                                                                        engagement_std=0.01,
                                                                        reach_std=0.01)

        else:
            est_reach_rate, est_engagement_rate = self.get_convert_rate(low_enfl=0.4, high_enfl=1.6, enfl=enfl,
                                                                        engagement_rate=0.18,
                                                                        reach_rate=0.05,
                                                                        engagement_std=0.01,
                                                                        reach_std=0.01)

        est_reach = (num_follower * est_reach_rate) * 0.65 + (engagement / est_engagement_rate) * 0.35

        return est_reach

    def rule_based_reach_est(self, follower, comment, like):
        follower = follower or 1
        engagement = like + 1.5 * comment
        if engagement < 15e3:
            est_reach = self.estimate_reach_for_small_range(engagement, follower)
        else:
            est_reach = self.estimate_reach_for_large_range(engagement, follower)
        est_reach = max(est_reach, engagement)

        return est_reach

    def calculate_rule_based_reaches(self, post_list):
        for post in post_list:
            follower = post.get('follower') or 0
            comment = post.get('comment') or 0
            like = post.get('like') or 0

            if all(index == 0 for index in [follower, comment, like]):
                reach = 0
            else:
                reach = self.rule_based_reach_est(follower, comment, like)
            post['reach'] = int(reach)
            post['reach_rate'] = Common.calculate_ratio(reach * 100, follower, 2) if follower else None

        return post_list

    def estimate_reach(self, data):
        """
        Calculate reach of list of posts using rule based

        Args:
            data (dict): dict that contains with the pattern:
            - "post_id": str,
            - "like": int
            - "comment": int

        Returns:
            _type_: _description_
        """
        response = self.calculate_rule_based_reaches(data)

        return response


if __name__ == "__main__":
    data = [
        {
            "post_id": "123",
            # "post_type": "reel",
            "like": 10000,
            # "comment": 3,
            # "share": 10,
            # "view": 1000,
            "follower": 1240320
        },
        {
            "post_id": "456",
            "like": 1033,
            "comment": 4,
            "share": 10,
            "view": 10,
            "follower": 1240320
        }
    ]
    reach_estimation = ReachEstimation("instagram", 'vi')
    print(reach_estimation.calculate(data))
    print(reach_estimation.calculate(data[0]))
    print(reach_estimation.calculate(data[1]))
    print(reach_estimation.calculate_reach_rate(3311842, 5544923))
