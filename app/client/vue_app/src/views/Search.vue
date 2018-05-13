<template>
  <div class="cf h-100">
    <div class="db fl w5 h-100 br b--black">
      <div class="fixed w5 tc mt6">
        sort by price hér
        <div class="mv3 w-100 bb"></div>
        colors koma hér
      </div>
    </div>
    <div class="fl w-80 search-grid pt3 ph3">
      <div v-for="product in chunkedProds[pageNum-1]">
        <ProductThumb class="tc" :prod="product"></ProductThumb>
      </div>
    </div>
    <div class="fl w-80 h3 pa3 dt">
      <div class="dtc v-mid center tc">
        <router-link
        v-for="i in howManyChunks"
        :to="{ path: '/search', query: { cat: cat, page: i } }"
        class="link black pa2 bt bb b--black hover-bg-red hover-white">
          {{ i }}
        </router-link>
        <!-- <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">1</a> -->
      </div>
    </div>
  </div>
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
      query: this.$route.query,
      prods: {},
      cat: '',
      pageNum: 1,
      chunkSize: 48
    }
  },
  methods: {
    fetchProducts () {
      this.cat = this.query.cat
      $backend.fetchProducts(this.cat)
        .then(responseData => {
          this.prods = responseData
        }).catch(error => {
          this.error = error.message
        })
    },
    chunkProds: function () {
      let _temp_arr = [];
      for (let i = 0, len=this.prods.length; i < len; i += this.chunkSize)
        _temp_arr.push(this.prods.slice(i, i + this.chunkSize));
      return _temp_arr;
    },
    updateAll: function () {
      this.prods = {}
      this.query = this.$route.query
      this.fetchProducts()
      if (this.query.page) {
        this.pageNum = this.query.page
      } else {
        this.pageNum = 1
      }
      this.chunkedProds = this.chunkProds()
    }
  },
  watch: {
    '$route' (to, from) {
      this.updateAll()
      console.log("route changed?")
    }
  },
  computed: {
    chunkedProds: function () {
      return this.chunkProds()
    },
    howManyChunks: function () {
      return this.chunkedProds.length
    }
  },
  mounted () {
    console.log("2. mounted")
    this.updateAll()
  },
  created () {
    console.log("1. created")
    this.updateAll()
  }
}
</script>
