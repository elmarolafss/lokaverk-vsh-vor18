import axios from 'axios'

const IS_PRODUCTION = process.env.NODE_ENV === 'production'
const API_URL = IS_PRODUCTION ? '/api/' : 'http://eaglemac.local:5000/api/'

let $axios = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {'Content-Type': 'application/json'}
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {

  fetchProducts (query) {
    let url = 'products'
    let first = true
    for (let qp in query) {
      if (query[qp] !== undefined && qp !== 'page') {
        if (first) {
          url += '?' + qp + '=' + query[qp] + '&'
          first = false
        }
        else { url += qp + '=' + query[qp] + '&' }
      }
    }
    if (url.slice(-1) === "&") {url = url.slice(0, -1)}
    return $axios.get(url)
      .then(response => response.data)
  },
  fetchProduct (pid) {
    let url = 'products/' + pid
    return $axios.get(url)
      .then(response => response.data)
  }
}
