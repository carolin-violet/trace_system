"""
区块链类
"""

import datetime
import os
from src.models import Blockchain
from src.security import Hash


class Chain:
    def __init__(self, chain, db):
        self.chain = chain
        self.db = db

    '''
    创建初始区块
    '''
    def create_genesis_block(self):
        timestamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        info = {
            "logistics_id": '0',
            "pre_hash": '0',
            "timestamp": timestamp,
            "nonce": 0,
            "data": '',
        }
        cur_hash = Hash.get_hash(info)
        genesis_block = Blockchain('0', cur_hash, '0', timestamp, 0, '')
        self.db.session.add(genesis_block)
        self.db.session.commit()

    '''
    增加新区块,
    data为加密后的data
    '''
    def new_block(self, logistics_id, data):
        pre_hash = self.last_block.cur_hash
        timestamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        pre_nonce = self.last_block.nonce
        nonce = self.proof_of_work(pre_nonce)
        data_path = self.store_cipher(logistics_id, data)

        info = {
            "logistics_id": logistics_id,
            "pre_hash": pre_hash,
            "timestamp": timestamp,
            "nonce": nonce,
            "data": data_path,
        }
        cur_hash = Hash.get_hash(info)
        block = Blockchain(logistics_id, cur_hash, pre_hash, timestamp, nonce, data_path)
        self.db.session.add(block)
        self.db.session.commit()

    '''
    存储密文，返回文件路径
    '''

    @staticmethod
    def store_cipher(logistics_id, data):
        data_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/data/' + logistics_id + '.txt'
        with open(data_path, 'wb') as fp:
            if type(data) == list:
                for item in data:
                    fp.write(item)
            elif type(data) == bytes:
                fp.write(data)
        return data_path

    '''
    工作量证明求解
    '''
    def proof_of_work(self, pre_nonce):
        cur_nonce = 0
        while not self.validate_proof(pre_nonce, cur_nonce):
            cur_nonce += 1
        return cur_nonce

    '''
    验证nonce
    '''
    @staticmethod
    def validate_proof(pre_nonce, cur_nonce):
        data = str(pre_nonce)+str(cur_nonce)
        return Hash.get_hash(data).startswith('0')

    '''
    验证区块链有效性：分别验证前一个区块的计算的hash与当前区块中上一个区块的hash是否一样，相邻区块的nonce进行工作量证明验证
    '''
    def validate_chain(self):
        pre_block = self.chain[0]
        cur_index = 1

        while cur_index < len(self.chain):
            # 重新计算前一个区块的哈希值并与后一个区块中记载的上一个区块的哈希值比对
            pre_info = {
                "logistics_id": pre_block.logistics_id,
                "pre_hash": pre_block.pre_hash,
                "timestamp": pre_block.timestamp,
                "nonce": pre_block.nonce,
                "data": pre_block.data_path,
            }
            pre_hash = Hash.get_hash(pre_info)
            if pre_hash != self.chain[cur_index].pre_hash:
                return cur_index + 1

            if not self.validate_proof(pre_block.nonce, self.chain[cur_index].nonce):
                return cur_index + 1

            pre_block = self.chain[cur_index]
            cur_index += 1
        return 'true'

    '''
    返回最后一个区块
    '''
    @property
    def last_block(self):
        if len(self.chain) > 1:
            return self.chain[-1]
        elif len(self.chain) == 1:
            return self.chain[0]


