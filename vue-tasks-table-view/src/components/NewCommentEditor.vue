<!-- Show the component only when we got logged in user's data from backend -->
<template v-if="isUserDataFetched">
  <form>
    <div class="mb-3">
      <label for="comment_text" class="form-label">Добавить комментарий:</label>
      <div class="d-flex">
        <div class="me-2">
          <img v-if="userData.avatar_img"
               class="rounded-circle"
               :src="userData.avatar_img"
               :alt="'Фото ' + userData.username"
               width="48"
               height="48">
        </div>
        <div class="flex-grow-1">
          <textarea class="form-control"
                    v-model="newCommentText"
                    :rows="textAreaRowsQty"
                    :disabled="isPosting"
          ></textarea>
        </div>
      </div>
    </div>

    <div class="d-flex mb-3 flex-wrap">
      <div class="flex-grow-1">
        <input v-model="isCompleteTask"
               class="form-check-input me-1"
               type="checkbox"
               id="check-complete-task"
               :disabled="isCompleteTaskCheckboxDisabled">
        <label class="form-check-label" for="check-complete-task">
          Завершить задачу с этим комментарием
        </label>
      </div>
      <div class="btn-toolbar mb-2 mb-md-0 justify-content-end">
        <button v-if="!task.is_acquainted"
                @click.prevent="onClickAcquaint"
                :disabled="isAcquainting"
                class="btn btn-sm btn-primary me-2">
          <i class="fa-solid fa-file-signature"></i> Ознакомлен
        </button>
        <button @click.prevent="onClickSubmit"
                :disabled="isPosting"
                class="btn btn-sm btn-success">
          <template v-if="isCompleteTask">
            <i class="fa-solid fa-file-circle-check"></i> Завершить задачу
          </template>
          <template v-else>
            <i class="fa-solid fa-comment"></i> Комментировать
          </template>
        </button>
      </div>
    </div>
  </form>

  <div v-if="isPreviewVisible"
       class="alert alert-secondary flex-grow-1 m-1">
    <h5>Предварительный просмотр</h5>
    <div class="card-body">
      <span v-html="markdownToHtml">
      </span>
    </div>
  </div>
</template>

<script>
import {useLinesCount} from "@/utils";

export default {
  name: 'NewCommentEditor',
  props: ['task', 'onClickAcquaint'],
  emits: ['newCommentPosted'],
  data() {
    return {
      newCommentText: '',
      userData: {
        username: '',
        avatar_img: '',
      },
      isUserDataFetched: false,
      isCompleteTask: false,
      isPosting: false,
      isAcquainting: false,
    }
  },
  methods: {
    useLinesCount,
    fetchUserData() {
      const url = `/users/api/v1/logged_in_user/`;

      return window.axios
        .get(url, {
          params: {},
        })
        .then((response) => {
          this.userData = response.data;
          this.isUserDataFetched = true;
        })
        .catch(function (error) {
          console.log("Axios.get error:", error);
          throw error;
        });
    },
    onClickSubmit() {
      if (this.newCommentText.trimStart().trimEnd().length < 5) {
        alert('Для отправки комментария, введите текст (не менее 5 символов)!');
      } else {
        this.isPosting = true;
        const newComment = {
          "task": this.task.id,
          "author": this.userData.id,
          "body": this.newCommentText,
        };

        // Actually do the post:
        return window.axios
          .post('/journal/tasks/api/v1/comment/', {
            newComment: newComment,
            isCompleteTask: this.isCompleteTask,
          })
          .then((response) => {
            this.isPosting = false;
            this.newCommentText = "";
            this.$emit('newCommentPosted', response);
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },
  },
  computed: {
    markdownToHtml() {
      // Convert comment text with markdown markup to raw HTML and sanitize it:
      return this.markdown(this.newCommentText);
    },
    isPreviewVisible() {
      // We want preview to be visible only when there's some text entered:
      return this.newCommentText.trimStart().trimEnd().length > 0;
    },
    textAreaRowsQty() {
      // Make text area taller to match number of lines in the entered comment,
      // using `minRows` as minimal height of the text area.
      const minRows = 3;
      const linesQty = useLinesCount(this.newCommentText);
      return linesQty <= minRows ? minRows : linesQty;
    },
    isCompleteTaskCheckboxDisabled() {
      // Disable when there's short text in the text area, or posting in progress:
      return this.newCommentText.trimStart().trimEnd().length < 5 || this.isPosting;
    },
  },
  created() {
    this.fetchUserData();
  }
}
</script>