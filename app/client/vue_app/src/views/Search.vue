<template>
  <div class="search-grid debug">
    <div v-if="all" v-for="prod in prods">
      <ProductThumb v-for="product in prod" :prod="product"></ProductThumb>
    </div>
    <div v-else>
      <ProductThumb :prod="prod"></ProductThumb>
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
      doo: '1233',
      error: '',
      query: this.$route.query,
      prods: {},
      all: true
    }
  },
  methods: {
    fetchProducts () {
      this.query = this.$route.query
      if (this.query.cat) { this.all = false }
      $backend.fetchProducts(this.query.cat)
        .then(responseData => {
          this.prods = responseData
        }).catch(error => {
          this.error = error.message
        })
    }
  },
  watch: {
    '$route' (to, from) {
      this.prods = {}
      this.fetchProducts()
    }
  },
  mounted () {
    this.fetchProducts()
  }
}
</script>
