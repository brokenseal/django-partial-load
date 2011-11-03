from json import dumps

from django.template.response import SimpleTemplateResponse
from django.http import HttpResponse

from partial_load import loader


class PartialLoadMiddleware(object):
    def process_response(self, request, response):
        # since the middleware is a most generic way of handling with the request/response process, let's check
        # if the response is a SimpleTemplateResponse instance first
        if request.is_ajax() and isinstance(response, SimpleTemplateResponse)\
                and request.META.has_key('HTTP_X_LOAD_BLOCKS'):
            
            block_list = request.META['HTTP_X_LOAD_BLOCKS'].split(',')
            result = loader.render_template_blocks(response.template, block_list, response.context)

            return HttpResponse(dumps(result), mimetype="application/json")
