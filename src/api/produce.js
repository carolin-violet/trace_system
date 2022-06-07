import request from '@/utils/request'

export function getProduceSummary(user_id) {
  return request({
    url: '/produce/' + user_id,
    method: 'get'
  })
}

export function getProduceDetail(data) {
  return request({
    url: '/produce/' + data.user_id + '/' + data.area_id + '/' + data.batch,
    method: 'get'
  })
}

export function addProduceInfo(data) {
  return request({
    url: '/produce',
    method: 'post',
    data
  })
}


export function getProduceTH(data) {
  return request({
    url: '/produce_th/' + data.user_id + '/' + data.area_id + '/' + data.batch,
    method: 'get',
    params: {
      time: data.time || ''
    }
  })
}

export function addProduceTH(data) {
  return request({
    url: '/produce_th',
    method: 'post',
    data
  })
}

