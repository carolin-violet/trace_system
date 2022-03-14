"""
区块链类
"""

import datetime
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
        genesis_data = ''

        cur_hash = Hash.get_hash(genesis_data)
        genesis_block = Blockchain(cur_hash, '0', timestamp, 0, genesis_data)
        self.db.session.add(genesis_block)
        self.db.session.commit()

    '''
    增加新区块,
    data为加密后的data
    '''
    def new_block(self, data):
        pre_hash = self.last_block.cur_hash
        timestamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        pre_nonce = self.last_block.nonce
        nonce = self.proof_of_work(pre_nonce)

        info = {
            "pre_hash": pre_hash,
            "timestamp": timestamp,
            "nonce": nonce,
            "data": data,
        }
        cur_hash = Hash.get_hash(info)

        block = Blockchain(cur_hash, pre_hash, timestamp, nonce, data)
        self.db.session.add(block)
        self.db.session.commit()

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
        return sha256(data.encode()).hexdigest().startswith('0')


    '''
    验证区块链有效性
    '''
    @property
    def validate_chain(self):
        pre_block = self.blocks[0]
        cur_index = 1

        while cur_index < len(self.blocks):
            # 重新计算前一个区块的哈希值并与后一个区块中记载的上一个区块的哈希值比对
            pre_hash = self.hash(pre_block.index, pre_block.commodity_id, pre_block.data, pre_block.pre_hash, pre_block.nonce, pre_block.timestamp)
            if pre_hash != self.blocks[cur_index].pre_hash:
                return False

            pre_block = self.blocks[cur_index]
            cur_index += 1
        return True

    '''
    返回最后一个区块
    '''
    @property
    def last_block(self):
        if len(self.chain) > 1:
            return self.chain[-1]
        elif len(self.chain) == 1:
            return self.chain[0]




