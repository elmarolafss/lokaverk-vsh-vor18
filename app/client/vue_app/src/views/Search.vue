<template>
  <div class="cf h-100">
    <div class="db fl w5 h-100 br b--black">.</div>
    <div class="fl w-80 search-grid pa3">
      <div v-for="product in chunkedProds">
        <ProductThumb class="tc" :prod="product"></ProductThumb>
      </div>
    </div>
    <div class="fl w-80 h3 pa3 dt">
      <div class="dtc v-mid center tc">
        <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">1</a>
        <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">2</a>
        <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">3</a>
        <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">4</a>
        <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">5</a>
        <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">...</a>
        <a class="link black pa2 bt bb b--black hover-bg-red hover-white" href="1">90</a>
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
    chunkProds: function (pnum) {
      let _temp_arr = [];
      for (let i = 0, len=this.prods.length; i < len; i += this.chunkSize)
        _temp_arr.push(this.prods.slice(i, i + this.chunkSize));
      return _temp_arr[pnum-1];
    }
  },
  watch: {
    '$route' (to, from) {
      this.prods = {}
      this.query = this.$route.query
      this.fetchProducts()
    }
  },
  computed: {
    chunkedProds: function () {
      return this.chunkProds(this.pageNum)
    }
  },
  mounted () {
    this.prods = {}
    this.query = this.$route.query
    this.fetchProducts()
  }
}
</script>
