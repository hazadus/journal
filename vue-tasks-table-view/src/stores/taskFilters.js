import { reactive } from 'vue';

export const taskFilters = reactive({
  showActive: true,
  showCompleted: false,
  showPrivate: true,
  showFavoritesOnly: false,

  set(newFilters) {
    this.showActive = newFilters.showActive;
    this.showCompleted = newFilters.showCompleted;
    this.showPrivate = newFilters.showPrivate;
    this.showFavoritesOnly = newFilters.showFavoritesOnly;
  },
})