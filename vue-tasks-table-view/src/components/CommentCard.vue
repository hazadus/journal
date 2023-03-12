<template>
  <!-- Comment card -->
  <div class="card flex-grow-1"
       :class="comment.is_acquainted ? 'bubble' : 'card-new border-success bubble-new'">

    <!-- Header -->
    <div class="card-header d-flex text-muted">
      <!-- Comment info -->
      <div class="flex-grow-1">
        <i class="fa-solid fa-user"></i> {{ useAuthorShortName(comment) }}, {{ useFormatDateTime(comment.created) }}
      </div>

      <!-- Buttons on the right side - hide when editing -->
      <div v-if="!isEditing">
        <!-- Edit button -->
        <a v-if="comment.author === userInfo.id"
           class="toolbar-link toolbar-link-primary me-1"
           @click.prevent="onClickEdit">
          <i class="fa-solid fa-pen-to-square"></i>
        </a>
        <!-- Archive button -->
        <a v-if="comment.author === userInfo.id"
           class="toolbar-link toolbar-link-danger"
           @click.prevent="onClickArchive">
          <i class="fa-solid fa-trash"></i>
        </a>
      </div>
    </div>

    <!-- COMMENT EDITOR STUFF -->
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

    <!-- COMMENT BODY -->
    <div v-if="!isEditing" class="card-body" :id="'comment-body-' + comment.id">
      <span v-html="markdownToHtml(comment.body)"></span>
    </div>

  </div>
</template>

<script>
import {useFormatDateTime, useAuthorShortName, useLinesCount} from "@/utils";

export default {
  name: "CommentCard",
  props: {
    comment: Object,
    userInfo: Object,
  },
  data() {
    return {
      isEditing: false,
      activeEditorTabName: 'edit',  // 'edit' or 'preview' tabs.
      modifiedBody: null, // Represents comment body content changed while editing.
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
    useAuthorShortName,
    useLinesCount,
    onClickEdit() {
      this.isEditing = true;
      this.activeEditorTabName = 'edit';
      this.modifiedBody = this.comment.body;
    },
    onClickSave() {
      alert('В РАЗРАБОТКЕ!\nЗдесь редактирование пока не работает - воспользуйтесь кнопкой редактирования комментария на отдельной странице задачи.\n\nEdit comment ' + this.comment.id);
    },
    onClickArchive() {
      alert('В РАЗРАБОТКЕ!\nЗдесь удаление пока не работает - воспользуйтесь кнопкой удаления комментария на отдельной странице задачи.\n\nArchive comment ' + this.comment.id);
    },
    markdownToHtml(markedDownContent) {
      // Sanitizes `markedDownContent` and converts markdown to HTML.
      return this.markdown(markedDownContent);
    },
    sanitize(content) {
      // Returns sanitized `content`.
      return this.sanitizeHtml(content);
    },
  },
}
</script>

<style scoped>
  .nav-link {
    font-size: 16px;
  }

  .help-text {
    font-family: var(--font-family-condensed);
  }
</style>