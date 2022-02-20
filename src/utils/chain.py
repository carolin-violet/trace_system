from src.models import Blockchain
import datetime
import json
from hashlib import sha256


class Chain:
    def __init__(self, commodity_id):
        self.commodity_id = commodity_id
        self.blocks = Blockchain.query.filter(Blockchain.commodity_id == self.commodity_id).all()

    '''
    创建初始区块
    '''
    def create_genesis_block(self, db):
        time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        cur_hash = self.hash(0, self.commodity_id, '', 1, 0, time_stamp)
        genesis_block = Blockchain(0, self.commodity_id, '', 1, cur_hash, 0, time_stamp)
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
        return sha256(str(pre_nonce)+str(cur_nonce)).hexdigest().startswith('0')

    '''
    将物流信息转换为字符串
    '''
    @staticmethod
    def new_logistics(commodity_id, status, com, time, ini, dec, cur, person, tel):
        data = '单号:' + commodity_id + '商品状态:' + status + '\n公司名称:' + com \
            + '\n操作时间:' + time + '\n初始地:' + ini + '\n目的地:' + dec \
            + '\n当前所在地:' + cur + '\n操作人:' + person + '\n联系方式:' + tel + '\n'
        return data

    '''
    增加新区块
    '''
    def add_block(self, db, commodity_id, status, com, time, ini, dec, cur, person, tel):
        time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        index = self.last_block.index + 1
        pre_hash = self.last_block.cur_hash
        data = self.new_logistics(commodity_id, status, com, time, ini, dec, cur, person, tel)
        nonce = self.proof_of_work(self.last_block.nonce)
        cur_hash = self.hash(index, self.commodity_id, data, pre_hash, nonce, time_stamp)
        block = Blockchain(index, self.commodity_id, data, pre_hash, cur_hash, nonce, time_stamp)
        db.session.add(block)
        db.session.commit()

    '''
    验证区块链有效性
    '''
    def validate_chain(self):
        pre_block = self.blocks[0]
        cur_index = 1

        while cur_index < len(self.blocks):
            # 验证哈希值是否正确
            if pre_block['cur_hash'] != self.blocks[cur_index]['pre_hash']:
                return False

            pre_block = self.blocks[cur_index]
            cur_index += 1
        return True

    '''
    返回最后一个区块
    '''
    @property
    def last_block(self):
        return self.blocks[-1]




