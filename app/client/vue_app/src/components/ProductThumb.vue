<template>
  <router-link to="#" class="link black product-thumb h-100">
    <div class="flex flex-column justify-between h-100">
      <div class="overflow-hidden ba" @mouseover="hover = true" @mouseleave="hover = false">
        <div v-if="hover">
          <img class="prod-thumb-img" v-lazy="thumb2" alt="">
        </div>
        <div v-else>
          <img class="prod-thumb-img" v-lazy="thumb1" alt="">
        </div>
      </div>
      <div class="flex-column tc h3 bg-white bb br bl">
        <p class="pv2 ui">{{ prod.title }}</p>
        <p class="pv2 pr2 ui">{{ prod.price }}$</p>
      </div>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'product-thumb',
  props: {
    prod: Object
  },
  data () {
    return {
      hover: false,
      thumb1: this.prod.images[0],
      thumb2: this.prod.images[1]
    }
  }
}
</script>
