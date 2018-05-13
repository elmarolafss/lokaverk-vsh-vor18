// Vue.js Filters
// https://vuejs.org/v2/guide/filters.html

import Vue from 'vue'

let filters = {

  formatTimestamp (timestamp) {
    let datetime = new Date(timestamp)
    return datetime.toLocaleTimeString('en-US')
  },
  sortAsc (arr) {
  	return arr.sort((p1, p2) => {return p1.price - p2.price})
  },
  sortDes (arr) {
  	return arr.sort((p1, p2) => {return p2.price - p1.price})
  }
}

// Register All Filters on import
Object.keys(filters).forEach(function (filterName) {
  Vue.filter(filterName, filters[filterName])
})
