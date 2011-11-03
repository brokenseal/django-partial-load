from json import dumps

from django.template.response import HttpResponse, SimpleTemplateResponse

from partial_load import loader


def partial_load(func):
    def _inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)

        if request.is_ajax() and request.META.has_key('HTTP_X_LOAD_BLOCKS'):
            if not isinstance(response, SimpleTemplateResponse):
                raise Exception("The response must be an instance of TemplateResponse.")

            block_list = request.META['HTTP_X_LOAD_BLOCKS'].split(',')
            template = loader.get_template(response.template_name)
            result = loader.render_template_blocks(template, block_list, response.context_data)

            return HttpResponse(dumps(result), mimetype="application/json")

        return response
    
    return _inner