(function($)
{
    var scrollElement = 'html, body';
    var active_input = '';

    // Settings
    var SCROLL_TOP_OFFSET = 60;


    $.fn.ready(function()
    {
        var commentform = $('form.js-comments-form');
        if( commentform.length > 0 )
        {
            // Detect last active input.
            // Submit if return is hit, or any button other then preview is hit.
            commentform.find(':input').focus(setActiveInput).mousedown(setActiveInput);
            commentform.submit(onCommentFormSubmit);
        }


        // Find the element to use for scrolling.
        // This code is much shorter then jQuery.scrollTo()
        $('html, body').each(function()
        {
            // See which tag updates the scrollTop attribute
            var initScrollTop = $(this).attr('scrollTop');
            $(this).attr('scrollTop', initScrollTop + 1);
            if( $(this).attr('scrollTop') == initScrollTop + 1 )
            {
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
        var form = event.target;
        if( active_input != 'preview' )
        {
            event.preventDefault();  // only after ajax call worked.
            ajaxComment(form, {
                'complete': onCommentPosted
            });
            return false;
        }
        return true;
    }


    function scrollToComment(id, speed)
    {
        // Allow initialisation before scrolling.
        var $comment = $("#c" + id);
        if( window.on_scroll_to_comment && window.on_scroll_to_comment({comment: $comment}) === false )
            return;

        // Scroll to the comment.
        if( $comment.length )
            $(scrollElement).animate( {scrollTop: $comment.offset().top - SCROLL_TOP_OFFSET }, speed || 1000 );
    }


    function onCommentPosted($comment)
    {
        var id = $comment.attr('id');

        if( id.substring(0, 1) == 'c' )
        {
            id = parseInt(id.substring(1));
            $("#comment-added-message").fadeIn(200);

            setTimeout(function(){ scrollToComment(id, 1000); }, 1000);
            setTimeout(function(){ $("#comment-added-message").fadeOut(500) }, 4000);
        }
    }


    /*
      Based on django-ajaxcomments, BSD licensed.
      Copyright (c) 2009 Brandon Konkle and individual contributors.

      Updated to be more generic, more fancy, and usable with different templates.
     */
    var commentBusy = false;

    function ajaxComment(form, args)
    {
        var oncomplete = args.complete;

        $('div.comment-error').remove();
        if (commentBusy) {
            return false;
        }

        commentBusy = true;
        var $form = $(form);
        var comment = $form.serialize();
        var url = $form.attr('action') || './';
        var ajaxurl = $form.attr('data-ajax-action');

        // Add a wait animation
        $('#comment-waiting').fadeIn(1000);

        // Use AJAX to post the comment.
        $.ajax({
            type: 'POST',
            url: ajaxurl || url,
            data: comment,
            dataType: 'json',
            success: function(data) {
                commentBusy = false;
                removeWaitAnimation();

                if (data.success) {
                    commentSuccess(data);
                    var added = $("#comments > :last-child");
                    if( oncomplete ) oncomplete(added);
                }
                else {
                    commentFailure(data);
                }
            },
            error: function(data) {
                commentBusy = false;
                removeWaitAnimation();

                // Submit as non-ajax instead
                //$form.unbind('submit').submit();
            }
        });

        return false;
    }

    function commentSuccess(data)
    {
        // Clean form
        $('form.js-comments-form textarea')[0].value = "";
        $('#id_comment').val('');

        // Show comment
        $('#comments').append(data['html']);
        $('div.comment:last').show('slow');
    }

    function commentFailure(data)
    {
        // Show errors
        $('form.js-comments-form ul.errorlist').each(function() {
          this.parentNode.removeChild(this);
        });

        for (var error in data.errors) {
            $('#id_' + error).parent().before(data.errors[error])
        }
    }

    function removeWaitAnimation()
    {
        // Remove the wait animation and message
        $('#comment-waiting').hide().stop();
    }

})(window.jQuery);
