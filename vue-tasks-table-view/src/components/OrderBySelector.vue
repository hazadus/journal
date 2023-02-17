<!--
** OrderBySelector
**
** This component is used to build fields list for Django's `order_by()` ORM method using drag and drop
** and ascending/descending trigger button for each field.
**
** References:
** https://github.com/SortableJS/vue.draggable.next
** https://github.com/SortableJS/vue.draggable.next/blob/master/example/components/two-lists.vue
-->
<template>
  <div>
    <div>
      <h6 class="options-title">Сортировать по:</h6>
      <draggable :list="fieldsSelected" itemKey="id" group="fields" class="drop-area">
        <template #item="{ element }">
          <div class="drop-item">
            {{ element.name }}
            <button class="button-ascending" @click="element.ascending = !element.ascending">
              {{ element.ascending ? '&#9650;' : '&#9660;' }}
            </button>
          </div>
        </template>
      </draggable>
    </div>

    <div>
      <h6 class="options-title">Доступные поля:</h6>
      <draggable :list="fieldsAvailable" itemKey="id" group="fields" class="drop-area">
        <template #item="{ element }">
          <div class="drop-item">
            {{ element.name }}
          </div>
        </template>
      </draggable>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import {fetchOptions} from "@/stores/fetchOptions";

export default {
  components: {
    draggable
  },
  props: {
  },
  data() {
    return {
      fetchOptions,
      fieldsSelected: [
        { name: "Новое", id: 1, sortField: "is_acquainted", ascending: true },
        { name: "Избранное", id: 2, sortField: "is_favorite", ascending: false },
        { name: "В работе", id: 3, sortField: "is_completed", ascending: true },
        { name: "Дата завершения", id: 4, sortField: "completed", ascending: false },
      ],
      fieldsAvailable: [
        { name: "Дата создания", id: 5, sortField: "created", ascending: true },
        { name: "Личное", id: 6, sortField: "is_private", ascending: true },
      ]
    };
  },
  watch: {
    fieldsSelected: {
      handler(fieldsSelected) {
        localStorage.setItem('fieldsSelected', JSON.stringify(fieldsSelected))
        // Here's the main purpose of this component: pass resulting field list to the parent:
        fetchOptions.orderByFields = this.orderByFields;
      },
      deep: true
    },
    fieldsAvailable: {
      handler(fieldsAvailable) {
        localStorage.setItem('fieldsAvailable', JSON.stringify(fieldsAvailable))
      },
      deep: true
    },
  },
  computed: {
    orderByFields() {
      // Returns list of fields for Django's `order_by()` ORM method, in desired order and with
      // descending flag ("-") if necessary.
      let keys = [];
      this.fieldsSelected.forEach((item) => { keys.push(item.ascending ? item.sortField : '-' + item.sortField) });
      return keys;
    }
  },
  mounted() {
    // do stuff on mount, e.g. load some data from localStorage.
    let fieldsSelected = JSON.parse(localStorage.getItem('fieldsSelected'));
    if (fieldsSelected) {
      this.fieldsSelected = fieldsSelected;
    }

    let fieldsAvailable = JSON.parse(localStorage.getItem('fieldsAvailable'));
    if (fieldsAvailable) {
      this.fieldsAvailable = fieldsAvailable;
    }
  },
};
</script>

<style scoped>
.button-ascending {
  border: none;
  background-color: transparent;
  cursor: pointer;
  color: #747474;
}

.options-title {
  font-family: var(--font-family-condensed);
}

.drop-area {
  padding: 5px;
  margin: 0 0 5px 0;
  background-color: #e4e4e4;
  font-family: var(--font-family-condensed);
  font-weight: 300;
  border-radius: 3px;
}

.drop-item {
  cursor: grab;
}
</style>