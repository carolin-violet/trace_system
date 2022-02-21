from src.models import Blockchain
import datetime
import json
from hashlib import sha256


class Chain:
    def __init__(self, commodity_id, blocks):
        self.commodity_id = commodity_id
        self.blocks = blocks

    '''
    创建初始区块
    '''
    def create_genesis_block(self, db):
        time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        cur_hash = self.hash(0, self.commodity_id, 'genesis_block', '1', 0, time_stamp)
        genesis_block = Blockchain(0, self.commodity_id, 'genesis_block', '1', cur_hash, 0, time_stamp)
        db.session.add(genesis_block)
        db.session.commit()

    '''
    求一个区块信息的哈希值
    '''
    @staticmethod
    def hash(index, commodity_id, data, pre_hash, nonce, timestamp):
        data = {
            "index": index,
            "commodity_id": commodity_id,
            "data": data,
            "pre_hash": pre_hash,
            "nonce": nonce,
            "timestamp": timestamp,
        }
        block_string = json.dumps(data, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

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
    将物流信息转换为字符串
    '''
    @staticmethod
    def new_logistics(commodity_id, status, com, time, ini, des, cur, person, tel):
        data = {
            "commodity_id": commodity_id,
            "status": status,
            "com": com,
            "time": time,
            "ini": ini,
            "des": des,
            "cur": cur,
            "person": person,
            "tel": tel,
        }
        return json.dumps(data, sort_keys=True)

    '''
    增加新区块
    '''
    def add_block(self, db, commodity_id, status, com, time, ini, dec, cur, person, tel):
        time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        index = self.last_block.index + 1
        pre_hash = self.last_block.cur_hash
        data = self.new_logistics(commodity_id, status, com, time, ini, dec, cur, person, tel)
        nonce = self.proof_of_work(self.last_block.nonce)
        cur_hash = self.hash(index, commodity_id, data, pre_hash, nonce, time_stamp)
        block = Blockchain(index, commodity_id, data, pre_hash, cur_hash, nonce, time_stamp)
        db.session.add(block)
        db.session.commit()

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
        if len(self.blocks) > 1:
            return self.blocks[-1]
        elif len(self.blocks) == 1:
            return self.blocks[0]




