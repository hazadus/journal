<!--
-- Component represents a timeline item with one comment.
--
-- Usage in timeline:

  <div class="timeline">
    <div class="timeline__line"></div>
    <div class="timeline__items">
      <CommentTimelineItem
        v-for="comment in comments" :key="comment.id"
        :comment="comment"
      />
    </div>
  </div>

-->
<template>
  <!-- Timeline item -->
  <div class="timeline__item mb-3">
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

        <CommentCard
            :comment="comment"
        />

      </div>
    </div>
  </div>
</template>

<script>
import {useFormatDateTime, useAuthorAvatarURL, useAuthorShortName} from "@/utils";
import CommentCard from "@/components/CommentCard.vue";

export default {
  name: "CommentTimelineItem",
  components: {
    CommentCard,
  },
  props: {
    comment: Object,
  },
  methods: {
    useFormatDateTime,
    useAuthorAvatarURL,
    useAuthorShortName,
  },
}
</script>