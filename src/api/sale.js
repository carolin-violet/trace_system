import request from '@/utils/request'

export function getCommodities(user_id) {
  return request({
    url: '/commodities/' + user_id,
    method: 'get'
  })
}

export function getImg(logistics_id) {
  return request({
    url: '/commodity/qrcode_img/' + logistics_id,
    method: 'get',
    responseType: 'blob'
  })
}
