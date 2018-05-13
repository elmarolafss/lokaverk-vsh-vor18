<template>
  <header class="header-grid-item bg-black" role="header">
    <div class="header-nav h-100 center flex justify-between items-center">
      <router-link to="/" class="db link white hover-red">
        <div class="subheadline pt1">late</div>
      </router-link>
      <div class="flex justify-end">
        <!-- <div class="dn flex-l justify-between pv2"> -->
        <div class="dn flex-l justify-between pv2">
          <router-link :to="{ path: '/search', query: { cat: cat } }" v-for="cat in categories" class="link btn-white mr3">
            <div class="btn-child ui">{{ cat }}</div>
          </router-link>
        </div>
        <form v-bind:class="{ searchBarHidden: barHidden }" class="search-bar absolute pt2-ns" action="/search"><input ref="sinp" class="h2 w-100 ui ph2" type="text" name="term"></form>
        <svg v-on:click="toggleBar" class="z-999 pv2 h2 w2 pointer dib search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M22.89,20.63a12.79,12.79,0,1,0-2.26,2.26L29.74,32,32,29.74ZM6,19.57a9.59,9.59,0,1,1,14.6-1.23,9.49,9.49,0,0,1-2.26,2.26A9.6,9.6,0,0,1,6,19.57Z"/></svg>
        <svg class="dn-l ml3 pv2 h2 w2 pointer dib search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="4"/><rect y="14" width="32" height="4"/><rect y="28" width="32" height="4"/></svg>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'header',
  data () {
    return {
      barHidden: true,
      categories: [
        'dresses',
        'jackets',
        'tops',
        'jeans',
        'pants'
      ]
    }
  },
  methods: {
    toggleBar: function () {
      this.barHidden = !this.barHidden
      if (!this.barHidden) {
        this.$refs.sinp.focus()
      }
    }
  }
}
</script>
