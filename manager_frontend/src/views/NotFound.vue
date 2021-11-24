<template>
  <div class="not-found">
    <div class="content">
      对不起，你当前访问的页面不存在！
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFound"
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

.content {
  padding-top: 5vh;
  padding-left: 5%;
  font-size: $--my-font-size-extra-large;
  color: $--color-danger;
  text-align: left;
}
</style>
