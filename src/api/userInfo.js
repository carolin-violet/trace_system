import request from '@/utils/request'

export function getUsers(user_type) {
  return request({
    url: '/users/' + user_type,
    method: 'get'
  })
}

export function addUser(data) {
  return request({
    url: '/users',
    method: 'post',
    data
  })
}

export function modifyUser(data) {
  return request({
    url: '/users/info/' + data.user_id,
    method: 'patch',
    data
  })
}

export function delUser(user_id) {
  return request({
    url: '/users/' + user_id,
    method: 'delete'
  })
}
