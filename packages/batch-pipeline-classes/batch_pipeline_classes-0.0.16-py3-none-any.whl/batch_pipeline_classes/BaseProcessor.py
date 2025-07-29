import logging
import time
from argparse import ArgumentParser

import requests
import json
import datetime as dt
from abc import ABC, abstractmethod

class BaseProcessor(ABC):

    @staticmethod
    def add_default_args(parser:ArgumentParser):
        parser.add_argument("--dates", help="Dates from which to query and load submissions")
        parser.add_argument("--count-init-contests", help="Amount of contests that should be processed during the initial run",default=40)


    @staticmethod
    def query_api(url, headers = {}, **params):
        if params:
            url = url + "?"

            for param, value in params.items():
                url += param + "=" + value + "&"

        resp = requests.get(url=url, headers=headers)
        return resp, url

    @staticmethod
    def process_response(response):
        print(response.status_code)
        print(response.reason)

        converted_response = json.loads(response.content.decode("utf-8"))
        return converted_response

    @staticmethod
    def translate_unix_to_timestamp(unix_time):
        timestamp = dt.datetime.fromtimestamp(unix_time)
        return timestamp

    @staticmethod
    def parse_dates(dates, date_format="%Y-%m-%d") -> (dt.date | None, dt.date | None):

        if not dates:
            return None, None

        date_str_split = dates.split(":")
        if len(date_str_split) < 2:
            return None, None

        try:
            from_date = dt.datetime.strptime(date_str_split[0], date_format).date()
            to_date = dt.datetime.strptime(date_str_split[1], date_format).date()
        except ValueError as ve:
            print(f"Wasn't able to get the dates provided because of the following error -> {str(ve)}")
            return None, None

        if from_date > to_date:
            return to_date, from_date

        return from_date, to_date

    # Class methods
    @abstractmethod
    def write_to_db(self, data, mode, table_name):
        pass

    @abstractmethod
    def read_from_db(self, query):
        pass

    @abstractmethod
    def execute_sql(self, sql_statement: str):
        pass

    @abstractmethod
    def load_last_execution_date(self) -> dt.date:
        pass


    @staticmethod
    def process_contest(
            contest,
            from_date = None,
            to_date = None,
            amount_of_contests = 40
    ):

        min_id = int(contest["max_index"]) - int(amount_of_contests)

        if from_date is None:
            contest_start_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"])
            contest_end_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"] + contest["durationSeconds"])

            if contest["id"] > min_id \
                    and contest["phase"] == "FINISHED"\
                    and contest_end_time.date() < to_date:
                return {
                    "id": contest["id"],
                    "name": contest["name"],
                    "start": contest_start_time,
                    "end": contest_end_time,
                    "duration": contest["durationSeconds"],
                    "type": contest["type"]
                }

        # Manual Parameters provided
        elif from_date is not None and to_date is not None:
            contest_start_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"])
            contest_end_time = BaseProcessor.translate_unix_to_timestamp(contest["startTimeSeconds"] + contest["durationSeconds"])
            if (
                    from_date <= contest_end_time.date() < to_date
                    and contest["phase"] == "FINISHED"
                    # and contest["id"] > min_id
            ):

                return {
                    "id": contest["id"],
                    "name": contest["name"],
                    "start": contest_start_time,
                    "end": contest_end_time,
                    "duration": contest["durationSeconds"],
                    "type": contest["type"]
                }

        return {}


    @staticmethod
    def extract_submissions(contest_id):
        sumbissions = BaseProcessor.establish_connection("https://codeforces.com/api/contest.status", contestId=str(contest_id))

        contest_sumbissions = []
        for subm in sumbissions:
            try:
                contest_sumbissions.append(
                    {
                        "id": subm["id"],
                        "timestamp": BaseProcessor.translate_unix_to_timestamp(subm["creationTimeSeconds"]),
                        "id_contest": subm["contestId"],
                        "id_problem": str(subm["problem"]["contestId"]) + "/" + str(subm["problem"]["index"]),
                        "problem_name": subm["problem"]["name"],
                        "tags": ",".join(subm["problem"]["tags"]),
                        "author": subm["author"]["members"][0].get("handle", "unknown") if subm["author"]["members"] else "unknown",
                        "programming_language": subm["programmingLanguage"],
                        "verdict": subm["verdict"],
                        "time_consumed": subm["timeConsumedMillis"],
                        "memory_usage": subm["memoryConsumedBytes"]
                    }
                )
            except KeyError:
                logging.error(f"The following submission -> {subm}. Failed to be processed! ")

        print("Submissions Extracted!")
        return contest_sumbissions

    @staticmethod
    def handle_error_response(response, api_params):
        if "handles: User with handle" in response.get("comment"):
            users = api_params["handles"] \
                .replace("&", "") \
                .split(";")

            comment_as_list = response.get("comment").split(" ")
            incorrect_user = comment_as_list[comment_as_list.index("handle") + 1]

            users.remove(incorrect_user)
            # sys.exit(0)
            return {"handles": ";".join(users)}, True
        else:
            print(f"Action on the following response {response} is not implemented yet!")
            logging.info(f"Action on the following response {response} is not implemented yet!")
            return api_params, False

    @staticmethod
    def establish_connection(url, **api_params):
        # exception = None
        # retry = 0

        # Variables for tracking errored responses.
        unprocessed_response = {}
        problematic_url = ""

        while True:
            api_response = requests.Response()
            try:

                logging.info("Establishing connection to the API!")
                print("Establishing connection to the API!")

                api_response, merged_url = BaseProcessor.query_api(url, **api_params)
                response = BaseProcessor.process_response(api_response)


                if response and "result" not in response:
                    logging.info(f"Response returned -> {response}, from the url: {merged_url}")
                    print(f"Response returned -> {response}, from the url: {merged_url}")

                    api_params, is_handled = BaseProcessor.handle_error_response(response, api_params)

                    if not is_handled:
                        return []

                    continue
                else:
                    entities = response["result"]

                return entities
            except json.decoder.JSONDecodeError as e:
                # exception = e
                # time.sleep(300)
                print(f"{e} error occured")
                print(f"Response from the API -> {api_response.text}")
                logging.error(f"{e} error occured")
                logging.error(f"Response from the API -> {api_response.text}")
                # retry += 1
                return []
            except requests.exceptions.ConnectionError as e:
                # exception = e
                # time.sleep(300)
                print(f"{e} error occured")
                print(f"Response from the API -> {api_response.text}")
                logging.error(f"{e} error occured")
                logging.error(f"Response from the API -> {api_response.text}")
                # retry += 1
                return []
            except Exception as e:
                # exception = e
                print(f"{e} error occured")
                print(f"Response from the API -> {api_response.text}")
                logging.error(f"{e} error occured")
                logging.error(f"Response from the API -> {api_response.text}")
                return []

        return []

    @staticmethod
    def extract_users(rows):
        unique_names_string = ";".join(rows)

        raw_rows = BaseProcessor.establish_connection("https://codeforces.com/api/user.info", handles=unique_names_string)

        unpacked_rows = [
            {
                "country": raw_row.get("country", "unknown"),
                "rating": raw_row.get("rating", 0),
                "nickname": raw_row["handle"],
                "title": raw_row.get("rank", "none"),
                "registration_date": BaseProcessor.translate_unix_to_timestamp(raw_row["registrationTimeSeconds"])
            }
            for raw_row in raw_rows
        ]

        if not raw_rows:
            return [
                {
                    "country": "none",
                    "rating": 0,
                    "nickname": "none",
                    "title": "none",
                    "registration_date": BaseProcessor.translate_unix_to_timestamp(978368400)
                }
            ]

        return unpacked_rows


