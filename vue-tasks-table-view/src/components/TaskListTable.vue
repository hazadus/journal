<template>
  <div class="alert alert-secondary">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline m-0">
      <h4>
        Всего задач: {{ this.tasks.length }}, отображается: {{ filteredTasks.length }}.
      </h4>
    </div>

    <!--
    orderByFields passed from OrderBySelector->OptionsPanel->here (from bottom to top);
    -->
    <OptionsPanel
        v-if="viewOptions.showOptions"
        :categories="categories"
        :categories-visible-ids="categoriesVisibleIds"
        @update:categoriesVisibleIds="(newCategoriesVisibleIds) => this.$emit('update:categoriesVisibleIds', newCategoriesVisibleIds)"
        :view-options="viewOptions"
        :tasks-filters="tasksFilters"
        :fetch-options="fetchOptions"
        @order-by-fields-changed="(newOrder) => this.$emit('orderChanged', newOrder)"
    />
  </div>

  <div class="table-tasks-wrapper">
    <table class="table table-hover table-tasks text-nowrap">
      <thead>
        <tr>
          <th scope="col" class="text-center" style="width: 30px;">
            <i class="fa-regular fa-star"></i>
          </th>
          <th scope="col" class="text-center" style="width: 30px;">
            <i class="fa-regular fa-lock"></i>
          </th>
          <th>
            Задача
          </th>
          <th v-if="viewOptions.showCreatedDate" class="table-column-date text-center">
            Создана
          </th>
          <th v-if="viewOptions.showCompletedDate" class="table-column-date text-center">
            Завершена
          </th>
        </tr>
      </thead>

      <tbody>
        <template v-for="task in filteredTasks" :key="task.id">
          <tr :class="task.is_acquainted ? '' : 'table-success'">
            <td class="cell-favorite">
              <i class="fa-regular fa-star" v-if="task.is_favorite"></i>
            </td>
            <td class="text-muted">
              <i class="fa-regular fa-lock" v-if="task.is_private"></i>
            </td>
            <td>
              <span v-if="task.is_completed" class="task-completed-mark">
                <i class="fa-solid fa-check"></i>
              </span>
              <a :href="`/journal/task/${task.id}/`" class="task-title-link">
                {{ task.title }}
              </a>
              <span v-if="viewOptions.showCommentsCount" class="text-muted category-title">
                <i class="fa-solid fa-comments"></i> {{ task.comments_count }}<span v-if="task.new_comments_count"> &middot; {{ task.new_comments_count }}</span>
              </span>
              <span v-if="task.attachment" class="ms-1">
                <a :href="task.attachment" class="text-muted">
                  <i class="fa-solid fa-paperclip"></i>
                </a>
              </span>
              <span v-if="viewOptions.showCategory" class="text-muted category-title">
                <i class="fa-solid fa-tag"></i> {{ task.category_title }}
              </span>
            </td>
            <td v-if="viewOptions.showCreatedDate" class="table-column-date text-center">
              <span class="text-muted category-title">
                {{ useFormatDateTime(task.created) }}
              </span>
            </td>
            <td v-if="viewOptions.showCompletedDate" class="table-column-date text-center">
              <span class="text-muted category-title">
                {{ task.is_completed ? useFormatDateTime(task.completed) : '' }}
              </span>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script>
import OptionsPanel from "@/components/OptionsPanel.vue";
import {useFormatDateTime} from "@/utils";

export default {
  name: "TaskListTable",
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
  methods: {
    useFormatDateTime,
  },
}
</script>

<style scoped>
.table-tasks-wrapper {
  overflow-x: auto;
}

.table-tasks {
  font-family: var(--font-family-condensed);
  font-weight: 300;
}

.cell-favorite {
  color: var(--bs-warning);
}

.task-completed-mark {
  margin: 0 5px 0 0;
  color: var(--bs-success);
}

.table-column-date {
  width: 130px;
}

.task-title-link {
  font-size: 18px;
}

@media (max-width: 768px) {
  .task-title-link {
    font-size: 16px;
  }
}

.category-title {
  display: inline-block;
  margin: 0 0 0 10px;
}
</style>