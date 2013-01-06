(function($)
{
    var scrollElement = 'html, body';
    var active_input = '';

    // Settings
    var COMMENT_SCROLL_TOP_OFFSET = 40;
    var PREVIEW_SCROLL_TOP_OFFSET = 20;


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
            var $rootEl = $(this);
            var initScrollTop = $rootEl.attr('scrollTop');
            $rootEl.attr('scrollTop', initScrollTop + 1);
            if( $rootEl.attr('scrollTop') == initScrollTop + 1 )
            {
                scrollElement = this.nodeName.toLowerCase();
                $rootEl.attr('scrollTop', initScrollTop);  // Firefox 2 reset
                return false;
            }
        });


        // On load, scroll to proper comment.
        var hash = window.location.hash;
        if( hash.substring(0, 2) == "#c" )
        {
            var id = parseInt(hash.substring(2));
            if( ! isNaN(id))   // e.g. #comments in URL
                scrollToComment(id, 1000);
        }
    });


    function setActiveInput()
    {
        active_input = this.name;
    }


    function onCommentFormSubmit(event)
    {
        event.preventDefault();  // only after ajax call worked.
        var form = event.target;
        var preview = (active_input == 'preview');

        ajaxComment(form, {
            onsuccess: (preview ? null : onCommentPosted),
            preview: preview
        });
        return false;
    }


    function scrollToComment(id, speed)
    {
        // Allow initialisation before scrolling.
        var $comment = $("#c" + id);
        if( $comment.length == 0 ) {
            if( window.console ) console.warn("scrollToComment() - #c" + id + " not found.");
            return;
        }

        if( window.on_scroll_to_comment && window.on_scroll_to_comment({comment: $comment}) === false )
            return;

        // Scroll to the comment.
        scrollToElement( $comment, speed, COMMENT_SCROLL_TOP_OFFSET );
    }


    function scrollToElement( $element, speed, offset )
    {
        if( $element.length )
            $(scrollElement).animate( {scrollTop: $element.offset().top - (offset || 0) }, speed || 1000 );
    }


    function onCommentPosted( comment_id, is_moderated, $comment )
    {
        var $message_span;
        if( is_moderated )
            $message_span = $("#comment-moderated-message").fadeIn(200);
        else
            $message_span = $("#comment-added-message").fadeIn(200);

        setTimeout(function(){ scrollToComment(comment_id, 1000); }, 1000);
        setTimeout(function(){ $message_span.fadeOut(500) }, 4000);
    }


    /*
      Based on django-ajaxcomments, BSD licensed.
      Copyright (c) 2009 Brandon Konkle and individual contributors.

      Updated to be more generic, more fancy, and usable with different templates.
     */
    var commentBusy = false;
    var previewAutoAdded = false;

    function ajaxComment(form, args)
    {
        var onsuccess = args.onsuccess;
        var preview = !!args.preview;

        $('div.comment-error').remove();
        if (commentBusy) {
            return false;
        }

        commentBusy = true;
        var $form = $(form);
        var comment = $form.serialize() + (preview ? '&preview=1' : '');
        var url = $form.attr('action') || './';
        var ajaxurl = $form.attr('data-ajax-action');

        // Add a wait animation
        if( ! preview )
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
                removeErrors();

                if (data.success) {
                    var $added;
                    if( preview )
                        $added = commentPreview(data);
                    else
                        $added = commentSuccess(data);

                    if( onsuccess )
                        args.onsuccess(data.comment_id, data.is_moderated, $added);
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
        $('form.js-comments-form textarea').last().val("");
        $('#id_comment').val('');

        // Show comment
        var had_preview = removePreview();
        var $comments = getCommentsDiv();
        $comments.append(data['html']).removeClass('empty');
        var $new_comment = $comments.children("div.comment-item:last");

        if( had_preview )
            // Avoid double jump when preview was removed. Instead refade to final comment.
            $new_comment.hide().fadeIn(600);
        else
            // Smooth introduction to the new comment.
            $new_comment.hide().show(600);

        return $new_comment;
    }

    function commentPreview(data)
    {
        var $previewarea = $("#comment-preview-area");
        if( $previewarea.length == 0 )
        {
            // If not explicitly added to the HTML, include a previewarea in the comments.
            // This should at least give the same markup.
            getCommentsDiv().append('<div id="comment-preview-area"></div>').addClass('has-preview');
            $previewarea = $("#comment-preview-area");
            previewAutoAdded = true;
        }

        var had_preview = $previewarea.hasClass('has-preview-loaded');
        $previewarea.html(data.html).addClass('has-preview-loaded');
        if( ! had_preview )
            $previewarea.hide().show(600);

        // Scroll to preview, but allow time to render it.
        setTimeout(function(){ scrollToElement( $previewarea, 500, PREVIEW_SCROLL_TOP_OFFSET ); }, 500);
    }

    function commentFailure(data)
    {
        // Show mew errors
        for (var field_name in data.errors) {
            if(field_name) {
                var $field = $('#id_' + field_name);

                // Twitter bootstrap style
                $field.after('<span class="js-errors">' + data.errors[field_name] + '</span>');
                $field.closest('.control-group').addClass('error');
            }
        }
    }

    function removeErrors()
    {
        $('form.js-comments-form .js-errors').remove();
        $('form.js-comments-form .control-group.error').removeClass('error');
    }

    function getCommentsDiv()
    {
        var $comments = $("#comments");
        if( $comments.length == 0 )
            alert("Internal error - unable to display comment.\n\nreason: container is missing in the page.");
        return $comments;
    }

    function removePreview()
    {
        var $previewarea = $("#comment-preview-area");
        var had_preview = $previewarea.hasClass('has-preview-loaded');

        if( previewAutoAdded )
            $previewarea.remove();  // make sure it's added at the end again later.
        else
            $previewarea.html('');

        // Update classes. allowing CSS to add/remove margins for example.
        $previewarea.removeClass('has-preview-loaded')
        $("#comments").removeClass('has-preview');

        return had_preview;
    }

    function removeWaitAnimation()
    {
        // Remove the wait animation and message
        $('#comment-waiting').hide().stop();
    }

})(window.jQuery);
