<template>
  <div class="d-flex component">
    <div class="tasks d-flex flex-column align-items-stretch bg-white">
      <a class="d-flex align-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
        <span class="fs-5 fw-semibold">Список задач</span>
      </a>

      <div class="list-group list-group-flush task-list scrollarea mh-100">
        <a v-for="task in this.tasks"
           :key="task.pk" href="#"
           @click="this.selectedItem = task"
           class="task-list-item list-group-item list-group-item-action py-3 lh-sm"
           :class="{ active: selectedItem && selectedItem.pk === task.pk }">
          <div class="d-flex w-100 align-items-center justify-content-between">
            <strong class="mb-1">
              {{ task.title }}
            </strong>
            <small>Wed</small>
          </div>
          <div class="col-10 mb-1 small">
            {{ task.category }}
          </div>
        </a>
      </div>
    </div>

    <div class="task-detail scrollarea flex-grow-0">
      <span v-if="selectedItem">
        <!-- Insert raw html: https://vuejs.org/guide/essentials/template-syntax.html#raw-html -->
        <!-- /journal/task/1/full_block/ -->
        <span v-html="detailContent"></span>
      </span>
      <span v-else>
        Выберите задачу слева
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "TaskListSidebar",
  props: {
    tasks: Array,
  },
  data () {
    return {
      selectedItem: null,
      detailContent: null,
    }
  },
  watch: {
    selectedItem: {
      handler() {
        const url = `/journal/task/${this.selectedItem.pk}/full_block/`;

        return window.axios
          .get(url, {})
          .then((response) => {
            // `response.data` contains JS object made from fetched JSON
            this.detailContent = response.data;
            return response.data;
          })
          .catch(function (error) {
            console.log("Axios.get error:", error);
            throw error;
          });
      }
    },
  }
}
</script>

<style scoped>
.component {
  height: 650px;
  margin: -15px 0 0 -20px;
}

.scrollarea {
  overflow-y: scroll;
}

.tasks {
  width: 380px;
  border: 1px solid #6c757d;
}

.task-list {
}

.task-list-item {
  font-family: var(--font-family-condensed);
}
</style>