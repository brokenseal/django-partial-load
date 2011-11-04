/*
*
*
* 
* */

(function($, undefined){
    var
        blocksCache = {}
        ,allBlocks = null
        ,$document = $(document)
        ,collectBlocks = function(blockName){
                
            if(blockName !== undefined && blocksCache[blockName] === undefined){

                blocksCache[blockName] = $document.find('*[data-block-name="' + blockName + '"]');
                
            } else if(blockName === undefined && allBlocks === null) {
                allBlocks = $document.find('*[data-block-name]');
                allBlocks.each(function(){
                    var
                        block = $(this)
                    ;
                    
                    blocksCache[ block.attr('data-block-name') ] = block;
                });
            }

            if(blockName === undefined){
                return blocksCache;
            }
        
            return blocksCache[blockName];
        }
    ;
    
    $.partialLoad = function(options){
        var
            blockNameList = options.blockNameList || []
            ,blockName
        ;

        if(blockNameList.length == 0) {
            // if the block name list is empty, load all the blocks from this document
            collectBlocks();
            
            for(blockName in blocksCache) {
                blockNameList.push(blockName);
            }
        }
        
        return $.ajax({
            url: options.url
            ,headers: {
                'X-Load-Blocks': blockNameList
            }
            ,success: function(blocks){
                var
                    len = blockNameList.length
                ;

                // iterate over the block names and update the blocks on the DOM
                while(len--){
                    blockName = blockNameList[len];
                    blocksCache[blockName].html(blocks[blockName]);
                }
                
                if($.isFunction(options.success)){
                    options.success(blocks);
                }
            }
            ,error: function(){
                if($.isFunction(options.error)){
                    options.error(blocks);
                }
            }
        });
    };

    $.fn.partialLoad = function(options){
        var
            opts = $.extend({}, $.fn.defaultOptions)
        ;
        opts = $.extend(options);
        
        this.each(function(){
            var
                link = $(this)
            ;

            link.click(function(){
                $.partialLoad({
                    url: link.attr('href')
                    ,blockNameList: options.blockNameList
                });
                return false;
            });
        });
    };

    $.fn.partialLoad.defaultOptions = {
        blockNameList: []               // a list of block names to retrieve from the server and update on the DOM
                                        // if left blank, all the blocks will be reloaded
        ,success: null                  // success callback
        ,error: null                    // error callback
    };
})(jQuery);