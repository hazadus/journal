<template>
  <div class="alert alert-secondary">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline m-0">
      <h4>
        Всего задач: {{ this.tasks.length }}, отображается: {{ filteredTasks.length }}.
      </h4>
      <div class="btn-toolbar mb-2 mb-md-0">
        <button class="btn btn-sm btn-primary" @click="viewOptions.showOptions = !viewOptions.showOptions">
          <i class="fa-solid fa-gears"></i> Настройки
        </button>
      </div>
    </div>

    <div class="row mb-3 border-top pt-3 mt-3" v-if="viewOptions.showOptions">
      <!-- TODO: make columns responsive -->
      <div class="col-2">
        <h5 class="options-title mb-1 pb-1 border-bottom">Фильтры</h5>
        <input type="checkbox" v-model="tasksFilters.showActive" id="check-show-active"> <label for="check-show-active" class="options-checkbox-label">В работе</label><br>
        <input type="checkbox" v-model="tasksFilters.showPrivate" id="check-show-private"> <label for="check-show-private" class="options-checkbox-label">Личные</label><br>
        <input type="checkbox" v-model="tasksFilters.showCompleted" id="check-show-completed"> <label for="check-show-completed" class="options-checkbox-label">Завершенные</label><br>
        <input type="checkbox" v-model="tasksFilters.showFavoritesOnly" id="check-show-favorite-only"> <label for="check-show-favorite-only" class="options-checkbox-label">Только избранные</label><br>
      </div>

      <div class="col-2">
        <h5 class="options-title mb-1 pb-1 border-bottom">Упорядочить</h5>
        <OrderBySelector @orderChanged="(newOrder) => this.orderByFields = newOrder" />
      </div>

      <div class="col-2">
        <h5 class="options-title mb-1 pb-1 border-bottom">Отображение</h5>
        <input type="checkbox" v-model="fetchOptions.autoUpdate" id="check-auto-update"> <label for="check-auto-update" class="options-checkbox-label">Автообновление</label><br>
        <input type="checkbox" v-model="viewOptions.showCategory" id="check-show-category"> <label for="check-show-category" class="options-checkbox-label">Категории</label><br>
        <input type="checkbox" v-model="viewOptions.showCommentsCount" id="check-show-comments-count"> <label for="check-show-comments-count" class="options-checkbox-label">Комментарии</label><br>
        <input type="checkbox" v-model="viewOptions.showCreatedDate" id="check-show-created-date"> <label for="check-show-created-date" class="options-checkbox-label">Дата создания</label><br>
        <input type="checkbox" v-model="viewOptions.showCompletedDate" id="check-show-completed-date"> <label for="check-show-completed-date" class="options-checkbox-label">Дата завершения</label><br>
      </div>

      <div class="col-6">
        <h5 class="options-title mb-1 pb-1 border-bottom">Категории</h5>
        <span v-for="category in this.categories" :key="category.id">
          <input type="checkbox" v-model="categoriesVisibleIds" :id="'category' + category.id" :value="category.id"> <label :for="'category' + category.id" class="options-checkbox-label">{{ category.title }}</label><br>
        </span>
        <button @click="categoriesVisibleIds = []" class="btn btn-sm btn-primary me-1 mt-2">Убрать все</button>
        <button @click="copyAllCategoryIdsToVisible" class="btn btn-sm btn-primary mt-2">Показать все</button>
      </div>
    </div>
  </div>

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
          <td>
            <i class="fa-regular fa-star" v-if="task.is_favorite"></i>
          </td>
          <td>
            <i class="fa-regular fa-lock" v-if="task.is_private"></i>
          </td>
          <td>
            <i v-if="task.is_completed" class="fa-solid fa-check-double"></i>
            <a :href="`/journal/task/${task.id}/`">
              {{ task.title }}
            </a>
            <span v-if="viewOptions.showCommentsCount" class="text-muted category-title">
              <i class="fa-solid fa-comments"></i> {{ task.comments_count }}<span v-if="task.new_comments_count"> &middot; {{ task.new_comments_count }}</span>
            </span>
            <span v-if="viewOptions.showCategory" class="text-muted category-title">
              <i class="fa-solid fa-tag"></i> {{ task.category_title }}
            </span>
          </td>
          <td v-if="viewOptions.showCreatedDate" class="table-column-date text-center">
            <span class="text-muted category-title">
              {{ formatDateTime(task.created) }}
            </span>
          </td>
          <td v-if="viewOptions.showCompletedDate" class="table-column-date text-center">
            <span class="text-muted category-title">
              {{ task.is_completed ? formatDateTime(task.completed) : '' }}
            </span>
          </td>
        </tr>
      </template>
    </tbody>
  </table>
