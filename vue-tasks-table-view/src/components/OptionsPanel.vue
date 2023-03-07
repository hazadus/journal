<template>
  <div class="row mb-3 border-top pt-3 mt-3">
    <div class="col-6 col-lg-2">
      <h5 class="options-title mb-1 pb-1 border-bottom">Фильтры</h5>
      <input type="checkbox" v-model="taskFilters.showActive" id="check-show-active"> <label for="check-show-active" class="options-checkbox-label">В работе</label><br>
      <input type="checkbox" v-model="taskFilters.showPrivate" id="check-show-private"> <label for="check-show-private" class="options-checkbox-label">Личные</label><br>
      <input type="checkbox" v-model="taskFilters.showCompleted" id="check-show-completed"> <label for="check-show-completed" class="options-checkbox-label">Завершенные</label><br>
      <input type="checkbox" v-model="taskFilters.showFavoritesOnly" id="check-show-favorite-only"> <label for="check-show-favorite-only" class="options-checkbox-label">Только <i class="fa-regular fa-star"></i></label><br>
    </div>

    <div class="col-6 col-lg-2">
      <h5 class="options-title mb-1 pb-1 border-bottom">Упорядочить</h5>
      <OrderBySelector />
    </div>

    <div class="col-6 col-lg-2">
      <h5 class="options-title mb-1 pb-1 border-bottom">Отображение</h5>

      <span class="options-checkbox-block"><input type="checkbox" v-model="fetchOptions.autoUpdate" id="check-auto-update"> <label for="check-auto-update" class="options-checkbox-label">Автообновление</label></span>
      <span class="options-checkbox-block"><input type="checkbox" v-model="viewOptions.showCategory" id="check-show-category"> <label for="check-show-category" class="options-checkbox-label">Категории</label></span>
      <span class="options-checkbox-block"><input type="checkbox" v-model="viewOptions.showCommentsCount" id="check-show-comments-count"> <label for="check-show-comments-count" class="options-checkbox-label">Комментарии</label></span>
      <span class="options-checkbox-block"><input type="checkbox" v-model="viewOptions.showCreatedDate" id="check-show-created-date"> <label for="check-show-created-date" class="options-checkbox-label">Дата создания</label></span>
      <span class="options-checkbox-block"><input type="checkbox" v-model="viewOptions.showCompletedDate" id="check-show-completed-date"> <label for="check-show-completed-date" class="options-checkbox-label">Дата завершения</label></span>
    </div>

    <div class="col-6 col-lg-6">
      <h5 class="options-title mb-1 pb-1 border-bottom">Категории</h5>
      <span v-for="category in this.categories" :key="category.id" class="options-checkbox-block">
        <input type="checkbox" v-model="viewOptions.categoriesVisibleIds" :id="'category' + category.id" :value="category.id"> <label :for="'category' + category.id" class="options-checkbox-label" @click.alt.prevent="viewOptions.categoriesVisibleIds=[category.id]">{{ category.title }}</label><br>
      </span>
      <button @click="viewOptions.categoriesVisibleIds = []" class="btn btn-sm btn-primary me-1 mt-2">Убрать все</button>
      <button @click="viewOptions.copyAllCategoryIdsToVisible(categories)" class="btn btn-sm btn-primary mt-2">Показать все</button>
      <br>
    </div>
  </div>

  <div class="btn-toolbar mb-0 justify-content-end border-top">
    <button class="btn btn-sm btn-primary me-2 mb-0 mt-2"
            @click="viewOptions.showOptions = !viewOptions.showOptions">
      <i class="fa-solid fa-close"></i> Закрыть настройки
    </button>
  </div>
</template>

<script>
import OrderBySelector from "@/components/OrderBySelector.vue";
import {fetchOptions} from "@/stores/fetchOptions";
import {taskFilters} from "@/stores/taskFilters";
import {viewOptions} from "@/stores/viewOptions";

export default {
  name: "OptionsPanel",
  components: {
    OrderBySelector
  },
  props: {
    categories: Array,
  },
  data() {
    return {
      fetchOptions,
      taskFilters,
      viewOptions,
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

.options-checkbox-block {
  display: block;
  /* Keep option checkboxes and labels on one line on small screens */
  overflow-x: hidden;
  white-space: nowrap;
}
</style>