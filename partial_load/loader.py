from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context, RequestContext
from django.http import HttpResponse

from django.template.base import SimpleNode


class BlockNotFound(Exception):
    pass


def get_template(template):
    if isinstance(template, (tuple, list)):
        return loader.select_template(template)
    return loader.get_template(template)

def render_template_blocks(template, block_list, context):
    """
    Renders a single block from a template. This template should have previously been rendered.
    """
    return render_template_blocks_nodelist(template.nodelist, block_list, context)

def render_template_blocks_nodelist(nodelist, block_list, context):
    block_map = {}

    print "nodelist: %s" % nodelist

    for node in nodelist:
        print "node class: %s" % node.__class__.__name__
        
        if isinstance(node, BlockNode) and node.name in block_list:
            print "node name: %s" % node.name
            block_map.setdefault(node.name, node.render(context))
            
        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            if hasattr(node, key):
                try:
                    inner_block_map = render_template_blocks_nodelist(getattr(node, key), block_list, context)
                except:
                    pass
                else:
                    print "inner_block_map 1: %s" % inner_block_map
                    block_map.update(inner_block_map)
                    inner_block_map = {}
                    
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            try:
                inner_block_map = render_template_blocks(node.get_parent(context), block_list, context)
            except BlockNotFound:
                pass
            else:
                print "inner_block_map 2: %s" % inner_block_map
                block_map.update(inner_block_map)
                            
    return block_map

def render_block_to_string(template_name, block_list, dictionary={}, context_instance=None):
    """
    Loads the given template_name and renders the given block with the given dictionary as
    context. Returns a string.
    """
    template = get_template(template_name)
    
    if context_instance is not None:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
        
    template.render(context_instance)
    
    return render_template_blocks(template, block_list, context_instance)

def direct_block_to_template(request, template, block_list, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given block in a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    if extra_context is None:
        extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    c = RequestContext(request, dictionary)
    t = get_template(template)
    t.render(c)
    return HttpResponse(render_template_blocks(t, block_list, c), mimetype=mimetype)