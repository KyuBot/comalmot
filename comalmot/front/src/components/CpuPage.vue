<template>
  <div v-if="cpus">
    <h1>CPU</h1>
    <div v-for="cpu in cpus">
      <h3>이름: {{ cpu.name }}</h3>
      <h5>목적: {{ cpu.purpose }}</h5>
      <h5>가격: {{ cpu.price }}</h5>
      <h5>평점: {{ cpu.rate }}</h5>
    </div>
  </div>
</template>

<script>
export default {
  created() {
    this.$http
      .get("/api/cpus")
      .then((res) => {
        this.cpus = res.data;
      })
      .catch((err) => {
        console.error(err);
      });
  },

  data() {
    return {
      cpus: [],
    };
  },
};
</script>

