from flask_restful import Resource, reqparse
import blockChain
from flask import jsonify


class AddBlock(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('file_name', type=str)
            parser.add_argument('file_size', type=str)
            parser.add_argument('file_type', type=str)
            parser.add_argument('file_hash', type=str)
            parser.add_argument('creator', type=str)
            parser.add_argument('type', type=str)
            parser.add_argument('salt', type=str)
            parser.add_argument('nonce', type=str)
            parser.add_argument('tag', type=str)

            arg = parser.parse_args()

            block = {
                'data': {
                    'name': arg['file_name'],
                    'size': arg['file_size'],
                    'file_type': arg['file_type'],
                    'file_hash': arg['file_hash'],
                    'salt': arg['salt'],
                    'nonce': arg['nonce'],
                    'tag': arg['tag'],
                },
                'creator': arg['creator'],
                'block_type': arg['type'],
            }

            if len(block['data']['file_hash']) < 1:
                return {'error': 'hash not valid',
                        }
            foo = blockChain.write_block(block, False)
            return {'status': True,
                    'index': foo['index']
                    }

        except Exception as e:
            return {'error': str(e),
                    }


class FetchBlock(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('index', type=str)
            arg = parser.parse_args()
            index = arg['index']

            block = blockChain.read_block(index)
            return jsonify(block)

        except Exception as e:
            return {'error': str(e),
                    }
