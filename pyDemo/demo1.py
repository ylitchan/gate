import requests


data={
  "operationName": "Search",
  "variables": {
    "limit": 10,
    "lowVolumeFilter": True,
    "networkFilter": [
      1,
      56,
      43114,
      250,
      137,
      1666600000,
      42161,
      10,
      7700,
      25,
      42220,
      1313161554,
      42170,
      1284,
      1285,
      9001,
      128,
      1088,
      100,
      592,
      42262,
      53935,
      288,
      4689,
      66,
      888,
      321,
      106,
      10000,
      24,
      122,
      20,
      2001,
      1030,
      3000,
      333999,
      55,
      70,
      57,
      8217,
      336,
      40,
      246,
      820
    ],
    "resolution": "1D",
    "search": "sliz"
  },
  "query": "query Search($search: String!, $networkFilter: [Int!], $lowVolumeFilter: Boolean, $resolution: String, $limit: Int) {\n  search(\n    search: $search\n    networkFilter: $networkFilter\n    lowVolumeFilter: $lowVolumeFilter\n    resolution: $resolution\n    limit: $limit\n  ) {\n    hasMore\n    hasMoreLowVolume\n    tokens {\n      ...BaseTokenWithMetadata\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BaseTokenWithMetadata on TokenWithMetadata {\n  address\n  decimals\n  id\n  liquidity\n  name\n  networkId\n  price\n  priceChange\n  priceChange24\n  priceChange12\n  priceChange4\n  priceChange1\n  resolution\n  symbol\n  volume\n  topPairId\n  exchanges {\n    ...ExchangeModel\n    __typename\n  }\n  __typename\n}\n\nfragment ExchangeModel on Exchange {\n  address\n  color\n  exchangeVersion\n  id\n  name\n  networkId\n  tradeUrl\n  iconUrl\n  enabled\n  __typename\n}\n"
}
headers={'x-api-key':'da2-vkmqkh3wlngdfktfeybq6j44li'}
a=requests.post('https://i3zwhsu375dqllo5srv5vn35ba.appsync-api.us-west-2.amazonaws.com/graphql',json=data,headers=headers)
data=a.json()['data']['search']['tokens'][0]
print(data['symbol'],data['address'],data['name'],data['price'],data['priceChange']*100)