<template>
  <div class="product-thumb">
    <h1>{{ prod.name }}</h1>
    <img :src="prod.link" :alt="prod.name">
  </div>
</template>

<script>
export default {
  name: 'product-thumb',
  data () {
    return {
      prod: {
        name: "prod name",
        link: "https://cdn.shopify.com/s/files/1/0293/9277/products/Fashion_Nova_12-07-17-777.jpg?v=1513114501"
      }
    }
  }
}
</script>
