from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Log
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import csv
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Log
from .serializers import LogSerializer


def log_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'newest')
    per_page = request.GET.get('per_page', '10')
    message_type = request.GET.get('message_type', 'all')
    source = request.GET.get('source', 'all')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10 

    logs = Log.objects.all()

    if query:
        logs = logs.filter(Q(message__icontains=query))

    if message_type != 'all':
        logs = logs.filter(message_type=message_type)

    if source != 'all':
        logs = logs.filter(source=source)

    if date_from:
        logs = logs.filter(created_at__gte=date_from)

    if date_to:
        logs = logs.filter(created_at__lte=date_to)

    if sort == 'newest':
        logs = logs.order_by('-created_at')
    else:
        logs = logs.order_by('created_at')

    paginator = Paginator(logs, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('logs/log_list_content.html', {
            'page_obj': page_obj,
            'query': query,
            'sort': sort,
            'per_page': per_page,
            'message_type': message_type,
            'source': source,
            'date_from': date_from,
            'date_to': date_to
        })
        return JsonResponse({'html': html})
    
    return render(request, 'logs/log_list.html', {
        'page_obj': page_obj,
        'query': query,
        'sort': sort,
        'per_page': per_page,
        'message_type': message_type,
        'source': source,
        'date_from': date_from,
        'date_to': date_to,
    })


def export_logs(request):
    query = request.GET.get('q', '')
    message_type = request.GET.get('message_type', 'all')
    source = request.GET.get('source', 'all')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    export_format = request.GET.get('format', 'csv')

    logs = Log.objects.all()

    if query:
        logs = logs.filter(Q(message__icontains=query))

    if message_type != 'all':
        logs = logs.filter(message_type=message_type)

    if source != 'all':
        logs = logs.filter(source=source)

    if date_from:
        logs = logs.filter(created_at__gte=date_from)

    if date_to:
        logs = logs.filter(created_at__lte=date_to)

    if export_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="logs.csv"'
        writer = csv.writer(response)
        writer.writerow(['Message', 'Message Type', 'Source', 'Created At'])
        for log in logs:
            writer.writerow([log.message, log.message_type, log.source, log.created_at])
    else:
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="logs.txt"'
        for log in logs:
            response.write(f"{log.message} | {log.message_type} | {log.source} | {log.created_at}\n")

    return response


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def get_queryset(self):
        queryset = Log.objects.all()
        query = self.request.query_params.get('q', '')
        message_type = self.request.query_params.get('message_type', 'all')
        source = self.request.query_params.get('source', 'all')
        date_from = self.request.query_params.get('date_from', '')
        date_to = self.request.query_params.get('date_to', '')

        if query:
            queryset = queryset.filter(Q(message__icontains=query))

        if message_type != 'all':
            queryset = queryset.filter(message_type=message_type)

        if source != 'all':
            queryset = queryset.filter(source=source)

        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)

        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset

    @action(detail=False, methods=['get'])
    def export(self, request):
        logs = self.get_queryset()
        export_format = request.query_params.get('format', 'csv')

        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="logs.csv"'
            writer = csv.writer(response)
            writer.writerow(['Message', 'Message Type', 'Source', 'Created At'])
            for log in logs:
                writer.writerow([log.message, log.message_type, log.source, log.created_at])
        else:
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="logs.txt"'
            for log in logs:
                response.write(f"{log.message} | {log.message_type} | {log.source} | {log.created_at}\n")

        return response