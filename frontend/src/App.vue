<template>
  <Free_form/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Free_form from './components/Free_form.vue'

export default {
  name: 'App',
  components: {
    HelloWorld, Free_form
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
