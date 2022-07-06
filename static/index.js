import App from './App.vue'

const vm = new Vue({
    el: '#vm',
    render(h) {
        return  h(App);
      },
})

console.log(123)