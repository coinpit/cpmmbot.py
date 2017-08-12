# Coinpit Market Maker Bot

This is sample market maker bot written for Coinpit with hedging.Feel free to modify it as per your need.

Download and install market maker bot

````bash
$> git clone https://github.com/coinpit/cpmmbot.py
$> cd cpmmbot.py
$> python setup.py install
````

settings.py file is generaged. please modify it as per bot requirement.

create a json file which stores bitmex apikey and secret.

example:

````json
{
    "ID": "Ag-_DuBvWrO8IK-6FnGhldzR",
    "Secret": "_Dss0iITNH5-4QlCNYxqXQ7kA2ngSmhKX4tlRBdn4mmsR3_A"
}
````


Getting help:

````bash
$> ./mmbot.py -h
usage: mmbot.py [-h] --bitmex BITMEX_APIKEY_FILE --coinpit COINPIT_APIKEY_FILE
                [--bh BITMEX_HOST] [--ch COINPIT_HOST]

Market maker bot for Coinpit with hedging supported at Bitmex

required:
    --bitmex BITMEX_APIKEY_FILE, -b BITMEX_APIKEY_FILE
                        Bitmex API KEY json file. example content: { "ID":
                        "Ag-_DuBvWrO8IK-6FnGhldzR", "Secret":
                        "_Dss0iITNH5-4QlCNYxqXQ7kA2ngSmhKX4tlRBdn4mmsR3_A" }
    --coinpit COINPIT_APIKEY_FILE, -c COINPIT_APIKEY_FILE
                        api-key downloaded from coinpit. provide path.

optional arguments:
    -h, --help            show this help message and exit

    --bh BITMEX_HOST      bitmex host. ex. https://live.coinpit.io/api/v1
    --ch COINPIT_HOST     coinpit host. ex. https://www.bitmex.com/api/v1/

````

Starting bot

````bash

$> ./mmbot.py -c <coinpit api-key file location> -b<bitmex api-key file location>

````
