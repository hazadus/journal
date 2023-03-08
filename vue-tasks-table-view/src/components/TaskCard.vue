<template>
  <div class="card mb-2"
       :class="task.is_acquainted ? '' : 'card-new border-success'">
    <div class="card-header text-muted">
      <div class="d-flex flex-wrap flex-md-nowrap align-items-center">
        <div class="flex-grow-1">
          <TaskFavoriteButton
              :task="task"
              @toggled="(response) => {
                this.$emit('favoriteToggled', response);
              }"
              style="margin: 0 5px 0 0;"
          />
          <i v-if="task.is_private" class="fa-solid fa-lock me-1"></i>
          <i class="fa-regular fa-calendar"></i> {{ useFormatDateTime(task.created) }}
          &middot; <i class="fa-solid fa-user"></i> {{ useAuthorShortName(task) }}
          <template v-if="task.is_completed">
              &middot; <i class="fa-solid fa-calendar-check"></i>
              {{ useFormatDateTime(task.completed) }}
          </template>
          &middot; <a class="text-muted" :href="`/journal/task/${task.id}/`" target="_blank">
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
          </a>
        </div>
      </div>
    </div>
    <div class="card-body task-card-body">
      <span v-html="markdownToHtml(task.body)"></span>
      <p v-if="task.attachment" class="mt-3">
        <i class="fa-solid fa-paperclip"></i> Файл: <a :href="task.attachment">
          {{ decodeURI(task.attachment) }}</a>
      </p>
    </div>
  </div>
</template>

<script>
import {useFormatDateTime, useAuthorAvatarURL, useAuthorShortName} from "@/utils";
import TaskFavoriteButton from "@/components/TaskFavoriteButton.vue";

export default {
  name: "TaskCard",
  components: {
    TaskFavoriteButton,
  },
  props: {
    task: Object,
  },
  emits: ['favoriteToggled'],
  methods: {
    useFormatDateTime,
    useAuthorAvatarURL,
    useAuthorShortName,
    markdownToHtml(markedDownContent) {
      // Sanitizes `markedDownContent` and converts markdown to HTML.
      return this.markdown(markedDownContent);
    },
  },
}
</script>