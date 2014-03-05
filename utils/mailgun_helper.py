from python_mailgun.client import Client


def send_password_reset(client, sender, to, link):
    """

    @param client:
    @type client: Client
    @param sender:
    @param to:
    @param link:
    """
    return client.send_mail(sender, to, 'password reset', link)