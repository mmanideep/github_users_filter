import requests

from multiprocessing import Pool

from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from decorators import log_search_api_call
from non_db_models.QueryProcessor import QueryProcessor
from settings import GITHUB_USERS_API, GIT_TOKEN
from utils import process_all_users_data


class SearchGitHubUsers(APIView):

    renderer_classes = (JSONRenderer,)

    @log_search_api_call
    def post(self, request):
        try:
            query_processor = QueryProcessor(**request.data)
            complete_query = query_processor.get_complete_query()
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        result_json = requests.get(
            "{}{}".format(GITHUB_USERS_API, complete_query),
            headers={"Authorization": "token {}".format(GIT_TOKEN)}
        ).json()
        pool = Pool(processes=1)
        pool.apply_async(process_all_users_data, [result_json])

        # process_all_users_data(git_response_data=result_json)
        return Response(result_json)
