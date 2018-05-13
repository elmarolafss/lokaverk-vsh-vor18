<template>
  <div class="h-100">
    <div class="dt w-100 h-100" v-if="error">
      <div class="subheadline tc dtc v-mid">
        This product does not exist...
      </div>
    </div>
    <div class="flex w-100 h-100 items-center justify-center" v-else>
      <div v-if="loading">
        <h2 class="tc mt5">loading...</h2>
      </div>
      <div class="single-product-grid mw9 center" v-else>
        <div class="single-prod-img-grid pt3 pl3 pb3">
          <img v-on:click="decrementImgs()" class="ba box-sizing" v-lazy="prod.images[iOne]" :alt="prod.id">
          <img v-on:click="incrementImgs()" class="ba box-sizing" v-lazy="prod.images[iTwo]" :alt="prod.id">
        </div>
        <div class="flex flex-column pa3 h-100 justify-center">
          <p class="mv3 ba tc pv2 ui-big">{{ prod.title }}</p>
          <p class="mv3 ba tc pv2 headline">{{ prod.price }}$</p>
          <button class="mv3 outline btn-white btn-wide ui-big">BUY NOW</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $backend from '../backend'

export default {
  name: 'product',
  data () {
    return {
      prod: {},
      pid: this.$route.params.id,
      loading: false,
      error: false,
      errorMessage: "",
      iOne: 0,
      iTwo: 1
    }
  },
  methods: {
    fetchProduct () {
      this.loading = true
      $backend.fetchProduct(this.pid)
        .then(responseData => {
          this.prod = responseData
          this.loading = false
        }).catch(error => {
          this.error = true
          this.errorMessage = error.message
        })
    },
    incrementImgs () {
      let len = this.prod.images.length
      if (this.iTwo + 1 < len) {
        this.iTwo += 1
        this.iOne += 1
      }
    },
    decrementImgs () {
      if (this.iOne - 1 >= 0) {
        this.iTwo -= 1
        this.iOne -= 1
      }
    }
  },
  created () {
    this.fetchProduct()
  }
}
</script>
