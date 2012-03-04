/*
  Based on django-ajaxcomments, BSD licensed.
  Copyright (c) 2009 Brandon Konkle and individual contributors.

  Updated to be more generic, more fancy, and usable with different templates.
 */

var ajaxComment = (function()
{
    var commentBusy = false;

    function ajaxComment(args)
    {
        var media = args.media;
        var oncomplete = args.complete;

        $('div.comment-error').remove();
        if (commentBusy) {
            return false;
        }

        commentBusy = true;
        var comment = $('div.comment-form form').serialize();
        var url = $('div.comment-form form').attr('action');

        // Add a wait animation
        $('#comment-waiting').fadeIn(1000);

        // Use AJAX to post the comment.
        $.ajax({
            type: 'POST',
            url: url + 'ajax/',
            data: comment,
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

                $('div.comment-form form').unbind('submit');
                $('div.comment-form form').submit();
            },
            dataType: 'json'
        });

        return false;
    }

    function commentSuccess(data)
    {
        $('div.comment-form form textarea')[0].value = "";
        $('#id_comment').val('');
        $('#comments').append(data['html']);
        $('div.comment:last').show('slow');
        $('#comment-thanks').show().fadeOut(4000);
    }

    function commentFailure(data)
    {
        $('div.comment-form ul.errorlist').each(function() {
          this.parentNode.removeChild(this);
        });

        for (var error in data.errors) {
            $('#id_' + error).parent().before(data.errors[error])
        }
    }

    function removeWaitAnimation()
    {
        // Remove the wait animation and message
        $('.ajax-loader').remove();
        $('div.comment-waiting').stop().remove();
    }

    return ajaxComment;
})();