from src.models import Commodity, Logistics, Blockchain
import datetime
time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())


class Block:
    def __init__(self, product_id):
        self.product_id = product_id
        com = Commodity.query.filter(Commodity.product_id == self.product_id).first
        self.name = com.name
        logistics = Logistics.query.filter(Logistics.product_id == self.product_id).all()[-1]
        self.data = '单号:' + logistics.product_id + '商品状态:' + logistics.status + '\n公司名称:' + logistics.com \
            + '\n操作时间:' + logistics.time + '\n初始地:' + logistics.ini + '\n目的地:' + logistics.dec \
            + '\n当前所在地:' + logistics.cur + '\n操作人:' + logistics.person + '\n联系方式:' + logistics.tel + '\n'

    def compute_hash(self):
        pass


class Chain:
    def __init__(self, commodity_id):
        pass

    def create_genesis_block(self):
        pass

    def proof_of_work(self):
        pass

    def add_block(self):
        pass

    def last_block(self):
        pass




