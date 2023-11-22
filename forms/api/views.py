from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from form.models import Template, Field
from .serializers import FieldSerializer, TemplateSerializer
from django.db.models import Q
import re


class FieldsView(APIView):
    def get(self, request, format=None):
        data = Field.objects.all()

        serializer = FieldSerializer(data, many=True)

        return Response(serializer.data)


class TemplateView(APIView):
    def get(self, request, format=None):
        data = Template.objects.all()

        serializer = TemplateSerializer(data, many=True)

        return Response(serializer.data)

def validate_field(value):
    pattern_mobile = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    pattern_dd_mm_yyyy = r'^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)[0-9]{2}$'
    pattern_yyyy_mm_dd = r'^\d{4}-\d{2}-\d{2}$'
    pattern_mail = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    value_type = ''

    if re.match(pattern_dd_mm_yyyy, value) is not None:
        value_type = 'DATE'
    elif re.match(pattern_yyyy_mm_dd, value) is not None:
        value_type = 'DATE'
    elif re.match(pattern_mobile, value) is not None:
        value_type = 'PHONE'
    elif re.match(pattern_mail, value) is not None:
        value_type = 'EMAIL'
    else:
        value_type = 'TEXT'

    return value_type






class SearchView(APIView):
    def get(self, request, format=None):
        query = self.request.query_params
        fields_name = list(query.keys())
        fields_values = list(query.items())
        values = list(query.values())
        # print(fields_name)
        # print(fields_values)
        for item in zip(fields_name, values):
            # print(item[0], validate_field(item[1]))
            res = Field.objects.filter(name=item[0], field_type=validate_field(item[1]))
            if len(res) != 0:
                continue
            else:
                data = {
                    'error': 'Form not found',
                }
            for i in range(len(fields_values)):
                data[f'{fields_values[i][0]}'] = f'{validate_field(fields_values[i][1])}'


            return Response(data, status=404)

        fields_id = Field.objects.filter(name__in=fields_name).values_list('id', flat=True)
        if len(fields_name) != len(fields_id):

            data = {
                    'error': 'Form not found',
                }

            for i in range(len(fields_values)):
                data[f'{fields_values[i][0]}'] = f'{validate_field(fields_values[i][1])}'

            return Response(data, )

        queryset = Template.objects.all()
        for f in fields_id:
            q_list = Q()
            q_list &= Q(fields__id=f)
            qs = queryset.filter(q_list)

        print(qs.values('id'))
        res = qs.values_list('id', flat=True)


        data = Template.objects.filter(id__in=res)
        serializer = TemplateSerializer(data, many=True)

        return Response(serializer.data)


class SearchFormView(APIView):
    def get(self, request, format=None):
        query = self.request.query_params
        fields_name = list(query.keys())
        # fields_values = list(query.items())

        fields_id = Field.objects.filter(name__in=fields_name).values_list('id', flat=True)
        if len(fields_name) == len(fields_id):
            queryset = Template.objects.all()
            for f in fields_id:
                q_list = Q()
                q_list &= Q(fields__id=f)
                qs1 = queryset.filter(q_list)

            result = qs1.values_list('name', flat=True)
            print(len(result))
            if len(result) == 1:
                res = []
                data = {}
                data[f'name'] = f'{result[0]}'
                res = Template.objects.filter(name=result[0]).values_list('fields__name', 'fields__field_type')
                for j in range(len(res)):
                    print(res[j])
                    data[f'{res[j][0]}'] = f'{res[j][1]}'

                return Response(data, status=200)
            else:
                res = qs1.values_list('id', flat=True)

                data = Template.objects.filter(id__in=res)
                print(data)
                serializer = TemplateSerializer(data, many=True)

                return Response(serializer.data)
        else:
            data = {
                'ошибка': 'Такой формы нет',
            }
            print('err')
            return Response(data, )


    # from django.db.models import Q
    # q_list = Q()
    # for word in 'текст для поиска'.split():
    #     q_list |= Q(name__icontains=word)
    #     q_list |= Q(surname__icontains=word)
    #     q_list |= Q(text__icontains=word)
    # queryset = ModelName.objects.filter(q_list)

    # from django.db.models import Q
    # queryset = Template.objects.all()
    # for word in 'текст для поиска'.split():
    #     q_list = Q()
    #     q_list |= Q(name__icontains=word)
    #     q_list |= Q(surname__icontains=word)
    #     q_list |= Q(text__icontains=word)
    #     queryset = queryset.filter(q_list)

    # fields_name = ["user_name", "user_id"]
    # fields_id = Field.objects.filter(name__in=fields_name).values_list('id', flat=True)
    # queryset = Template.objects.all()
    # for f in fields_id:
    #     q_list = Q()
    #     q_list &= Q(fields__id=f)
    #     qs = queryset.filter(q_list)
    #
    # print(qs)
    # res = qs.values_list('id', flat=True)
    # res = qs.values('id')


# fields_name = ['user_name', 'user_email']
# fields_values = ['nik@mail.com', 'mail@mail.ru']
#
# def validate_type(names: list, values: list):
#     for item in zip(names, values):
#         print(item)
#
#
# validate_type(fields_name, fields_values)