import Vue from 'vue'
import App from './App.vue'
import ElementUI, {Select, Input, Button, Table} from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.config.productionTip = false
Vue.use(ElementUI);

Vue.component(Select.name, Select);
Vue.component(Input.name, Input);
Vue.component(Button.name, Button);
Vue.component(Table.name, Table);

new Vue({
  el: '#app',
  render: h => h(App),
}).$mount('#app')
