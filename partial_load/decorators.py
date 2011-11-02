from django.template.response import TemplateResponse, HttpResponse
from partial_load import loader
from json import dumps


def partial_load(func):
    def _inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)

        if request.is_ajax() and request.META.has_key('HTTP_X_LOAD_BLOCKS'):
            if not isinstance(response, TemplateResponse):
                raise Exception("The response must be an instance of TemplateResponse.")

            block_list = request.META['HTTP_X_LOAD_BLOCKS'].split(',')
            result = loader.render_template_blocks(response.template, block_list, response.context)

            return HttpResponse(dumps(result), mimetype="application/json")
            
    return _inner