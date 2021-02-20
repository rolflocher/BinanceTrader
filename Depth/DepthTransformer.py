
import json

class DepthTransformer:
    
    def transform(self, diffs, seed):
        diffDtos = []
        for diff in diffs:
            diffDto = {
                'time': diff[0],
                'firstId': diff[1],
                'lastId': diff[2],
                'bids': json.loads(diff[3]),
                'asks': json.loads(diff[4])
            }
            diffDtos.append(diffDto)
        seedDto = {
            'lastId': seed[0],
            'bids': json.loads(seed[1]),
            'asks': json.loads(seed[2])
        }
        return diffDtos, seedDto
