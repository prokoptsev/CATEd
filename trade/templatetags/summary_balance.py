from django import template
from trade.models import UserWallet, UserExchanges
import requests

register = template.Library()


@register.inclusion_tag('trade/user_summaries.html')
def get_user_summaries(user):
    btc_total = float(0)
    usd_total = float(0)
    wallets = UserWallet.objects.filter(user=user)
    exchanges = UserExchanges.objects.filter(user=user)
    if wallets is not None:
        for wallet in wallets:
            usd_total += float(wallet.total_usd)
    if exchanges is not None:
        for exchange in exchanges:
            usd_total += float(exchange.total_usd)
    if usd_total > 0:
        btc_price = requests.get('https://api.cryptonator.com/api/full/btc-usd').json()
        btc_total = usd_total / float(btc_price['ticker']['price'])
    return {'btc': btc_total,
            'usd': usd_total}

