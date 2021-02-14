import requests
import json
from datetime import datetime
from dateutil import tz
from discord import Webhook, RequestsWebhookAdapter, Embed

# WEBHOOK_ID, WEBHOOK_TOKEN = '808112459016568842', 'siFMRiPRqO4c8voESKREzrz2NGQ_oQg5mNkxOyUO01eTtpp-80O3RSN_WOVXcWq2T1TU'
WEBHOOK_ID, WEBHOOK_TOKEN = '805813682357272656', 'M7sFh9S6Xzql1Ue1QLVw0olhMETU2j57NOfLfgDXgXaS0gVOMtvVdcI3cn1CnH5dC5Ol'

test_alerts_webhook = Webhook.partial(WEBHOOK_ID, WEBHOOK_TOKEN, adapter=RequestsWebhookAdapter())

with open('tradingoutput.json') as f:
  trading_data = json.load(f)

order_description = trading_data[5]['orderLegCollection'][0]['instrument']['description']
order_type = trading_data[5]['orderType']
price = trading_data[5]['price']
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
utc = datetime.strptime(trading_data[5]['closeTime'], '%Y-%m-%dT%H:%M:%S%z')
# utc.astimezone(to_zone)

instruction_dict = {
    'SELL_TO_CLOSE': 'STC',
    'BUY_TO_OPEN': 'BTO'
}

embed_dict = {
      "author": {
        "name": "RiskRebellion",
        "url": "https://www.reddit.com/r/cats/",
        "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
      },
      "title": f"{trading_data[5]['orderLegCollection'][0]['instrument']['description'].split(' ')[0]}"
               f"({trading_data[5]['orderLegCollection'][0]['positionEffect']})",
      "color": 15258703,
      "fields": [
          {
            "name": "Order Description",
            "value": f"**{instruction_dict[trading_data[5]['orderLegCollection'][0]['instruction']]}** "
                     f"{trading_data[5]['orderLegCollection'][0]['instrument']['description']}",
            "inline": True
          },
          {
              "name": "Order Type",
              "value": order_type,
              "inline": True
          },
          {
              "name": "Price",
              "value": "Yup",
              "inline": True
          },
          {
              "name": "Gain/Loss %",
              "value": "Yup",

          },
        # {
        #   "name": "Thanks!",
        #   "value": "You're welcome :wink:"
        # }
      ],
      "footer": {
        "text": f'Executed@{utc.astimezone(to_zone).strftime("%Y/%m/%d %H:%M:%S")}',
      }
}
embed = Embed.from_dict(embed_dict)

test_alerts_webhook.send(username='RiskRebellion Alerts',
                         avatar_url='https://islandmint.me/wp-content/uploads/2021/02/Rrebel.png',
                         embed=embed)
# test_alerts_webhook.send(username=None,
#                          content=f'order description {order_description}\norder type {order_type}\nprice {price}\nExecuted {utc.astimezone(to_zone).strftime("%Y/%m/%d %H:%M:%S")}')
