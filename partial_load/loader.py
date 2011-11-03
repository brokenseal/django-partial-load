from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context



def get_template(template):
    if isinstance(template, (tuple, list)):
        return loader.select_template(template)
    return loader.get_template(template)

def render_template_blocks(template, block_list, context):
    """
        Renders a list of blocks from a template.
        Return a dictionary of rendered template blocks.
    """
    return render_blocks(template.nodelist, block_list, context)

def render_blocks(nodelist, block_list, context):
    block_map = {}
    
    for node in nodelist:
        if isinstance(node, BlockNode) and node.name in block_list:
            block_map.setdefault(node.name, node.render(Context(context)))
            
        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            if hasattr(node, key):
                inner_block_map = render_blocks(getattr(node, key), block_list, context)
                block_map.update(inner_block_map)
                    
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            inner_block_map = render_template_blocks(node.get_parent(context), block_list, context)
            block_map.update(inner_block_map)
                            
    return block_map