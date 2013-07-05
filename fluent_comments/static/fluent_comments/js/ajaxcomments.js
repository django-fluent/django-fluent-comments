(function($)
{
    var scrollElement = 'html, body';
    var active_input = '';

    // Settings
    var COMMENT_SCROLL_TOP_OFFSET = 40;
    var PREVIEW_SCROLL_TOP_OFFSET = 20;
    var ENABLE_COMMENT_SCROLL = true;


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


        // Bind events for threaded comment reply
        if($.fn.on) {
            // jQuery 1.7+
            $('body').on('click', '.comment-reply-link', showThreadedReplyForm);
        }
        else {
            $('.comment-reply-link').live('click', showThreadedReplyForm);
        }

        $('.comment-cancel-reply-link').click(cancelThreadedReplyForm);

        var $all_forms = $('.js-comments-form');
        $all_forms
          .each(function(){
            var $form = $(this);
            var object_id = parseInt($form.attr('data-object-id'));  // Supported in all jQuery versions.
            $form.wrap('<div class="js-comments-form-orig-position" id="comments-form-orig-position-' + object_id + '"></div>');
          });

        // HACK HACK HACK
        // Restore the parent-id when the server is unable to do so.
        // See if the comment-form can be found near to the current list of comments.
        var $all_comment_divs = $("div.comments");
        var $all_broken_comment_divs = $all_comment_divs.filter("#comments-None").add($all_comment_divs.filter('#comments-'));
        $all_broken_comment_divs.each(function(){
            var node = this.parentNode;
            for(var i = 0; i < 4; i++) {
                var $form = $(node).find('.js-comments-form');
                if($form.length) {
                    var target_object_id = parseInt($form.attr('data-object-id'));
                    if(target_object_id) {
                        $(this).attr('id', 'comments-' + target_object_id).attr('data-object-id', target_object_id);
                    }
                    break;
                }

                node = node.parentNode;
                if(! node) break;
            }
        });

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
        if( ! ENABLE_COMMENT_SCROLL ) {
            return;
        }
        
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
        if( ! ENABLE_COMMENT_SCROLL ) {
            return;
        }
        
        if( $element.length )
            $(scrollElement).animate( {scrollTop: $element.offset().top - (offset || 0) }, speed || 1000 );
    }


    function onCommentPosted( comment_id, object_id, is_moderated, $comment )
    {
        var $message_span;
        if( is_moderated )
            $message_span = $("#comment-moderated-message-" + object_id).fadeIn(200);
        else
            $message_span = $("#comment-added-message-" + object_id).fadeIn(200);

        setTimeout(function(){ scrollToComment(comment_id, 1000); }, 1000);
        setTimeout(function(){ $message_span.fadeOut(500) }, 4000);
    }


    function showThreadedReplyForm(event) {
        event.preventDefault();

        var $a = $(this);
        var comment_id = $a.data('comment-id');

        $('#id_parent').val(comment_id);
        $('.js-comments-form').insertAfter($a.closest('.comment-item'));
    }


    function cancelThreadedReplyForm(event) {
        if(event)
            event.preventDefault();

        var $form = $(event.target).closest('form.js-comments-form');
        resetForm($form);
    }

    function resetForm($form) {
        var object_id = parseInt($form.attr('data-object-id'));
        $($form[0].elements['comment']).val('');  // Wrapped in jQuery to silence errors for missing elements.
        $($form[0].elements['parent']).val('');   // Reset parent field in case threaded comments are used.
        $form.appendTo($('#comments-form-orig-position-' + object_id));
    }


    /*
      Based on django-ajaxcomments, BSD licensed.
      Copyright (c) 2009 Brandon Konkle and individual contributors.

      Updated to be more generic, more fancy, and usable with different templates.
     */
    var previewAutoAdded = false;

    function ajaxComment(form, args)
    {
        var onsuccess = args.onsuccess;
        var preview = !!args.preview;

        if (form.commentBusy) {
            return false;
        }

        form.commentBusy = true;
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
                form.commentBusy = false;
                removeWaitAnimation($form);
                removeErrors($form);

                if (data.success) {
                    var $added;
                    if( preview )
                        $added = commentPreview(data);
                    else
                        $added = commentSuccess($form, data);

                    if( onsuccess )
                        args.onsuccess(data.comment_id, data.object_id, data.is_moderated, $added);
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

    function commentSuccess($form, data)
    {
        // Clean form
        resetForm($form);

        // Show comment
        var had_preview = removePreview(data);
        var $new_comment = addComment(data);

        if( had_preview )
            // Avoid double jump when preview was removed. Instead refade to final comment.
            $new_comment.hide().fadeIn(600);
        else
            // Smooth introduction to the new comment.
            $new_comment.hide().show(600);

        return $new_comment;
    }

    function addComment(data)
    {
        // data contains the server-side response.
        var html = data['html'];
        var parent_id = data['parent_id'];
        var object_id = data['object_id'];

        var $new_comment;
        if(parent_id)
        {
            var $parentLi = $("#c" + parseInt(parent_id)).parent('li.comment-wrapper');
            var $commentUl = $parentLi.children('ul');
            if( $commentUl.length == 0 )
                $commentUl = $parentLi.append('<ul class="comment-list-wrapper"></ul>').children('ul.comment-list-wrapper');
            $commentUl.append('<li class="comment-wrapper">' + html + '</li>');
        }
        else
        {
            // Each top-level of django-threadedcomments starts in a new <ul>
            // when you use the comment.open / comment.close logic as prescribed.
            if(data['use_threadedcomments'])
                html = '<ul class="comment-list-wrapper"><li class="comment-wrapper">' + html + '</li></ul>';

            var $comments = getCommentsDiv(object_id);
            $comments.append(html).removeClass('empty');
        }

        return $("#c" + parseInt(data.comment_id));
    }

    function commentPreview(data)
    {
        var object_id = data['object_id'];
        var $comments = getCommentsDiv(object_id);

        var $previewarea = $comments.find(".comment-preview-area");
        if( $previewarea.length == 0 )
        {
            // If not explicitly added to the HTML, include a previewarea in the comments.
            // This should at least give the same markup.
            $comments.append('<div class="comment-preview-area"></div>').addClass('has-preview');
            $previewarea = $comments.children(".comment-preview-area");
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
        var form = $('form#comment-form-' + parseInt(data.object_id))[0];

        // Show mew errors
        for (var field_name in data.errors) {
            if(field_name) {
                var $field = $(form.elements[field_name]);

                // Twitter bootstrap style
                $field.after('<span class="js-errors">' + data.errors[field_name] + '</span>');
                $field.closest('.control-group').addClass('error');
            }
        }
    }

    function removeErrors($form)
    {
        $form.find('.js-errors').remove();
        $form.find('.control-group.error').removeClass('error');
    }

    function getCommentsDiv(object_id)
    {
        var selector = "#comments-" + parseInt(object_id);
        var $comments = $(selector);
        if( $comments.length == 0 )
            alert("Internal error - unable to display comment.\n\nreason: container " + selector + " is missing in the page.");
        return $comments;
    }

    function removePreview(data)
    {
        var object_id = data['object_id'];
        var $comments_list = $('#comments-' + object_id);
        
        var $previewarea = $comments_list.find(".comment-preview-area");
        var had_preview = $previewarea.hasClass('has-preview-loaded');

        if( previewAutoAdded )
            $previewarea.remove();  // make sure it's added at the end again later.
        else
            $previewarea.html('');

        // Update classes. allowing CSS to add/remove margins for example.
        $previewarea.removeClass('has-preview-loaded');
        $comments_list.removeClass('has-preview');

        return had_preview;
    }

    function removeWaitAnimation($form)
    {
        // Remove the wait animation and message
        $form.find('.comment-waiting').hide().stop();
    }

})(window.jQuery);
