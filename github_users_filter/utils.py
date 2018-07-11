import datetime
import pytz

from models import GithubUser


def process_all_users_data(git_response_data):
    github_users = [
        GithubUser.initialize_from_git_user_api(user_data["url"]) for user_data in git_response_data["items"]]
    for github_user in github_users:
        try:
            github_user.save()
            print "Saved user ", github_user
        except Exception as e:
            print "Unable to save {}".format(github_user), str(e)


def get_current_datetime_ist():
    tz = pytz.timezone("Asia/Calcutta")
    current_datetime = datetime.datetime.now(tz)
    return current_datetime
