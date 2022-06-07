import request from '@/utils/request'

export function getBlocks(user_type) {
  return request({
    url: '/blockchain',
    method: 'get'
  })
}

export function getOutBlocks(user_type) {
  return request({
    url: '/blockchain/out-chain',
    method: 'get'
  })
}

export function verifyChain(user_type) {
  return request({
    url: '/blockchain/validate_proof',
    method: 'get'
  })
}

export function addBlock(data) {
  return request({
    url: '/blockchain',
    method: 'post',
    data
  })
}
