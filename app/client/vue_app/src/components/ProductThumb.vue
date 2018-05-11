<template>
  <router-link to="#" class="product-thumb h-100">
  	<div class="flex flex-column justify-between h-100">
	  	<div class="hide-child" @mouseover="hover = true" @mouseleave="hover = false">
	  		<div v-if="hover">
	  			<img class="child" v-lazy="thumb2" :alt="prod.id">
	  		</div>
	  		<div v-else>
		  		<img v-lazy="thumb1" :alt="prod.id">
	  		</div>
	  	</div>
	    <p class="ui tc">{{ prod.title }}</p>
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
