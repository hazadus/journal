<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">
      Задачи: табличный вид (Vue)
    </h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <button @click="viewOptions.isTableView = !viewOptions.isTableView" class="btn btn-sm btn-warning me-1">
        <template v-if="viewOptions.isTableView">
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
        v-if="viewOptions.isTableView"
        :tasks="tasksAll"
        :filtered-tasks="filteredTasks"
        :categories="categoriesAll"
    />
    <TaskListSidebar
        v-else
        :tasks="tasksAll"
        :filtered-tasks="filteredTasks"
        :categories="categoriesAll"
    />
  </template>
</template>

<script>
import TaskListTable from "@/components/TaskListTable.vue";
import TaskListSidebar from "@/components/TaskListSidebar.vue";
import {fetchOptions} from "@/stores/fetchOptions";
import {taskFilters} from "@/stores/taskFilters";
import {viewOptions} from "@/stores/viewOptions";

export default {
  name: 'App',
  components: {
    TaskListTable,
    TaskListSidebar
  },
  data() {
    return {
      // Imported from stores:
      // NB: note emphasis on `store` variable names; accessed without `this`!
      fetchOptions,
      taskFilters,
      viewOptions,
      // Fetched from API:
      tasksAll: [],
      categoriesAll: [],
      polling: null,
    }
  },
  computed: {
    filteredTasks() {
      let filtered = this.tasksAll;

      if (!taskFilters.showCompleted) {
        filtered = filtered.filter((task) => !task.is_completed);
      }

      if (!taskFilters.showActive) {
        filtered = filtered.filter((task) => task.is_completed);
      }

      if (taskFilters.showFavoritesOnly) {
        filtered = filtered.filter((task) => task.is_favorite);
      }

      if (!taskFilters.showPrivate) {
        filtered = filtered.filter((task) => !task.is_private);
      }

      filtered = filtered.filter((task) => viewOptions.categoriesVisibleIds.includes(task.category));

      return filtered;
    }
  },
  watch: {
    fetchOptions: {
      handler(newFetchOptions) {
        localStorage.setItem('fetchOptions', JSON.stringify(newFetchOptions));
        // Re-fetch all tasks - maybe orderByFields changed?
        this.fetchAllTasks();
      },
      deep: true
    },
    viewOptions: {
      handler(newViewOptions) {
        localStorage.setItem('viewOptions', JSON.stringify(newViewOptions))
      },
      deep: true
    },
    taskFilters: {
      handler(newTaskFilters) {
        localStorage.setItem('taskFilters', JSON.stringify(newTaskFilters))
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

          // Load options from storage only after categories are fetched
          let storedViewOptions = JSON.parse(localStorage.getItem('viewOptions'));
          if (storedViewOptions) {
            viewOptions.set(storedViewOptions);
          }

          if (viewOptions.categoriesVisibleIds == null) {
            viewOptions.copyAllCategoryIdsToVisible(this.categoriesAll);
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
        orderByFields: fetchOptions.orderByFields.toString(),
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
        if (fetchOptions.autoUpdate) {
          this.fetchAllTasks();
        }
      }, fetchOptions.pollDataTimeout)
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
    let storedFetchOptions = JSON.parse(localStorage.getItem('fetchOptions'));
    if (storedFetchOptions) {
      fetchOptions.set(storedFetchOptions);
    }

    let storedTaskFilters = JSON.parse(localStorage.getItem('taskFilters'));
    if (storedTaskFilters) {
      taskFilters.set(storedTaskFilters);
    }
  },
}
</script>

<style scoped>

</style>
