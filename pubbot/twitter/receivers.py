
from constance import config

from pubbot.dispatch import receiver
from pubbot.conversation import say
from pubbot.twitter.signals import tweet


@receiver(tweet)
def broadcast_tweet(sender, text, user, id_str, **kwargs):
    if config.TWITTER_BROADCAST_FOLLOW:
        if user['screen_name'].lower() not in config.TWITTER_BROADCAST_FOLLOW.lower().split(","):
            return

    say(
        content="\n".join([
            "https://twitter.com/%s/status/%s" % (user['screen_name'], id_str),
            "[ %s: %s ]" % (user['screen_name'], text.replace("\n", ""))
        ]),
        tags=['twitter_stream'],
    )
