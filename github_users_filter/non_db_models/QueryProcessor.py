import operator
import datetime

from django.core.exceptions import ValidationError

INT_OPERATOR_SYMBOL_MAPPER = {
    "eq": "=",
    "gte": ">=",
    "gt": ">",
    "lte": "<=",
    "lt": "<"
}

DATE_OPERATOR_SYMBOL_MAPPER = {
    "eq": "=",
    "gte": ">=",
    "gt": ">",
    "lte": "<=",
    "lt": "<",
    "bt": ".."
}

ALLOWED_IN_VALUES = ["login", "email", "fullname"]


class QueryProcessor(object):

    def __init__(self, **kwargs):
        """
        eg:
            {
                'query': 'foobar',
                'repos': {
                        'value': 100,
                        'operator': 'gte'
                    },
                'created': {
                    'value': '2018'
                    }
            }
        operators can be 'gte', 'lte', 'lt', 'gt', 'in'

        """
        self.all_queries_list = []
        self.query = kwargs.get("query")
        self.in_query = kwargs.get("in_query")
        self.repos = kwargs.get("repos")
        self.location = kwargs.get("location")
        self.lang = kwargs.get("lang")
        self.created = kwargs.get("created")
        self.followers = kwargs.get("followers")

    query = property(operator.attrgetter('_query'))
    repos = property(operator.attrgetter('_repos'))
    location = property(operator.attrgetter('_location'))
    lang = property(operator.attrgetter('_lang'))
    created = property(operator.attrgetter('_created'))
    followers = property(operator.attrgetter('_followers'))
    in_query = property(operator.attrgetter('_in_query'))

    @query.setter
    def query(self, val):
        if not val:
            raise ValidationError("query is required")
        self._query = val
        self.all_queries_list.append(self._query)

    @in_query.setter
    def in_query(self, val=None):
        if not val:
            return
        if val not in ALLOWED_IN_VALUES:
            raise ValidationError("Only {} are allowed for in_query".format(ALLOWED_IN_VALUES))
        self._in_query = "in:%s" % val
        self.all_queries_list.append(self._in_query)

    @repos.setter
    def repos(self, query_dict=None):
        if not isinstance(query_dict, dict):
            return
        if query_dict.get("value") < 0:
            raise ValidationError("repos cannot be less than zero")
        try:
            oper = INT_OPERATOR_SYMBOL_MAPPER[query_dict["operator"]]
            value = query_dict["value"]
            self._repos = "repos:%s%d" % (oper, value)
            self.all_queries_list.append(self._repos)
        except (TypeError, KeyError):
            raise ValidationError("please enter valid input for repos query")

    @location.setter
    def location(self, val=None):
        if val is not None and isinstance(val, basestring):
            self._location = "location:%s" % val
            self.all_queries_list.append(self._location)
        elif val is not None and not isinstance(val, basestring):
            raise ValidationError("location should be string")

    @lang.setter
    def lang(self, val=None):
        if val is not None and isinstance(val, basestring):
            self._lang = "language:%s" % val
            self.all_queries_list.append(self._lang)
        elif val is not None and not isinstance(val, basestring):
            raise ValidationError("lang should be string")

    @created.setter
    def created(self, query_dict=None):
        if query_dict is None:
            return
        if not isinstance(query_dict, dict):
            raise ValidationError("please enter valid query dictionary for created")
        try:
            values = []
            if "value" in query_dict:
                values.append(query_dict["value"])
                datetime.datetime.strptime(values[0], "%Y-%m-%d")
                oper = DATE_OPERATOR_SYMBOL_MAPPER[query_dict["operator"]]
                self._created = "created:%s%s" % (oper, values[0])

            elif "values" in query_dict:
                values.extend(query_dict["values"])
                datetime.datetime.strptime(values[0], "%Y-%m-%d")
                datetime.datetime.strptime(values[1], "%Y-%m-%d")
                if query_dict.get("operator") != "bt":
                    raise ValidationError("Please enter valid operator for created query dict")
                oper = DATE_OPERATOR_SYMBOL_MAPPER[query_dict["operator"]]
                self._created = "created:%s%s%s" % (values[0], oper, values[1])
            else:
                raise ValidationError("Please enter value or values for created query dict")
            self.all_queries_list.append(self._created)

        except ValueError:
            raise ValidationError("Invalid date format")
        except (TypeError, KeyError):
            raise ValidationError("Invalid operator found for created dict")

    @followers.setter
    def followers(self, query_dict=None):
        if not isinstance(query_dict, dict):
            return
        if query_dict.get("value") < 0:
            raise ValidationError("repos cannot be less than zero")
        try:
            oper = INT_OPERATOR_SYMBOL_MAPPER[query_dict["operator"]]
            value = query_dict["value"]
            self._followers = "followers:%s%d" % (oper, value)
            self.all_queries_list.append(self._followers)
        except (TypeError, KeyError):
            raise ValidationError("please enter valid input for repos query")

    def get_complete_query(self):
        return "+".join(self.all_queries_list)
