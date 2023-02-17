<template>
  <div class="row mb-3 border-top pt-3 mt-3">
    <div class="col-6 col-lg-2">
      <h5 class="options-title mb-1 pb-1 border-bottom">Фильтры</h5>
      <input type="checkbox" v-model="localTasksFilters.showActive" id="check-show-active"> <label for="check-show-active" class="options-checkbox-label">В работе</label><br>
      <input type="checkbox" v-model="localTasksFilters.showPrivate" id="check-show-private"> <label for="check-show-private" class="options-checkbox-label">Личные</label><br>
      <input type="checkbox" v-model="localTasksFilters.showCompleted" id="check-show-completed"> <label for="check-show-completed" class="options-checkbox-label">Завершенные</label><br>
      <input type="checkbox" v-model="localTasksFilters.showFavoritesOnly" id="check-show-favorite-only"> <label for="check-show-favorite-only" class="options-checkbox-label">Только избранные</label><br>
    </div>

    <div class="col-6 col-lg-2">
      <h5 class="options-title mb-1 pb-1 border-bottom">Упорядочить</h5>
      <OrderBySelector @orderChanged="(newOrder) => this.$emit('orderByFieldsChanged', newOrder)" />
    </div>

    <div class="col-6 col-lg-2">
      <h5 class="options-title mb-1 pb-1 border-bottom">Отображение</h5>
      <input type="checkbox" v-model="localFetchOptions.autoUpdate" id="check-auto-update"> <label for="check-auto-update" class="options-checkbox-label">Автообновление</label><br>
      <input type="checkbox" v-model="localViewOptions.showCategory" id="check-show-category"> <label for="check-show-category" class="options-checkbox-label">Категории</label><br>
      <input type="checkbox" v-model="localViewOptions.showCommentsCount" id="check-show-comments-count"> <label for="check-show-comments-count" class="options-checkbox-label">Комментарии</label><br>
      <input type="checkbox" v-model="localViewOptions.showCreatedDate" id="check-show-created-date"> <label for="check-show-created-date" class="options-checkbox-label">Дата создания</label><br>
      <input type="checkbox" v-model="localViewOptions.showCompletedDate" id="check-show-completed-date"> <label for="check-show-completed-date" class="options-checkbox-label">Дата завершения</label><br>
    </div>

    <div class="col-6 col-lg-6">
      <h5 class="options-title mb-1 pb-1 border-bottom">Категории</h5>
      <span v-for="category in this.categories" :key="category.id" class="category-checkbox-block">
        <input type="checkbox" v-model="localCategoriesVisibleIds" :id="'category' + category.id" :value="category.id"> <label :for="'category' + category.id" class="options-checkbox-label" @click.alt.prevent="localCategoriesVisibleIds=[category.id]">{{ category.title }}</label><br>
      </span>
      <button @click="localCategoriesVisibleIds = []" class="btn btn-sm btn-primary me-1 mt-2">Убрать все</button>
      <button @click="copyAllCategoryIdsToVisible" class="btn btn-sm btn-primary mt-2">Показать все</button>
      <br>
    </div>
  </div>
</template>

<script>
import OrderBySelector from "@/components/OrderBySelector.vue";

export default {
  name: "OptionsPanel",
  components: {
    OrderBySelector
  },
  props: {
    categories: Array,
    categoriesVisibleIds: Array,
    viewOptions: Object,
    fetchOptions: Object,
    tasksFilters: Object,
  },
  emits: [
    'update:categoriesVisibleIds',
    'update:viewOptions',
    'update:fetchOptions',
    'update:tasksFilters',
    'orderByFieldsChanged',
  ],
  data() {
    return {
      // Locals
      localCategoriesVisibleIds: this.categoriesVisibleIds,   // List of visible categories in task list
      localViewOptions: this.viewOptions,  // updated!
      localFetchOptions: this.fetchOptions,  // somehow updated ...
      localTasksFilters: this.tasksFilters,  // updated!
    }
  },
  watch: {
    localCategoriesVisibleIds: {
      handler(newCategoriesVisibleIds) {
        this.$emit('update:categoriesVisibleIds', newCategoriesVisibleIds);
      },
      deep: true
    },
    localTasksFilters: {
      handler(newTasksFilters) {
        this.$emit('update:tasksFilters', newTasksFilters);
      },
      deep: true
    },
    localViewOptions: {
      handler(newViewOptions) {
        this.$emit('update:viewOptions', newViewOptions);
      },
      deep: true
    },
  },
  methods: {
    copyAllCategoryIdsToVisible() {
      // Copies all category IDs from category list passed from backend to the list of visible categories,
      this.localCategoriesVisibleIds = [];
      for (let i = 0; i < this.categories.length; i++) {
        this.localCategoriesVisibleIds.push(this.categories[i].id);
      }
    },
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

.category-checkbox-block {
  display: block;
  /* Keep category titles on one line on small screens */
  overflow-x: hidden;
  white-space: nowrap;
}
</style>