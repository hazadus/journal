<template>
  <div class="component">
    <div class="tasks">

      <div class="d-flex align-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
        <div class="" style="flex-grow: 1;">
          Задач: {{ filteredTasks.length }} / {{ tasks.length }}
        </div>
      </div>

      <div class="task-list list-group list-group-flush">
        <a v-for="task in this.filteredTasks"
           :key="task.id" href="#"
           @click="this.selectedItem = task"
           class="task-list-item list-group-item list-group-item-action py-3 lh-sm"
           :class="{ active: selectedItem && selectedItem.id === task.id }">
          <div class="d-flex w-100 align-items-center justify-content-between">
            <strong class="mb-1">
              {{ task.title }}
            </strong>
            <i class="fa-regular fa-star" v-if="task.is_favorite"></i>
            <i class="fa-regular fa-lock" v-if="task.is_private"></i>
          </div>
          <div class="col-10 mb-1 small">
            {{ task.category_title }}
          </div>
        </a>
      </div>
    </div>

    <div class="alert alert-secondary flex-grow-1 m-1" v-if="viewOptions.showOptions">
      <OptionsPanel
          :categories="categories"
      />
    </div>
    <div class="task-detail" v-else>
      <span v-if="!selectedItem">
        Выберите задачу слева
      </span>
      <template v-else>
        <template v-if="detailItem">
          <h3>
            {{ detailItem.title }}
          </h3>

          <!-- Task Detail card -->
          <div class="card mb-2">
            <div class="card-header text-muted">
              <div class="d-flex flex-wrap flex-md-nowrap align-items-center">
                <div class="flex-grow-1">
                  <i v-if="detailItem.is_private" class="fa-solid fa-lock me-1"></i>
                  <i class="fa-regular fa-calendar"></i> {{ useFormatDateTime(detailItem.created) }}
                  &middot; <i class="fa-solid fa-user"></i> {{ useAuthorShortName(detailItem) }}
                  <template v-if="detailItem.is_completed">
                      &middot; <i class="fa-solid fa-calendar-check"></i>
                      {{ useFormatDateTime(detailItem.completed) }}
                  </template>
                </div>
              </div>
            </div>
            <div class="card-body task-card-body">
              <span v-html="detailItem.body"></span>
              <p v-if="detailItem.attachment" class="mt-3">
                <i class="fa-solid fa-paperclip"></i> Файл: <a :href="detailItem.attachment">
                  {{ detailItem.attachment }}</a>
              </p>
            </div>
          </div>


          <template v-if="comments">
            <h4>
              Комментарии
            </h4>

            <!-- Timeline -->
            <div class="timeline">
              <!-- Left vertical line -->
              <div class="timeline__line"></div>

              <!-- The timeline items timeline -->
              <div class="timeline__items">
                  <!-- Each timeline item -->
                  <div v-for="comment in comments" :key="comment.id" class="timeline__item mb-3">
                    <!-- The circle and title -->
                    <div class="timeline__top mb-2">
                      <!-- The circle -->
                      <div class="timeline__circle text-center">
                        <i class="fa-solid fa-comment"></i>
                      </div>

                      <!-- The title -->
                      <div class="timeline__title" :id="'comment-' + comment.id">
                        Добавлен комментарий:
                      </div>
                    </div>
                    <!-- The description which has round userpic -->
                    <div class="timeline__desc_avatar">
                      <div class="d-flex">
                        <!-- Comment author's avatar -->
                        <div class="timeline__desc_avatar__avatar mt-3 me-2">
                          <img :src="useAuthorAvatarURL(comment)" width="48" height="48" class="rounded-circle" alt="User picture">
                        </div>
                        <!-- Comment card -->
                        <div class="card flex-grow-1">
                          <div class="card-header d-flex text-muted">
                            <!-- Comment info -->
                            <div class="flex-grow-1">
                              <i class="fa-solid fa-user"></i> {{ useAuthorShortName(comment) }}, {{ useFormatDateTime(comment.created) }}
                            </div>
                          </div>
                          <div class="card-body" :id="'comment-body-' + comment.id">
                            {{ comment.body }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
              </div>
            </div>
          </template>

        </template>
      </template>
    </div>
  </div>
</template>

<script>
import OptionsPanel from "@/components/OptionsPanel.vue";
import {useFormatDateTime} from "@/utils";
import {useAuthorAvatarURL} from "@/utils";
import {useAuthorShortName} from "@/utils";
import {viewOptions} from "@/stores/viewOptions";

export default {
  name: "TaskListSidebar",
  components: {
    OptionsPanel
  },
  props: {
    tasks: Array,
    filteredTasks: Array,
    categories: Array,
  },
  data () {
    return {
      viewOptions,
      selectedItem: null,
      detailItem: null,
      comments: null,
    }
  },
  methods: {
    useFormatDateTime,
    useAuthorAvatarURL,
    useAuthorShortName,
    fetchSelectedTask() {
        const url = `/journal/tasks/api/v1/task/${this.selectedItem.id}/`;

        return window.axios
          .get(url, {})
          .then((response) => {
            // `response.data` contains JS object made from fetched JSON
            this.detailItem = response.data;
            return response.data;
          })
          .catch(function (error) {
            console.log("Axios.get error:", error);
            throw error;
          });
    },
    fetchSelectedTaskComments() {
        const url = `/journal/tasks/api/v1/comment_list/`;

        return window.axios
          .get(url, {
            params: {
              taskId: this.selectedItem.id,
            }
          })
          .then((response) => {
            // `response.data` contains JS object made from fetched JSON
            this.comments = response.data;
            return response.data;
          })
          .catch(function (error) {
            console.log("Axios.get error:", error);
            throw error;
          });
    },
  },
  watch: {
    selectedItem: {
      handler() {
        this.fetchSelectedTask();
        this.fetchSelectedTaskComments();
      }
    },
  },
  mounted() {
    // `Select` first item of the list on page load.
    if (!this.selectedItem) {
      if (this.tasks.length) {
        this.selectedItem = this.tasks[0];
      }
    }
  },
}
</script>

<style scoped>
.component {
  display: flex;
  margin: -16px 0 0 -24px;
}

.tasks {
  width: 380px;
  flex-shrink: 0;
  border-right: 1px solid #e4e4e4;
}

@media (max-width: 1400px) {
  .tasks {
    width: 300px;
  }
}

.task-list {
  height: calc(100vh - 185px);
  overflow-y: auto;
}

.task-list-item {
  font-family: var(--font-family-condensed);
}

.task-detail {
  height: calc(100vh - 121px);
  padding: 10px;
  flex-grow: 1;
  overflow-y: auto;
}
</style>