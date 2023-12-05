import Vue from "vue";
import Element from "./screens/Element.vue";

Vue.config.productionTip = false;



new Vue({
  render: h => h(Element)
}).$mount("#app");