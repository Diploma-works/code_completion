<template>
  <div id="app">
    <a href="https://www.jetbrains.com/"><img alt="JetBrains logo" src="./assets/logo.png" width="200" height="216.8"></a>
    <Showcase/>
  </div>
</template>

<script>
import Showcase from './components/Showcase.vue'

export default {
  name: 'App',
  components: {
    Showcase
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
  margin-top: 30px;
  margin-bottom: 120px;
}
</style>
