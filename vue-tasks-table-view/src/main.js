import { createApp } from 'vue'
import App from './App.vue'

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

createApp(App).mount('#app')
