# Python Standard Library Imports
import operator
import typing as T
from dataclasses import dataclass
from functools import reduce

# Django Imports
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q
from django.http import (
    HttpRequest,
    HttpResponse,
)

# HTK Imports
from htk.api.utils import json_response
from htk.utils import strtobool_safe


# isort: off


@dataclass
class DataTablesQueryParams:
    """Class for holding DataTables Query Parameters

    See: https://datatables.net/examples/data_sources/server_side.html
    """

    @dataclass
    class Column:
        data: T.Optional[str]
        name: T.Optional[str]
        searchable: bool
        orderable: bool
        search_value: T.Optional[str]
        search_regex: bool

        @classmethod
        def nth_from_request(cls, request, n) -> 'DataTablesQueryParams.Column':
            obj = cls(
                data=request.GET.get(f'columns[{n}][data]', None),
                name=request.GET.get(f'columns[{n}][name]', None),
                searchable=strtobool_safe(
                    request.GET.get(f'columns[{n}][searchable]', False)
                ),
                orderable=strtobool_safe(
                    request.GET.get(f'columns[{n}][orderable]', False)
                ),
                search_value=request.GET.get(
                    f'columns[{n}][search][value]', None
                ),
                search_regex=strtobool_safe(
                    request.GET.get(f'columns[{n}][search][regex]', False)
                ),
            )
            return obj

        @property
        def field_name(self):
            return self.name or self.data

    @dataclass
    class Order:
        column_index: int
        is_descending: bool

        @classmethod
        def nth_from_request(cls, request, n) -> 'DataTablesQueryParams.Order':
            try:
                obj = cls(
                    column_index=int(request.GET[f'order[{n}][column]']),
                    is_descending=(
                        request.GET.get(f'order[{n}][dir]', 'asc') == 'desc'
                    ),
                )
            except (TypeError, ValueError):
                obj = None

            return obj

    draw: int
    start: int
    length: int
    search_value: T.Optional[str]
    search_regex: bool
    columns: list['DataTablesQueryParams.Column']
    ordering: list['DataTablesQueryParams.Order']

    @classmethod
    def from_request(cls, request: HttpRequest):
        # NOTE: uncomment to debug, since DataTables requests sends A TON of information
        # from htk.utils.debug import slack_debug
        # params_kv = '- ' + '\n - '.join(
        #     [f'{k}={v}' for k, v in request.GET.items()]
        # )
        # slack_debug(params_kv)

        dtqp = DataTablesQueryParams(
            draw=request.GET.get('draw', 1),
            start=int(request.GET.get('start', 0)),
            length=int(request.GET.get('length', 25)),
            search_value=request.GET.get('search[value]', None),
            # https://datatables.net/reference/option/search.regex
            search_regex=strtobool_safe(
                request.GET.get('search[regex]', False)
            ),
            columns=cls._extract_columns(request),
            ordering=cls._extract_ordering(request),
        )
        return dtqp

    @classmethod
    def _extract_columns(
        cls, request: HttpRequest
    ) -> list['DataTablesQueryParams.Column']:
        """Extracts the datatables columns query parameters from the request

        Example URL params:

        columns[0][data]=foo
        columns[0][name]=
        columns[0][searchable]=true
        columns[0][orderable]=true
        columns[0][search][value]=
        columns[0][search][regex]=false
        columns[1][data]=bar
        columns[1][name]=
        columns[1][searchable]=true
        columns[1][orderable]=true
        columns[1][search][value]=
        columns[1][search][regex]=false
        columns[2][data]=baz
        columns[2][name]=
        columns[2][searchable]=true
        columns[2][orderable]=true
        columns[2][search][value]=
        columns[2][search][regex]=false
        columns[N][data]=qux
        columns[N][name]=
        columns[N][searchable]=true
        columns[N][orderable]=true
        columns[N][search][value]=
        columns[N][search][regex]=false

        """
        end = None

        # use a `while` loop because we don't know in advance how many columns there are
        # a well-formed payload would have integer indexes in strictly increasing order, starting from 0
        i = 0
        while True:
            # just check if the 'name' column is present
            key = f'columns[{i}][name]'
            if key in request.GET:
                end = i
                i += 1
            else:
                # no more columns
                break

        columns = (
            [
                DataTablesQueryParams.Column.nth_from_request(request, i)
                for i in range(end + 1)
            ]
            if end is not None
            else []
        )

        return columns

    @classmethod
    def _extract_ordering(
        cls, request: HttpRequest
    ) -> list['DataTablesQueryParams.Order']:
        """Extracts the datatables columns query parameters from the request

        Example URL params:

        order[0][column]=42
        order[0][dir]=asc
        order[1][column]=17
        order[1][dir]=desc

        """
        end = None

        # use a `while` loop because we don't know in advance how many order parameters there are
        # a well-formed payload would have integer indexes in strictly increasing order, starting from 0
        i = 0
        while True:
            # just check if the 'column' column is present
            key = f'order[{i}][column]'
            if key in request.GET:
                end = i
                i += 1
            else:
                # no more columns
                break

        ordering = (
            [
                o
                for i in range(end + 1)
                if (
                    o := DataTablesQueryParams.Order.nth_from_request(
                        request, i
                    )
                )
            ]
            if end is not None
            else []
        )

        return ordering

    @property
    def order_by(self):
        def _format(column_index: int, is_descending: bool) -> str:
            try:
                column = self.columns[column_index]
                prefix = '-' if is_descending else ''
                value = f'{prefix}{column.field_name}'
            except IndexError:
                # payload was either tampered with or application glitched
                value = None
            return value

        order_by = [
            v
            for o in self.ordering
            if (v := _format(o.column_index, o.is_descending))
        ]

        return order_by


def model_datatables_api_get_view(
    request: HttpRequest,
    model_class: models.Model,
    base_exclusion: T.Optional[Q] = None,
    base_filter: T.Optional[Q] = None,
    search_fields: T.Optional[list[str]] = None,
    default_ordering: T.Optional[list[str]] = None,
) -> HttpResponse:
    """Generic API view for handling a server-side processed
    Datatables request.
    """

    ##
    # Unpack DataTables query parameters

    dtqp = DataTablesQueryParams.from_request(request)

    ##
    # Build the QuerySet

    q = model_class.objects

    if base_exclusion:
        q = q.exclude(base_exclusion)

    if base_filter:
        q = q.exclude(base_filter)

    base_q = q

    if search_fields and dtqp.search_value:
        # chain search fields with an OR search
        search_criteria = [
            Q(**{search_field: dtqp.search_value})
            for search_field in search_fields
        ]
        filter_param = reduce(operator.or_, search_criteria)
        q = q.filter(filter_param)
    else:
        q = q.all()

    ordering = dtqp.order_by or default_ordering

    if ordering:
        q = q.order_by(*ordering)

    ##
    # Compute the paginated results and pagination details

    p = Paginator(q, dtqp.length)

    records_total = base_q.count()
    records_filtered = q.count()

    page_num = dtqp.start // dtqp.length + 1

    ##
    # Build the response

    response = json_response(
        {
            'draw': dtqp.draw,
            'data': [obj.as_dict() for obj in p.page(page_num)],
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
        },
    )
    return response
