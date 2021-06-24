A desklet to get cryptocurrency coin prices from binance written with python-gtk3

    simple installation
    get price every min (1, 5, 10, 30, 60)
    support http proxy

![Image of Binance Desklet](https://github.com/mmtaee/binance-desklet/blob/master/sample.jpg)

Installation :
    
    - clone the repo
    - chmod +x install.sh
    - ./install.sh
    - reboot


if you want add newcoin to list :

    # nano /usr/bin/bianance_desklets/binance.py    
    append to 'COINS' dictionary 
    example : 
        COINS = [
            'BTC/USDT',
            'ETH/USDT',
            'TRX/USDT',
            'XMR/USDT',
        ]
    to see Monero price.
