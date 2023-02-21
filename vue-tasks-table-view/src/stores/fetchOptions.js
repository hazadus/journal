import { reactive } from 'vue';

export const fetchOptions = reactive({
  autoUpdate: true,         // re-fetch data from backend from time to time
  pollDataTimeout: 12000,    // update period, ms
  orderByFields: [],

  set(newOptions) {
    this.autoUpdate = newOptions.autoUpdate;
    this.pollDataTimeout = newOptions.pollDataTimeout;
    this.orderByFields = newOptions.orderByFields;
  }
})