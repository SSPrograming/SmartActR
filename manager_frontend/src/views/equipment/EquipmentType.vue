<template>
  <div class="equipment-type">
    <div class="container">
      <div class="toolbar">
        <Toolbar refresh></Toolbar>
      </div>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'

export default {
  name: "EquipmentType",
  components: {
    Toolbar
  }
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: $--toolbar-margin-bottom;
}
</style>