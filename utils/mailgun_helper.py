from python_mailgun.client import Client

def send_password_reset(client, sender, to, text, html):
    """


    @param client:
    @type client: Client
    @param sender:
    @param to:
    @param text:
    @param html:
    """
    return client.send_mail(sender, to, 'password reset', text, html=html)