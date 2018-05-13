<template>
  <main class="main-grid-item">
  <div class="cf h-100 search-main-grid">
    <div class="search-filter db h-100 br b--black">
      <div class="fixed w5 tc mt6">
        <router-link
        :to="{ path: $route.fullPath, query: { sort: 'hilo' } }"
        class="dib link ui black pb2 bb">
          Highest - Lowest
        </router-link>
        <router-link
        :to="{ path: $route.fullPath, query: { sort: 'lohi' } }"
        class="dib link ui black pt2">
          Lowest - Highest
        </router-link>
      </div>
    </div>
    <div class="subheadline pa4 search-grid" v-if="loading">
      Loading...
    </div>
    <div class="pt3 ph3 search-grid" v-else>
      <div class="subheadline" v-if="empty">
        sorry, i got nothing...
      </div>
      <div v-for="product in chunkedProds" v-else>
        <ProductThumb class="tc" :prod="product"></ProductThumb>
      </div>
    </div>
    <div v-if="error" class="subheadline pa4">{{ errorMessage }}</div>
    <div class="search-pages h-100 pa3 dt">
      <div class="dtc v-mid center tc">
        <router-link
        v-for="i in howManyChunks"
        :to="{ path: $route.fullPath, query: { page: i } }"
        class="link black pa2 bt bb b--black hover-bg-red hover-white">
          {{ i }}
        </router-link>
      </div>
    </div>
  </div>
  </main>
</template>

<script>
import ProductThumb from '@/components/ProductThumb.vue'
import $backend from '../backend'

export default {
  name: 'search',
  components: {
    ProductThumb
  },
  data () {
    return {
      prods: [],
      cToHex: {},
      loading: false,
      error: false,
      errorMessage: "",
      colFilter: false,
      saveColors: []
    }
  },
  methods: {
    fetchProducts () {
      this.loading = true
      $backend.fetchProducts(this.$route.query)
        .then(responseData => {
          this.prods = responseData
          this.loading = false
        }).catch(error => {
          this.error = true
          this.errorMessage = error.message
        })
    },
    updateAll () {
      this.prods = {}
      this.error = false
      this.errorMessage = ""
      this.query = this.$route.query
      this.fetchProducts()
    },
    pageIndex () {
      if (this.query.page) {
        return this.query.page - 1
      } else {
        return 0
      }
    }
  },
  watch: {
    '$route': 'updateAll'
  },
  computed: {
    chunkedProds () {
      return this.prods[this.pageIndex()]
    },
    howManyChunks () {
      return this.prods.length
    },
    empty () {
      if (this.prods.length === 0) {return true}
      return false
    }
  },
  created () {
    this.updateAll()
  }
}
</script>
