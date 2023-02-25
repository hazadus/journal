<template>
  <form>
    <div class="mb-3">
      <label for="comment_text" class="form-label">Добавить комментарий:</label>
      <div class="d-flex">
        <div class="me-2">
          Userpic
        </div>
        <div class="flex-grow-1">
          <textarea class="form-control"
                    v-model="newCommentText"
                    rows="3"
          ></textarea>
        </div>
      </div>
    </div>

    <div class="d-flex mb-3 flex-wrap">
      <div class="flex-grow-1">
        <input class="form-check-input" type="checkbox" value="complete" id="check-complete-task"
               name="check_complete_task" disabled>
        <label class="form-check-label" for="check-complete-task">
          Завершить задачу с этим комментарием
        </label>
      </div>
      <div class="btn-toolbar mb-2 mb-md-0 justify-content-end">
        <button class="btn btn-sm btn-primary me-2"
                v-if="!task.is_acquainted">
          <i class="fa-solid fa-file-signature"></i> Ознакомлен
        </button>
        <button class="btn btn-sm btn-success" id="submit-button">
          <i class="fa-solid fa-comment"></i> Комментировать
        </button>
      </div>
    </div>
  </form>

  <div>
    <h5>Предварительный просмотр</h5>
    <span v-html="markdownToHtml">
    </span>
  </div>
</template>

<script>
export default {
  name: "NewCommentEditor",
  props: {
    task: Object,
  },
  data() {
    return {
      newCommentText: "",
    }
  },
  computed: {
    markdownToHtml() {
      return this.markdown(this.newCommentText);
    },
  },
}
</script>

<style scoped>

</style>