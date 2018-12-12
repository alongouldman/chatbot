# import json
# import pickle
#
# keyfile_dict = {
#         'type': 'service_account',
#         'client_email': "freedom-bot@freedom-bot-1.iam.gserviceaccount.com",
#         # 'client_email': os.environ['BOT_GOOGLEAPI_CLIENT_EMAIL'],
#         'private_key': "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDGYHs0hs17PUhH\nm0gHAGjqUFL4Hum/bdSTTIFOvZFp6VMHGNBf7kVpMKewBM2JcIFEK/4oKnNGsYAy\nR5mIDwSuPRS2DD6iPTExsjUw7+Gfyyn0aKXzrA+jclcfPVDUzAhiMAFz1Z4qwjcy\nUEeCtEGaXrpky0evvF2TJE4kCfcQrdjVc7sGwrAEOmoFckZ0pZOu123th2p7SMKq\nfQWSvDRno8ADJa+JQOxcTKX/RACzHFxPm9TT7ZF3eCqhUiAI5Yz/XbtUUYwTt1SQ\nsP+EV3R3KFpEYCueZ0XSqYJLG47WIaPqqIkS61ACafhoWqqqMysa00p2zBeEp7x+\nUvJroXGRAgMBAAECggEAAb4yJOzwiB46qOjnDAszkMf4A6azYW+ByjHGUtKY8QoY\nFPhRh98+QEFpfsMbCnOo6hg8G16cnMzVUlPFWEAAB7chDAStZfPlT1FIVPvNkt+o\nSKXE/AApcsNf2zYY5Ea+5dxzvdCdGzVxwlUY3L/QUf62MumjkYplVNQxRNEq2NxX\nM4PMCh03jlRwODfDdweNFXmf7PGn2LgKUAel+RRpTvfMt8CDKwjGZJQGmwLHCNFv\nkZvQGUr9OgYAJwpm4sypwyASPi5vySPEwmGCrs1JqkO6BpR1+4f5255+7BMxMlUF\n8dcDAMG26yp1fxA90Fa8sBb9vXs3SOOHVhOot6pxgQKBgQDuoMuRFC9jZkpa8lYQ\nS4B8BRLW0y90y3Kr/QpmQ8egZK2NXON4z4E2RlID736/c36fXEczTNZa4TiGMdlp\njAh6I373mPMue5NnFVk12x2RzX9gqHvT2Fep1Rul26aTE97rLNVMMxmfl0r6/jKX\njgUcwuNJJQDpwicJAQ1u+7n/gQKBgQDU0YrE3u1dNm8wfQNmaET4Fe7CXT72GpaG\nrsyC64es/XCLRDUwgiUcKBOddeIwSKj8iOdymrJk2KtSR31p5q6H9pd+kb9bMs4x\n05XHk7txNrLSSxDptq99DJim29SPfZXDuPtZNWq+jz4mciMENVwke7PzN0321ZBp\naxneUoR6EQKBgQDVLEvudOvIjm7KREbiE7DaGeY0h0CTw9PTFSAfL1m8TXRFHsAP\nAsBZbgSCg4blHRX24wawK2oqkZxfNVUV1wUTp3YbVkWYNsj9g7LIS9BkmgG6pYjJ\nPTFDBJ/IUSrDpTK1QL3jbprrWMqg4kjr3vFuOiO1ChuAt/MLNid8B+CnAQKBgCKm\nEv/Gg8K/UA8G63zK0R/LAlpmsA+FeKho4ScXjblecepaqoZBSiVxaPAj9zWBPvIO\noBAKm6zLkekNdp+9TQEZ5sRWml8QwH1gQ2yA4u2lyCtwyUoj0iJ74IaaF9tcyPta\nrKFzjvODgszjnEvdHClcconQoULktmRTaZzGtobhAoGBANwvlEr0PPCJdZFcX0I/\nuurXbIk9JRJK+4QZDEu0ARiCFa38OiAzZxs8R89DG4DPNs53JniyaUKGmoTVGTH3\nxCewLOGVcwRztWeINR4jCHvSmMRk7tVYjdTeBLd4HbAebAgOwc9+BtzDvAayMHeJ\nuBsEhe7Rptlp4RDeJvNgek3+\n-----END PRIVATE KEY-----\n",
#         'private_key_id': "134f1354e8ae832c3fd60005448e0e42cc5f4ad2",
#         'client_id': "101731452250466063757"
#         # 'token_uri': "https://oauth2.googleapis.com/token"
#     }
#
# input = json.dumps(keyfile_dict)
# with open('environ_secret.txt', 'w') as file:
#     file.write(input)
#
# output = json.loads(input)
# print(type(output))


from utils import *


def remove_money_words(words):
    money_words = get_money_words()
    print(money_words)
    return [item for item in words if item not in money_words]



s = '30 שקל צדקה שקל צדקה מרמי ש"ח לוי!!!! שכוייח'

words = s.split(' ')
print(remove_money_words(words))
