import Vue from "vue";
import Router from "vue-router";
// import HelloWorld from '@/components/HelloWorld'
import Cpu from "@/components/CpuPage";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/cpu",
      name: "cpu",
      component: Cpu
    }
  ]
});
