<template>
  <div class="alert alert-secondary">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline m-0">
      <h4>
        Всего задач: {{ tasksAll.length }}, отображается: {{ filteredTasks.length }}.
      </h4>
      <div class="btn-toolbar mb-2 mb-md-0">
        <a class="btn btn-sm btn-primary" @click="showOptions = !showOptions">
          <i class="fa-solid fa-gears"></i> Настройки
        </a>
      </div>
    </div>

    <div class="row mb-3 border-top pt-3" v-if="showOptions">
      <div class="col-3">
        <h5>Фильтры</h5>
        <input type="checkbox" v-model="tasksFilters.showActive" id="check-show-active"> <label for="check-show-active">В работе</label><br>
        <input type="checkbox" v-model="tasksFilters.showPrivate" id="check-show-private"> <label for="check-show-private">Личные</label><br>
        <input type="checkbox" v-model="tasksFilters.showCompleted" id="check-show-completed"> <label for="check-show-completed">Завершенные</label><br>
        <input type="checkbox" v-model="tasksFilters.showFavoritesOnly" id="check-show-favorite-only"> <label for="check-show-favorite-only">Только избранные</label><br>
      </div>

      <div class="col-3">
        <h5>Что показывать</h5>
        <input type="checkbox" v-model="showCategory" id="check-show-category"> <label for="check-show-category">Категории</label><br>
        <input type="checkbox" v-model="showCommentsCount" id="check-show-comments-count"> <label for="check-show-comments-count">Количество комментов</label><br>
        <input type="checkbox" v-model="showCreatedDate" id="check-show-created-date"> <label for="check-show-created-date">Дата создания</label><br>
        <input type="checkbox" v-model="showCompletedDate" id="check-show-completed-date"> <label for="check-show-completed-date">Дата завершения</label><br>
      </div>

      <div class="col-6">
        <h5>Категории</h5>
        <span v-for="category in categoriesAll" :key="category.id">
          <input type="checkbox" v-model="categoriesVisibleIds" :id="'category' + category.id" :value="category.id"> <label :for="'category' + category.id" class="category-label">{{ category.title }}</label><br>
        </span>
        <button @click="categoriesVisibleIds = []" class="btn btn-sm btn-primary me-1">Убрать все</button>
        <button @click="loadCategoriesIds" class="btn btn-sm btn-primary">Показать все</button>
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
        <th v-if="showCreatedDate" class="table-column-date text-center">
          Создана
        </th>
        <th v-if="showCompletedDate" class="table-column-date text-center">
          Завершена
        </th>
      </tr>
    </thead>

    <tbody>
      <template v-for="task in filteredTasks" :key="task.pk">
        <tr :class="task.is_acquainted ? '' : 'table-success'">
          <td>
            <i class="fa-regular fa-star" v-if="task.is_favorite"></i>
          </td>
          <td>
            <i class="fa-regular fa-lock" v-if="task.is_private"></i>
          </td>
          <td>
            <a :href="task.url">
              {{ task.title }}
            </a>
            <span v-if="showCommentsCount" class="text-muted category-title">
              <i class="fa-solid fa-comments"></i> {{ task.comments_count }}<span v-if="task.new_comments_count"> &middot; {{ task.new_comments_count }}</span>
            </span>
            <span v-if="showCategory" class="text-muted category-title">
              <i class="fa-solid fa-tag"></i> {{ task.category }}
            </span>
          </td>
          <td v-if="showCreatedDate" class="table-column-date text-center">
            <span class="text-muted category-title">
              {{ formatDateTime(task.created) }}
            </span>
          </td>
          <td v-if="showCompletedDate" class="table-column-date text-center">
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
export default {
  name: 'App',
  data() {
    return {
      // `task_list` and `categoriesList` are generated in Django template in `footer_scripts` block.
      // eslint-disable-next-line
      tasksAll: taskList,
      // eslint-disable-next-line
      categoriesAll: categoriesList,
      categoriesVisibleIds: JSON.parse(localStorage.getItem('categoriesVisibleIds') || '[]') || [],
      // TODO: save these filters to localStorage
      tasksFilters: {
        showActive: true,
        showCompleted: false,
        showPrivate: true,
        showFavoritesOnly: false,
      },
      showOptions: true,
      showCategory: localStorage.getItem('showCategory') === 'true',
      showCommentsCount: true,
      showCreatedDate: false,
      showCompletedDate: false,
    }
  },
  watch: {
    showCategory: {
      handler(showCategory) {
        localStorage.setItem('showCategory', showCategory.toString())
      },
    },
    categoriesVisibleIds: {
      handler(categoriesVisibleIds) {
        localStorage.setItem('categoriesVisibleIds', JSON.stringify(categoriesVisibleIds))
      },
      deep: true
    },
  },
  computed: {
    filteredTasks() {
      let filtered = this.tasksAll;

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

      filtered = filtered.filter((task) => this.categoriesVisibleIds.includes(task.category_id));

      return filtered;
    }
  },
  methods: {
    loadCategoriesIds() {
      // TODO: refactor - rename this function.
      for (let i=0; i<this.categoriesAll.length; i++) {
        this.categoriesVisibleIds.push(this.categoriesAll[i].id);
      }
    },
    formatDateTime(date) {
      return date.toLocaleDateString("ru-RU") + " " + date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
    },
  },
  mounted() {
    // do stuff on mount, e.g. load some data from localStorage.
  },
}
</script>

<style>
.table-tasks {
 font-family: var(--font-family-condensed);
}

.category-title {
  display: inline-block;
  margin: 0 0 0 10px;
}

.category-label {
 font-family: var(--font-family-condensed);
}

.table-column-date {
  width: 130px;
}
</style>
