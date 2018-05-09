<template>
  <div id="app" class="body-grid vh-100">
    <Header></Header>

    <!-- main content -->
    <router-view/>

    <!-- footer -->
    <Footer></Footer>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  components: {
    Header,
    Footer
  }
}
</script>
