<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">
      Задачи: табличный вид (Vue)
    </h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <button @click="isTableView = !isTableView" class="btn btn-sm btn-warning me-1">
        <template v-if="isTableView">
          <i class="fa-solid fa-columns"></i> Колонки
        </template>
        <template v-else>
          <i class="fa-solid fa-table"></i> Таблица
        </template>
      </button>
      <button class="btn btn-sm btn-primary me-1" @click="viewOptions.showOptions = !viewOptions.showOptions">
        <i class="fa-solid fa-gears"></i> Настройки
      </button>
      <a class="btn btn-sm btn-success" href="/journal/task/create/">
        <i class="fa-solid fa-file-circle-plus"></i> Добавить задачу
      </a>
    </div>
  </div>
  <!--
  ** NB: `v-else` is here because we want to render the component only when categories are
  ** already fetched from backend, or else they won't be available as props in component's `mounted()` method.
  ** This will lead to the situation when on the first load (when nothing is stored in localStorage)
  ** the list of visible categories inside the component will be empty, and no tasks will be displayed.
  -->
  <div v-if="!tasksAll.length || !categoriesAll.length" class="d-flex align-items-center">
    <div class="spinner-border text-primary me-3" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div>
      Идёт загрузка &mdash; пожалуйста, подождите!
    </div>
  </div>
  <template v-else>
    <TaskListTable
        v-if="isTableView"
        :tasks="tasksAll"
        :filtered-tasks="filteredTasks"
        :categories="categoriesAll"
        v-model:categories-visible-ids="categoriesVisibleIds"
        v-model:view-options="viewOptions"
        :tasks-filters="tasksFilters"
        v-model:fetch-options="fetchOptions"
        @orderChanged="(newOrder) => this.orderByFields = newOrder"
    />
    <TaskListSidebar
        v-else
        :tasks="tasksAll"
        :filtered-tasks="filteredTasks"
        :categories="categoriesAll"
        v-model:categories-visible-ids="categoriesVisibleIds"
        v-model:view-options="viewOptions"
        :tasks-filters="tasksFilters"
        v-model:fetch-options="fetchOptions"
        @orderChanged="(newOrder) => this.orderByFields = newOrder"
    />
  </template>
</template>

<script>
import TaskListTable from "@/components/TaskListTable.vue";
import TaskListSidebar from "@/components/TaskListSidebar.vue";

export default {
  name: 'App',
  components: {
    TaskListTable,
    TaskListSidebar
  },
  data() {
    return {
      tasksAll: [],
      categoriesAll: [],
      // List of visible categories in task list
      categoriesVisibleIds: [],
      // Show as table or 3-column view
      isTableView: true,
      // Ordering options
      orderByFields: [],
      // Fetch options
      fetchOptions: {
        autoUpdate: true,         // re-fetch data from backend from time to time
        pollDataTimeout: 5000,    // update period, ms
      },
      polling: null,
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
    }
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

      filtered = filtered.filter((task) => this.categoriesVisibleIds.includes(task.category));

      return filtered;
    }
  },
  watch: {
    fetchOptions: {
      handler(fetchOptions) {
        localStorage.setItem('fetchOptions', JSON.stringify(fetchOptions));
      },
      deep: true
    },
    orderByFields: {
      handler() {
        // Refetch all tasks on order change
        this.fetchAllTasks();
      },
      deep: true
    },
    categoriesVisibleIds: {
      handler(categoriesVisibleIds) {
        localStorage.setItem('categoriesVisibleIds', JSON.stringify(categoriesVisibleIds))
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
  },
  methods: {
    fetchAllCategories() {
      const url = window.location.origin + `/journal/tasks/api/v1/category_list/`;

      return window.axios
        .get(url, {
          params: {},
        })
        .then((response) => {
          this.categoriesAll = response.data;

          // Check options only after categories are fetched
          let categoriesVisibleIdsItem = localStorage.getItem('categoriesVisibleIds');
          if (categoriesVisibleIdsItem == null) {
            for (let i = 0; i < this.categoriesAll.length; i++) {
              this.categoriesVisibleIds.push(this.categoriesAll[i].id);
            }
          } else {
            this.categoriesVisibleIds = JSON.parse(categoriesVisibleIdsItem);
          }

          return response.data;
        })
        .catch(function (error) {
          console.log("Axios.get error:", error);
          throw error;
        });
    },
    fetchAllTasks() {
      const url = window.location.origin + `/journal/tasks/api/v1/task_list/`;

      // Pass sort order to backend like:
      // ?orderByFields=-is_favorite,-is_completed,-is_acquainted,-created,-completed
      let queryParam = {
        orderByFields: this.orderByFields.toString(),
      };

      return window.axios
        .get(url, {
          params: queryParam,
        })
        .then((response) => {
          this.tasksAll = response.data;
          return response.data;
        })
        .catch(function (error) {
          console.log("Axios.get error:", error);
          throw error;
        });
    },
    pollData () {
      this.polling = setInterval(() => {
        if (this.fetchOptions.autoUpdate) {
          this.fetchAllTasks();
        }
      }, this.fetchOptions.pollDataTimeout)
    }
  },
  created() {
    this.fetchAllCategories();
    this.fetchAllTasks();
    this.pollData();
  },
  beforeUnmount() {
    clearInterval(this.polling);
  },
  mounted() {
    // do stuff on mount, e.g. load some data from localStorage.
    let fetchOptions = JSON.parse(localStorage.getItem('fetchOptions'));
    if (fetchOptions) {
      this.fetchOptions = fetchOptions;
    }

    // do stuff on mount, e.g. load some data from localStorage.
    let viewOptions = JSON.parse(localStorage.getItem('viewOptions'));
    if (viewOptions) {
      this.viewOptions = viewOptions;
    }

    let tasksFilters = JSON.parse(localStorage.getItem('tasksFilters'));
    if (tasksFilters) {
      this.tasksFilters = tasksFilters;
    }
  },
}
</script>

<style scoped>

</style>
