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

        <!-- Buttons on the right side - hide when editing -->
        <div v-if="!isEditing">
          <!-- Edit button -->
          <a v-if="task.author === userInfo.id"
             @click.prevent="onClickEdit"
             class="toolbar-link toolbar-link-primary me-1">
            <i class="fa-solid fa-pen-to-square"></i>
          </a>
        </div>

      </div>
    </div>

    <!-- TASK EDITOR STUFF -->
    <!-- Edit / preview tabs -->
    <ul v-if="isEditing" class="nav nav-tabs ms-1 mt-1">
      <li class="nav-item">
        <a class="nav-link"
           :class="activeEditorTabName === 'edit' ? 'active' : ''"
           @click.prevent="activeEditorTabName = 'edit'"
           href="#">Редактировать</a>
      </li>
      <li class="nav-item">
        <a class="nav-link"
           :class="activeEditorTabName === 'preview' ? 'active' : ''"
           @click.prevent="activeEditorTabName = 'preview'"
           href="#">Предпросмотр</a>
      </li>
    </ul>

    <div v-if="isEditing" class="d-flex mb-3 flex-wrap ms-1 me-1">
      <!-- Comment editor -->
      <textarea v-if="activeEditorTabName === 'edit'" class="form-control"
                v-model="modifiedBody"
                :rows="textAreaRowsQty">
      </textarea>
      <!-- Comment preview -->
      <div v-if="activeEditorTabName === 'preview'" class="card-body d-block w-100">
        <span v-html="markdownToHtml(this.modifiedBody)"></span>
      </div>

      <!-- Buttons -->
      <div class="help-text flex-grow-1 text-muted p-1 align-items-center">
        <i class="fa-solid fa-info-circle"></i> В тексте задачи можно использовать разметку <a href="http://konvut.github.io/k50articles/" target="_blank">Markdown <i class="fa-solid fa-question-circle"></i></a> .
      </div>
      <div class="btn-toolbar mt-1 mb-2 mb-md-0 justify-content-end">
        <button class="btn btn-sm btn-secondary me-1"
                @click="isEditing=false">
          <i class="fa-solid fa-cancel"></i> Отмена
        </button>
        <button class="btn btn-sm btn-success"
                @click="onClickSave">
            <i class="fa-solid fa-save"></i> Сохранить
        </button>
      </div>
    </div>

    <!-- TASK BODY -->
    <div v-if="!isEditing" class="card-body task-card-body">
      <span v-html="markdownToHtml(task.body)"></span>
      <p v-if="task.attachment" class="mt-3">
        <i class="fa-solid fa-paperclip"></i> Файл: <a :href="task.attachment">
          {{ decodeURI(task.attachment) }}</a>
      </p>
    </div>
  </div>
</template>

<script>
import {useFormatDateTime, useAuthorAvatarURL, useAuthorShortName, useLinesCount} from "@/utils";
import TaskFavoriteButton from "@/components/TaskFavoriteButton.vue";

export default {
  name: 'TaskCard',
  components: {
    TaskFavoriteButton,
  },
  props: {
    task: Object,
    userInfo: Object,
  },
  emits: ['favoriteToggled'],
  data() {
    return {
      isEditing: false,
      activeEditorTabName: 'edit',  // 'edit' or 'preview' tabs.
      modifiedBody: null, // Represents task body content changed while editing.
    }
  },
  computed: {
    textAreaRowsQty() {
      // Make text area taller to match number of lines in the comment,
      // using `minRows` as minimal height of the text area.
      const minRows = 3;
      const linesQty = useLinesCount(this.modifiedBody);
      return linesQty <= minRows ? minRows : linesQty;
    },
  },
  methods: {
    useFormatDateTime,
    useAuthorAvatarURL,
    useAuthorShortName,
    useLinesCount,
    onClickEdit() {
      this.isEditing = true;
      this.activeEditorTabName = 'edit';
      this.modifiedBody = this.task.body;
    },
    onClickSave() {
      alert('В РАЗРАБОТКЕ!\nЗдесь редактирование пока не работает - воспользуйтесь кнопкой редактирования задачи на отдельной странице задачи.\n\nEdit task ' + this.task.id);
    },
    markdownToHtml(markedDownContent) {
      // Sanitizes `markedDownContent` and converts markdown to HTML.
      return this.markdown(markedDownContent);
    },
  },
}
</script>

<style scoped>
  .help-text {
    font-family: var(--font-family-condensed);
  }
</style>