</template>

<script>
import OrderBySelector from "@/components/OrderBySelector.vue";

export default {
  name: "TaskListTable",
  components: {
    OrderBySelector
  },
  props: {
    tasks: Array,
    categories: Array,
    defaultFetchOptions: Object
  },
  emits: ['fetchOptionsChanged', 'orderChanged'],
  data() {
    return {
      // List of visible categories in task list
      categoriesVisibleIds: [],
      // List of fields to order by on backend
      orderByFields: [],
      // Default task filters. Will be loaded from localStorage in mounted()
      tasksFilters: {
        showActive: true,
        showCompleted: false,
        showPrivate: true,
        showFavoritesOnly: false,
      },
      // Defaul view options. Will be loaded from localStorage in mounted()
      viewOptions: {
        showOptions: true,        // show options pane
        showCategory: false,      // show category name
        showCommentsCount: true,  // show comments count
        showCreatedDate: false,   // show creation date
        showCompletedDate: false, // show completion date
      },
      // Fetch options
      fetchOptions: this.defaultFetchOptions,
    }
  },
  watch: {
    categoriesVisibleIds: {
      handler(categoriesVisibleIds) {
        localStorage.setItem('categoriesVisibleIds', JSON.stringify(categoriesVisibleIds))
      },
      deep: true
    },
    orderByFields: {
      handler() {
        // Refetch all tasks on order change: do this on parent
        this.$emit('orderChanged', this.orderByFields)
      },
      deep: true
    },
    viewOptions: {
      handler(viewOptions) {
        localStorage.setItem('viewOptions', JSON.stringify(viewOptions))
      },
      deep: true
    },
    tasksFilters: {
      handler(tasksFilters) {
        localStorage.setItem('tasksFilters', JSON.stringify(tasksFilters))
      },
      deep: true
    },
    fetchOptions: {
      handler(fetchOptions) {
        this.$emit('fetchOptionsChanged', fetchOptions)
      },
      deep: true
    },
  },
  computed: {
    filteredTasks() {
      let filtered = this.tasks;

      if (!this.tasksFilters.showCompleted) {
        filtered = filtered.filter((task) => !task.is_completed);
      }

      if (!this.tasksFilters.showActive) {
        filtered = filtered.filter((task) => task.is_completed);
      }

      if (this.tasksFilters.showFavoritesOnly) {
        filtered = filtered.filter((task) => task.is_favorite);
      }

      if (!this.tasksFilters.showPrivate) {
        filtered = filtered.filter((task) => !task.is_private);
      }

      filtered = filtered.filter((task) => this.categoriesVisibleIds.includes(task.category));

      return filtered;
    }
  },
  methods: {
    copyAllCategoryIdsToVisible() {
      // Copies all category IDs from category list passed from backend to the list of visible categories,
      for (let i = 0; i < this.categories.length; i++) {
        this.categoriesVisibleIds.push(this.categories[i].id);
      }
    },
    formatDateTime(dateIsoFormatString) {
      // Format date like "06.02.2023 20:05" from python `date.isoformat` string.
      let date = new Date(dateIsoFormatString);
      return date.toLocaleDateString("ru-RU") + " " + date.toLocaleTimeString("ru-RU", {
        hour: "2-digit",
        minute: "2-digit"
      });
    },
  },
  mounted() {
    // do stuff on mount, e.g. load some data from localStorage.
    let viewOptions = JSON.parse(localStorage.getItem('viewOptions'));
    if (viewOptions) {
      this.viewOptions = viewOptions;
    }

    let tasksFilters = JSON.parse(localStorage.getItem('tasksFilters'));
    if (tasksFilters) {
      this.tasksFilters = tasksFilters;
    }

    let categoriesVisibleIds = JSON.parse(localStorage.getItem('categoriesVisibleIds'));
    if (categoriesVisibleIds) {
      this.categoriesVisibleIds = categoriesVisibleIds;
    } else {
      this.copyAllCategoryIdsToVisible();
    }
  },
}
</script>

<style scoped>
.options-title {
  font-family: var(--font-family-condensed);
}

.options-checkbox-label {
  font-family: var(--font-family-condensed);
}

.table-tasks {
 font-family: var(--font-family-condensed);
}

.category-title {
  display: inline-block;
  margin: 0 0 0 10px;
}

.table-column-date {
  width: 130px;
}
</style>