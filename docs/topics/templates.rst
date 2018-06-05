Using custom comment templates
==============================

Besides the standard templates of django-comments_, this package provides
a ``comments/comment.html`` template to render a single comment.

It's default looks like:

.. code-block:: html+django

      {% load i18n %}
      <div{% if preview %} id="comment-preview"{% else %} id="c{{ comment.id }}"{% endif %} class="comment-item">
       {% block comment_item %}
         {% if preview %}<h3>{% trans "Preview of your comment" %}</h3>{% endif %}
           <h4>
             {% block comment_title %}
               {% if comment.url %}<a href="{{ comment.url }}" rel="nofollow">{% endif %}
               {% if comment.name %}{{ comment.name }}{% else %}{% trans "Anonymous" %}{% endif %}{% comment %}
               {% endcomment %}{% if comment.url %}</a>{% endif %}
               <span class="comment-date">{% blocktrans with submit_date=comment.submit_date %}on {{ submit_date }}{% endblocktrans %}</span>
               {% if not comment.is_public %}<span class="comment-moderated-flag">({% trans "moderated" %})</span>{% endif %}
               {% if USE_THREADEDCOMMENTS and not preview %}<a href="#c{{ comment.id }}" data-comment-id="{{ comment.id }}" class="comment-reply-link">{% trans "reply" %}</a>{% endif %}
             {% endblock %}
           </h4>

           <div class="comment-text">{{ comment.comment|linebreaks }}</div>
       {% endblock %}
      </div>

.. note::

   The ``id="comment-preview"``, ``data-comment-id`` fields are required for proper JavaScript actions.
   The div id should be ``id="c{{ comment.id }}"``, because ``Comment.get_absolute_url()`` points to it.

Adding a Bootstrap 4 layout, including Gravatar_ would look like:

.. code-block:: html+django

    {% load i18n gravatar %}

    <div id="{% if preview %}comment-preview{% else %}c{{ comment.id }}{% endif %}" class="comment-item{% if comment.user_id and comment.user_id == comment.content_object.author_id %} by-author{% endif %}">
      {% if preview %}<h3>{% trans "Preview of your comment" %}</h3>{% endif %}
      <div class="media">
        {% gravatar comment.email css_class='user-image' %}
        <div class="media-body">
          <h4>
            {% block comment_title %}
              {% if comment.url %}<a href="{{ comment.url }}" rel="nofollow">{% endif %}
              {% if comment.name %}{{ comment.name }}{% else %}{% trans "Anonymous" %}{% endif %}{% comment %}
              {% endcomment %}{% if comment.url %}</a>{% endif %}
              {% if not comment.is_public %}<span class="comment-moderated-flag">({% trans "moderated" %})</span>{% endif %}
              {% if comment.user_id and comment.user_id == comment.content_object.author_id %}<span class="comment-author-flag">[{% trans "author" %}]</span>{% endif %}
            {% endblock %}
          </h4>

          <div class="comment-text">{{ comment.comment|linebreaks }}</div>
          <div class="comment-tools">
            {% if USE_THREADEDCOMMENTS and not preview %}<a href="#c{{ comment.id }}" data-comment-id="{{ comment.id }}" class="comment-reply-link">{% trans "reply" %}</a>{% endif %}
            <span class="comment-date">{{ comment.submit_date }}</span>
          </div>
        </div>
      </div>
    </div>

.. warning::

    While extremely popular, Gravatar_ is a huge privacy risk,
    as it acts like a tracking-pixel for all your users.
    It also exposes email addresses as the MD5 hashes can be reverse engineerd.
    See the :doc:`GDPR <gdpr>` notes for more information.

Customize date time formatting
------------------------------

To override the displayed date format, the template doesn't have to be overwritten.
Instead, define ``DATETIME_FORMAT`` in a locale file. Define the following setting:

.. code-block:: python

    FORMAT_MODULE_PATH = 'settings.locale'

Then create :samp:`settings/locale/{XY}/formats.py` with:

.. code-block:: python

    DATETIME_FORMAT = '...'

This should give you consistent dates across all views.


.. _django-comments: https://github.com/django/django-contrib-comments
.. _Gravatar: https://gravatar.com
