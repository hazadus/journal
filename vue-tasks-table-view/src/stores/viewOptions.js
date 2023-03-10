import { reactive } from 'vue';

export const viewOptions = reactive({
  isTableView: false,       // show as table or 3-column view
  showOptions: true,        // show options pane
  showCategory: false,      // show category name
  showCommentsCount: true,  // show comments count
  showCreatedDate: false,   // show creation date
  showCompletedDate: false, // show completion date
  categoriesVisibleIds: null,  // `null` to detect an initial moment when we need to copy all category ids here

  set(newOptions) {
    this.isTableView = newOptions.isTableView;
    this.showOptions = newOptions.showOptions;
    this.showCategory = newOptions.showCategory;
    this.showCommentsCount = newOptions.showCommentsCount;
    this.showCreatedDate = newOptions.showCreatedDate;
    this.showCompletedDate = newOptions.showCompletedDate;
    this.categoriesVisibleIds = newOptions.categoriesVisibleIds;
  },
  copyAllCategoryIdsToVisible(categories) {
    // Copies all category IDs from category list passed to the list of visible categories,
    this.categoriesVisibleIds = [];
    for (let i = 0; i < categories.length; i++) {
      this.categoriesVisibleIds.push(categories[i].id);
    }
  },
})