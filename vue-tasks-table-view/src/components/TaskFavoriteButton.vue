<template>
  <button class="favorite-button"
        :class="task.is_favorite ? 'is-favorite' : ''"
        @click.stop="onClick(task)">
    <i class="fa-regular fa-star"></i>
  </button>
</template>

<script>
export default {
  name: "TaskFavoriteButton",
  props: {
    task: Object,
  },
  emits: ['toggled'],
  data() {
    return {
      isFetching: false,
    }
  },
  methods: {
    onClick(task) {
      const url = `/journal/tasks/api/v1/task/${task.id}/favorite/`;

      if (!this.isFetching) {
        this.isFetching = true;

        return window.axios
          .get(url, {
            params: {},
          })
          .then((response) => {
            this.$emit('toggled', response.data);
            return response.data;
          })
          .catch(function (error) {
            console.error("Axios.get error:", error);
            throw error;
          })
          .finally(() => {
            this.isFetching = false;
          });
      }
    },
  }
}
</script>

<style scoped>
.favorite-button {
  color: #e4e4e4 !important;
  background-color: transparent;
  border: 0;
  padding: 0;
  text-decoration: none;
  cursor: pointer;
  transition: 0.5s;
}

.favorite-button:hover {
  transform: scale(1.2);
}

.is-favorite {
  color: var(--bs-warning) !important;
}
</style>