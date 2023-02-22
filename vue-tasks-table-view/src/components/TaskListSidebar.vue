<template>
  <div class="component">
    <div class="tasks">

      <div class="d-flex align-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
        <div class="" style="flex-grow: 1;">
          Задач: {{ filteredTasks.length }} / {{ tasks.length }}
        </div>
      </div>

      <!-- Tasks list -->
      <div class="task-list list-group list-group-flush">
        <a v-for="task in this.filteredTasks"
           :key="task.id" href="#"
           @click="this.selectedItem = task"
           class="task-list-item list-group-item list-group-item-action py-3 lh-sm"
           :class="{ 'active': isTaskListItemActive(task), 'bg-success-subtle': isTaskListItemBgSuccessClass(task), }">
          <div class="d-flex w-100 align-items-center justify-content-between">
            <span class="task-list-item-title flex-grow-1"
                  :class="task.is_acquainted ? '' : 'task-list-item-title-new'">
              <span v-if="task.is_completed" class="task-completed-mark">
                <i class="fa-solid fa-check"></i>
              </span>
              {{ sanitize(task.title) }}
            </span>
            <TaskFavoriteButton
                :task="task"
                @toggled="(response) => {
                  task.is_favorite = response.is_favorite;
                  if (detailItem && detailItem.id === task.id) {
                    detailItem.is_favorite = response.is_favorite;
                  }
                  // Require refetch to update ordering
                  this.$emit('favoriteToggled');
                }"
            />
            <span class="text-muted" v-if="task.is_private">
              <i class="fa-regular fa-lock"></i>
            </span>
          </div>
          <div class="task-list-item-info mb-1 small">
            <span v-if="viewOptions.showCommentsCount" class="task-list-item-info-comment-count">
              <i class="fa-solid fa-comments"></i> {{ task.comments_count }}<template v-if="task.new_comments_count"> &middot; {{ task.new_comments_count }}</template>
            </span>
            <template v-if="viewOptions.showCategory">
              <i class="fa-regular fa-tag"></i> {{ task.category_title }}
            </template>
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
            {{ sanitize(detailItem.title) }}
          </h3>

          <!-- Task Detail card -->
          <div class="card mb-2"
               :class="detailItem.is_acquainted ? '' : 'card-new border-success'">
            <div class="card-header text-muted">
              <div class="d-flex flex-wrap flex-md-nowrap align-items-center">
                <div class="flex-grow-1">
                  <TaskFavoriteButton
                      :task="detailItem"
                      @toggled="(response) => {
                        detailItem.is_favorite = response.is_favorite;
                        // Require refetch to update ordering
                        this.$emit('favoriteToggled');
                      }"
                      style="margin: 0 5px 0 0;"
                  />
                  <i v-if="detailItem.is_private" class="fa-solid fa-lock me-1"></i>
                  <i class="fa-regular fa-calendar"></i> {{ useFormatDateTime(detailItem.created) }}
                  &middot; <i class="fa-solid fa-user"></i> {{ useAuthorShortName(detailItem) }}
                  <template v-if="detailItem.is_completed">
                      &middot; <i class="fa-solid fa-calendar-check"></i>
                      {{ useFormatDateTime(detailItem.completed) }}
                  </template>
                  &middot; <a class="text-muted" :href="`/journal/task/${detailItem.id}/`" target="_blank">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                  </a>
                </div>
              </div>
            </div>
            <div class="card-body task-card-body">
              <span v-html="markdownToHtml(detailItem.body)"></span>
              <p v-if="detailItem.attachment" class="mt-3">
                <i class="fa-solid fa-paperclip"></i> Файл: <a :href="detailItem.attachment">
                  {{ decodeURI(detailItem.attachment) }}</a>
              </p>
            </div>
          </div>

          <!-- Comments block -->
          <template v-if="comments">
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
                          <img class="rounded-circle"
                               :src="useAuthorAvatarURL(comment)"
                               :alt="'Фото ' + useAuthorShortName(comment)"
                               width="48"
                               height="48">
                        </div>
                        <!-- Comment card -->
                        <div class="card flex-grow-1"
                             :class="comment.is_acquainted ? 'bubble' : 'card-new border-success bubble-new'">
                          <div class="card-header d-flex text-muted">
                            <!-- Comment info -->
                            <div class="flex-grow-1">
                              <i class="fa-solid fa-user"></i> {{ useAuthorShortName(comment) }}, {{ useFormatDateTime(comment.created) }}
                            </div>
                          </div>
                          <div class="card-body" :id="'comment-body-' + comment.id">
                            <span v-html="markdownToHtml(comment.body)"></span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
              </div>
            </div>
          </template>

          <!-- Task completed alert -->
          <div class="alert alert-success" v-if="detailItem.is_completed">
            <i class="fa-solid fa-file-circle-check"></i> Задача завершена.
          </div>

          <!-- "Add new comment" block-->
          <NewCommentEditor
              v-if="!detailItem.is_completed"
              :task="detailItem"
          />

        </template>
      </template>
    </div>
  </div>
</template>

<script>
import OptionsPanel from "@/components/OptionsPanel.vue";
import TaskFavoriteButton from "@/components/TaskFavoriteButton.vue";
import NewCommentEditor from "@/components/NewCommentEditor.vue";
import {viewOptions} from "@/stores/viewOptions";
import {useFormatDateTime, useAuthorAvatarURL, useAuthorShortName} from "@/utils";

import {marked} from 'marked';
import * as DOMPurify from 'dompurify';

marked.setOptions({
  breaks: true,
});

export default {
  name: "TaskListSidebar",
  components: {
    OptionsPanel,
    TaskFavoriteButton,
    NewCommentEditor,
  },
  props: {
    tasks: Array,
    filteredTasks: Array,
    categories: Array,
  },
  emits: ['favoriteToggled'],
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
    isTaskListItemActive(task) {
      return this.selectedItem && this.selectedItem.id === task.id;
    },
    isTaskListItemBgSuccessClass(task) {
      // Returns true if task list item should have `bg-success-subtle` class -
      // when task.is_acquainted is false, and task is not selected by user.
      if (this.isTaskListItemActive(task)) {
        return false;
      } else {
        return !task.is_acquainted;
      }
    },
    markdownToHtml(markedDownContent) {
      // Sanitizes `markedDownContent` and converts markdown to HTML.
      return DOMPurify.sanitize(marked(markedDownContent));
    },
    sanitize(content) {
      // Returns sanitized `content`.
      return DOMPurify.sanitize(content);
    },
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

.task-list {
  height: calc(100vh - 185px);
  overflow-y: auto;
}

.task-list-item {
  font-family: var(--font-family-condensed);
  border-bottom: 1px solid #e4e4e4 !important;
}

.task-list-item-title {
  font-size: 18px;
  margin-bottom: 10px;
}

.task-list-item-title-new {
  font-weight: 600;
}

.task-list-item-info {
  font-size: 14px;
  color: var(--bs-light-text);
  overflow-x: hidden;
  white-space: nowrap;
}

.active .task-list-item-info {
  color: white;
}

.task-list-item-info-comment-count {
  margin: 0 5px 0 0;
}

@media (max-width: 1400px) {
  .tasks {
    width: 300px;
  }

  .task-list-item-title {
    font-size: 14px;
  }

  .task-list-item-info {
    font-size: 12px;
  }
}

.task-completed-mark {
  margin: 0 3px 0 0;
  color: var(--bs-success);
}

.task-detail {
  height: calc(100vh - 121px);
  padding: 10px;
  flex-grow: 1;
  overflow-y: auto;
}
</style>