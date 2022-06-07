import request from '@/utils/request'

export function getLogistics(logistics_id) {
  return request({
    url: '/logistics/' + logistics_id,
    method: 'get'
  })
}

export function addLogistics(data) {
  return request({
    url: '/logistics',
    method: 'post',
    data
  })
}

export function delLogistics(logistics_id) {
  return request({
    url: '/logistics/' + logistics_id,
    method: 'delete'
  })
}


