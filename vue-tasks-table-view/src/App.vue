<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">
      Задачи: табличный вид (Vue)
    </h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <button @click="isTableView = !isTableView" class="btn btn-sm btn-warning me-3">
        <template v-if="isTableView">
          <i class="fa-solid fa-columns"></i> Колонки
        </template>
        <template v-else>
          <i class="fa-solid fa-table"></i> Таблица
        </template>
      </button>
      <a class="btn btn-sm btn-success" href="/journal/task/create/">
        <i class="fa-solid fa-file-circle-plus"></i> Добавить задачу
      </a>
    </div>
  </div>
  <!--
  ** NB: `v-else-if="categoriesAll.length"` is here because we want to render the component only when categories are
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
        :categories="categoriesAll"
        :default-fetch-options="fetchOptions"
        @fetchOptionsChanged="(newFetchOptions) => this.fetchOptions = newFetchOptions"
        @orderChanged="(newOrder) => this.orderByFields = newOrder"
    />
    <TaskListSidebar
        v-else
        :tasks="tasksAll"
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
      // Show as table or 3-column view
      isTableView: false,
      // Ordering options
      orderByFields: [],
      // Fetch options
      fetchOptions: {
        autoUpdate: true,         // re-fetch data from backend from time to time
        pollDataTimeout: 5000,    // update period, ms
      },
      polling: null,
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
  },
}
</script>

<style scoped>

</style>
