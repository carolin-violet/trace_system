import request from '@/utils/request'

export function getCommodities() {
  return request({
    url: '/commodities',
    method: 'get'
  })
}

export function addCommodity(data) {
  return request({
    url: '/commodity',
    method: 'post',
    data
  })
}

export function delCommodity(logistics_id) {
  return request({
    url: '/commodity/' + logistics_id,
    method: 'delete'
  })
}


