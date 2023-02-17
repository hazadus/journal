<template>
  <div class="component">
    <div class="tasks">

      <div class="d-flex align-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
        <div class="" style="flex-grow: 1;">
          Задач: {{ filteredTasks.length }} / {{ tasks.length }}
        </div>
      </div>

      <div class="task-list list-group list-group-flush">
        <a v-for="task in this.filteredTasks"
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

    <div class="alert alert-secondary" v-if="viewOptions.showOptions">
      <OptionsPanel
          :categories="categories"
          :categories-visible-ids="categoriesVisibleIds"
          @update:categoriesVisibleIds="(newCategoriesVisibleIds) => this.$emit('update:categoriesVisibleIds', newCategoriesVisibleIds)"
          :view-options="viewOptions"
          :tasks-filters="tasksFilters"
          :fetch-options="fetchOptions"
          @order-by-fields-changed="(newOrder) => this.$emit('orderChanged', newOrder)"
      />
    </div>
    <div class="task-detail" v-else>
      <template v-if="selectedItem">
        <template v-if="detailItem">
          <h3>
            {{ detailItem.title }}
          </h3>
          <div class="m-2">
            <p>
              Автор: {{ detailItem.author_last_name }} {{ detailItem.author_first_name }} {{ detailItem.author_second_name }},
              {{ useFormatDateTime(detailItem.created) }}
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
                &middot; {{ useFormatDateTime(comment.created) }}<br>
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
import OptionsPanel from "@/components/OptionsPanel.vue";
import {useFormatDateTime} from "@/utils";

export default {
  name: "TaskListSidebar",
  components: {
    OptionsPanel
  },
  props: {
    tasks: Array,
    filteredTasks: Array,
    categories: Array,
    categoriesVisibleIds: Array,
    fetchOptions: Object,
    viewOptions: Object,
    tasksFilters: Object,
  },
  emits: [
    'orderChanged',
    'update:categoriesVisibleIds',
  ],
  data () {
    return {
      selectedItem: null,
      detailItem: null,
      comments: null,
    }
  },
  methods: {
    useFormatDateTime,
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
  overflow-y: auto;
}

.task-list-item {
  font-family: var(--font-family-condensed);
}

.task-detail {
  height: calc(100vh - 121px);
  padding: 10px;
  flex-grow: 1;
  overflow-y: auto;
}
</style>