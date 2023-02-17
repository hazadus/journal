<template>
  <div class="component">
    <div class="tasks">

      <a class="d-flex align-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
        <span class="fs-5 fw-semibold">Список задач</span>
      </a>

      <div class="task-list list-group list-group-flush">
        <a v-for="task in this.tasks"
           :key="task.id" href="#"
           @click="this.selectedItem = task"
           class="task-list-item list-group-item list-group-item-action py-3 lh-sm"
           :class="{ active: selectedItem && selectedItem.id === task.id }">
          <div class="d-flex w-100 align-items-center justify-content-between">
            <strong class="mb-1">
              {{ task.title }}
            </strong>
            <i class="fa-regular fa-star" v-if="task.is_favorite"></i>
            <i class="fa-regular fa-lock" v-if="task.is_private"></i>
          </div>
          <div class="col-10 mb-1 small">
            {{ task.category_title }}
          </div>
        </a>
      </div>
    </div>

    <div class="task-detail">
      <template v-if="selectedItem">
        <template v-if="detailItem">
          <h3>
            {{ detailItem.title }}
          </h3>
          <div class="m-2">
            <p>
              Автор: {{ detailItem.author_last_name }} {{ detailItem.author_first_name }} {{ detailItem.author_second_name }},
              {{ formatDateTime(detailItem.created) }}
            </p>
            <span v-html="detailItem.body"></span>
          </div>

          <h4>
            Комментарии
          </h4>
          <template v-if="comments">
            <ul>
              <li v-for="comment in comments" :key="comment.id">
                {{ comment.author_last_name }} {{ comment.author_first_name }} {{ comment.author_second_name }}
                &middot; {{ formatDateTime(comment.created) }}<br>
                {{ comment.body }}
              </li>
            </ul>
          </template>

        </template>
      </template>
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
      detailItem: null,
      comments: null,
    }
  },
  methods: {
    formatDateTime(dateIsoFormatString) {
      // Format date like "06.02.2023 20:05" from python `date.isoformat` string.
      let date = new Date(dateIsoFormatString);
      return date.toLocaleDateString("ru-RU") + " " + date.toLocaleTimeString("ru-RU", {
        hour: "2-digit",
        minute: "2-digit"
      });
    },
    fetchSelectedTask() {
        const url = `/journal/tasks/api/v1/task/${this.selectedItem.id}/`;

        return window.axios
          .get(url, {})
          .then((response) => {
            // `response.data` contains JS object made from fetched JSON
            this.detailItem = response.data;
            return response.data;
          })
          .catch(function (error) {
            console.log("Axios.get error:", error);
            throw error;
          });
    },
    fetchSelectedTaskComments() {
        const url = `/journal/tasks/api/v1/comment_list/`;

        return window.axios
          .get(url, {
            params: {
              taskId: this.selectedItem.id,
            }
          })
          .then((response) => {
            // `response.data` contains JS object made from fetched JSON
            this.comments = response.data;
            return response.data;
          })
          .catch(function (error) {
            console.log("Axios.get error:", error);
            throw error;
          });
    },
  },
  watch: {
    selectedItem: {
      handler() {
        this.fetchSelectedTask();
        this.fetchSelectedTaskComments();
      }
    },
  }
}
</script>

<style scoped>
.component {
  display: flex;
  margin: -16px 0 0 -24px;
}

.tasks {
  width: 380px;
  flex-shrink: 0;
  border-right: 1px solid #e4e4e4;
}

@media (max-width: 1400px) {
  .tasks {
    width: 300px;
  }
}

.task-list {
  height: calc(100vh - 185px);
  overflow-y: scroll;
}

.task-list-item {
  font-family: var(--font-family-condensed);
}

.task-detail {
  height: calc(100vh - 121px);
  padding: 10px;
  flex-grow: 1;
  overflow-y: scroll;
}
</style>