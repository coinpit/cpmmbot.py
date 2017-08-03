class Account(object):
    def __init__(self, apikey):
        assert (apikey is not None), 'usage: Account(apikey)'
        assert (apikey["name"] is not None), "name is missing in apikey provided."
        assert (apikey["apiPublicKey"] is not None), "apiPublicKey is missing in apikey provided."
        assert (apikey["userid"] is not None), "userid is missing in apikey provided."
        assert (apikey["secretKey"] is not None), "secretKey is missing in apikey provided."
        assert (apikey["serverAddress"] is not None), "serverAddress is missing in apikey provided."
        assert (apikey["accountid"] is not None), "accountid is missing in apikey provided."
        assert (apikey["publicKey"] is not None), "publicKey is missing in apikey provided."
        self.apikey = apikey
        self.name = apikey["name"]
        self.role = apikey["role"]
        self.apiPublicKey = apikey["apiPublicKey"]
        self.userid = apikey["userid"]
        self.secretKey = apikey["secretKey"]
        self.authorization = apikey["authorization"]
        self.serverAddress = apikey["serverAddress"]
        self.accountid = apikey["accountid"]
        self.publicKey = apikey["publicKey"]
