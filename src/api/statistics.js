import request from '@/utils/request'

export function personCount() {
  return request({
    url: '/statistics/personCount',
    method: 'get'
  })
}
