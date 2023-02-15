<template>
  <TaskListTable
      :tasks="tasksAll"
      :categories="categoriesAll"
      :default-fetch-options="fetchOptions"
      @fetchOptionsChanged="(newFetchOptions) => this.fetchOptions = newFetchOptions"
      @orderChanged="(newOrder) => this.orderByFields = newOrder"
  />
</template>

<script>
import TaskListTable from "@/components/TaskListTable.vue";

export default {
  name: 'App',
  components: {
    TaskListTable
  },
  data() {
    return {
      tasksAll: [],
      categoriesAll: [],
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
