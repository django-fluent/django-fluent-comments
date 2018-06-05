Privacy concerns (GDPR)
=======================

Comment support needs to consider the General Data Protection Regulation (GDPR)
when when you serve European customers. Any personal data (email address, IP-address)
should only be stored as long as this is truely needed, and it must be clear whom it's shared with.

.. tip::

    For a simple introduction, see https://premium.wpmudev.org/blog/gdpr-compliance/

The Django comments model also stores the email address and IP-address of the commenter,
which counts as personal information a user should give consent for. Consider running
a background task that removes the IP-address or email address after a certain period.

Concerns for third-party services
---------------------------------

When using :doc:`Akismet <akismet>`, the comment data and IP-address is passed to the servers of Akismet_.

In case you update templates to display user avatars using Gravatar_, this this also
provides privacy-sensitive information to a third party. Gravatar acts like a tracking-pixel,
noticing every place you visit. It also makes your user's email address public.
While the URL field is encoded as MD5, Gravatar doesn't use salted hashes so the
data can be easily reverse engineered back to real user accounts.

.. seealso::

    For more information, read:

    * https://meta.stackexchange.com/questions/21117/is-using-gravatar-a-security-risk
    * https://webapps.stackexchange.com/questions/9973/is-it-safe-to-use-gravatar/30605#30605
    * http://onemansblog.com/2007/02/02/protect-your-privacy-delete-internet-usage-tracks/comment-page-1/#comment-46204
    * https://www.wordfence.com/blog/2016/12/gravatar-advisory-protect-email-address-identity/

.. _Akismet: https://akismet.com
.. _Gravatar: https://gravatar.com
