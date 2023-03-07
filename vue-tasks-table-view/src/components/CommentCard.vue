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

      <!-- Buttons on the right side -->
      <div>
        <!-- Edit button -->
        <a class="toolbar-link toolbar-link-primary me-1"
           @click.prevent="onClickEdit">
          <i class="fa-solid fa-pen-to-square"></i>
        </a>
        <!-- Archive button -->
        <a class="toolbar-link toolbar-link-danger"
           @click.prevent="onClickArchive">
          <i class="fa-solid fa-trash"></i>
        </a>
      </div>
    </div>

    <!-- Body -->
    <div class="card-body" :id="'comment-body-' + comment.id">
      <span v-html="markdownToHtml(comment.body)"></span>
    </div>

  </div>
</template>

<script>
import {useFormatDateTime, useAuthorShortName} from "@/utils";

export default {
  name: "CommentCard",
  props: {
    comment: Object,
  },
  data() {
    return {
      isEditing: false,
      modifiedBody: this.comment.body, // Represents comment body content changed while editing.
    }
  },
  methods: {
    useFormatDateTime,
    useAuthorShortName,
    onClickEdit() {
      alert('Edit comment ' + this.comment.id);
    },
    onClickArchive() {
      alert('Archive comment ' + this.comment.id);
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