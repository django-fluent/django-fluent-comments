(function($)
{
    var scrollElement = 'html, body';
    var active_input = '';

    // Parse script parameters!
    var scripts = document.getElementsByTagName('script');
    var myscript = scripts[ scripts.length - 1 ];
    var cap = /[?&]STATIC_URL=([^&]+)/.exec(myscript.src);

    var STATIC_URL = cap[1] || window.STATIC_URL || '/static/';
    var ajaxmedia = STATIC_URL + 'fluent_comments/';


    $.fn.ready(function()
    {
        var commentform = $('#comment-form > form');
        if( commentform.length > 0 )
        {
          // Detect last active input.
          // Submit if return is hit, or any button other then preview is hit.
          commentform.find(':input').focus(setActiveInput).mousedown(setActiveInput);
          commentform.submit(onCommentFormSubmit);
        }


        // Find the element to use for scrolling.
        // This code is much shorter then jQuery.scrollTo()
        $('html, body').each(function () {
            var initScrollTop = $(this).attr('scrollTop');
            $(this).attr('scrollTop', initScrollTop + 1);
            if ($(this).attr('scrollTop') == initScrollTop + 1) {
                scrollElement = this.nodeName.toLowerCase();
                $(this).attr('scrollTop', initScrollTop);  // Firefox 2 reset
                return false;
            }
        });


        // On load, scroll to proper comment.
        var hash = window.location.hash;
        if( hash.substring(0, 2) == "#c" )
        {
          var id = parseInt(hash.substring(2));
          scrollToComment(id, 1000);
        }
    });


    function setActiveInput()
    {
        active_input = this.name;
    }

    function onCommentFormSubmit(event)
    {
        if( active_input != 'preview' )
        {
            ajaxComment({
                'media': ajaxmedia,
                'complete': onCommentPosted
            });
            event.preventDefault();  // only after ajax call worked.
            return false;
        }
        return true;
    }


    function scrollToComment(id, speed)
    {
        // Allow initialisation for scrolling.
        if( window.on_scroll_to_comment && window.on_scroll_to_comment(id) === false )
            return;

        // Scroll to the comment.
        var $comment = $("#c" + id);
        if( $comment.length )
            $(scrollElement).animate( {scrollTop: $comment.offset().top }, speed || 1000 );
    }


    function onCommentPosted($comment)
    {
        var id = $comment.attr('id');

        if( id.substring(0, 1) == 'c' )
        {
            id = parseInt(id.substring(1));
            $("#comment-added-message").fadeIn(200);

            setTimeout(function(){
              scrollToComment(id, 1000);
            }, 1000);

            setTimeout(function(){
              $("#comment-added-message").fadeOut(500);
            }, 4000);
        }
    }
})(window.jQuery);
