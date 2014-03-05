"""
This module contains a set functions to automatize mailguns calls
"""

from python_mailgun.client import Client


def send_password_reset(client, sender, to, text, html):
    """ Sends a password reset mail


    @param client: the mailgun client to use
    @type client: Client
    @param sender: sender's address
    @param to: recipient's address
    @param text: the text body
    @param html: the html body
    """
    return client.send_mail(sender, to, 'password reset', text, html=html)