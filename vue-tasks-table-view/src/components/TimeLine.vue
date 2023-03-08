<template>
  <!-- Timeline -->
  <div class="timeline">
    <!-- Left vertical line -->
    <div class="timeline__line"></div>

    <!-- The timeline items -->
      <div class="timeline__items">
        <!-- Each timeline item -->
        <slot></slot>
      </div>
  </div>
</template>

<script>
export default {
  name: "TimeLine"
}
</script>