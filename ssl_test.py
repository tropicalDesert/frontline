import express

def test(req,res):
    return 'testing'

express.get(test)
credentials={
    'keyfile':'./ssl/key.pem',
    'certfile':'./ssl/cert.pem'
}
express.serve('127.0.0.1',3000,https=credentials)
