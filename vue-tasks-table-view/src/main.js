import { createApp } from 'vue';
import App from './App.vue';
import * as Sentry from "@sentry/vue";

/**
 * We'll load the axios HTTP library which allows us to easily issue requests
 * to our Django back-end. This library automatically handles sending the
 * CSRF token as a header based on the value of the "XSRF" token cookie.
 */

window.axios = require('axios');
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

/**
 * Next we will register the CSRF Token as a common header with Axios so that
 * all outgoing HTTP requests automatically have it attached. This is just
 * a simple convenience so we don't have to attach every token manually.
 */

let token = document.getElementsByName("csrfmiddlewaretoken");

if (token) {
  window.axios.defaults.headers.common['X-CSRFToken'] = token[0].value;
} else {
  console.error('CSRF token not found: https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax');
}

// Add markdown as global
import {marked} from 'marked';
import * as DOMPurify from 'dompurify';

marked.setOptions({
  breaks: true,
});

// Can be accessed anywhere in the components as `this.markdown`, `this.sanitizeHtml`.
const markedMixin = {
  methods: {
    markdown: function (input) {
      // Return marked down & sanitized input as raw HTML
      return DOMPurify.sanitize(marked(input));
    },
    sanitizeHtml: function (input) {
      // Return sanitized input
      return DOMPurify.sanitize(input);
    },
  },
};

const app = createApp(App);

Sentry.init({
  app,
  dsn: "https://f34f0f582dfa429e868907665de40a62@o1402378.ingest.sentry.io/4504825355698176",
  tracesSampleRate: 0.1,
});

app.mixin(markedMixin);
app.mount('#dashboard-page-content');
