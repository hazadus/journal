(function(){"use strict";var e={6036:function(e,t,o){var l=o(9199);const a={key:0,class:"d-flex align-items-center"},s=(0,l.createElementVNode)("div",{class:"spinner-border text-primary me-3",role:"status"},[(0,l.createElementVNode)("span",{class:"visually-hidden"},"Loading...")],-1),n=(0,l.createElementVNode)("div",null," Идёт загрузка — пожалуйста, подождите! ",-1),c=[s,n];function i(e,t,o,s,n,i){const r=(0,l.resolveComponent)("TaskListTable");return n.tasksAll.length&&n.categoriesAll.length?n.categoriesAll.length?((0,l.openBlock)(),(0,l.createBlock)(r,{key:1,tasks:n.tasksAll,categories:n.categoriesAll,"default-fetch-options":n.fetchOptions,onFetchOptionsChanged:t[0]||(t[0]=e=>this.fetchOptions=e),onOrderChanged:t[1]||(t[1]=e=>this.orderByFields=e)},null,8,["tasks","categories","default-fetch-options"])):(0,l.createCommentVNode)("",!0):((0,l.openBlock)(),(0,l.createElementBlock)("div",a,c))}const r=e=>((0,l.pushScopeId)("data-v-3c0d9a24"),e=e(),(0,l.popScopeId)(),e),d={class:"alert alert-secondary"},m={class:"d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline m-0"},p={class:"btn-toolbar mb-2 mb-md-0"},h=r((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-gears"},null,-1))),u={key:0,class:"row mb-3 border-top pt-3 mt-3"},k={class:"col-6 col-lg-2"},f=r((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Фильтры",-1))),b=r((()=>(0,l.createElementVNode)("label",{for:"check-show-active",class:"options-checkbox-label"},"В работе",-1))),g=r((()=>(0,l.createElementVNode)("br",null,null,-1))),v=r((()=>(0,l.createElementVNode)("label",{for:"check-show-private",class:"options-checkbox-label"},"Личные",-1))),V=r((()=>(0,l.createElementVNode)("br",null,null,-1))),w=r((()=>(0,l.createElementVNode)("label",{for:"check-show-completed",class:"options-checkbox-label"},"Завершенные",-1))),N=r((()=>(0,l.createElementVNode)("br",null,null,-1))),y=r((()=>(0,l.createElementVNode)("label",{for:"check-show-favorite-only",class:"options-checkbox-label"},"Только избранные",-1))),E=r((()=>(0,l.createElementVNode)("br",null,null,-1))),C={class:"col-6 col-lg-2"},x=r((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Упорядочить",-1))),O={class:"col-6 col-lg-2"},S=r((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Отображение",-1))),B=r((()=>(0,l.createElementVNode)("label",{for:"check-auto-update",class:"options-checkbox-label"},"Автообновление",-1))),F=r((()=>(0,l.createElementVNode)("br",null,null,-1))),T=r((()=>(0,l.createElementVNode)("label",{for:"check-show-category",class:"options-checkbox-label"},"Категории",-1))),D=r((()=>(0,l.createElementVNode)("br",null,null,-1))),_=r((()=>(0,l.createElementVNode)("label",{for:"check-show-comments-count",class:"options-checkbox-label"},"Комментарии",-1))),A=r((()=>(0,l.createElementVNode)("br",null,null,-1))),I=r((()=>(0,l.createElementVNode)("label",{for:"check-show-created-date",class:"options-checkbox-label"},"Дата создания",-1))),U=r((()=>(0,l.createElementVNode)("br",null,null,-1))),j=r((()=>(0,l.createElementVNode)("label",{for:"check-show-completed-date",class:"options-checkbox-label"},"Дата завершения",-1))),M=r((()=>(0,l.createElementVNode)("br",null,null,-1))),J={class:"col-6 col-lg-6"},L=r((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Категории",-1))),P=["id","value"],R=["for","onClick"],q=r((()=>(0,l.createElementVNode)("br",null,null,-1))),$={class:"table-tasks-wrapper"},X={class:"table table-hover table-tasks text-nowrap"},Z=r((()=>(0,l.createElementVNode)("th",{scope:"col",class:"text-center",style:{width:"30px"}},[(0,l.createElementVNode)("i",{class:"fa-regular fa-star"})],-1))),K=r((()=>(0,l.createElementVNode)("th",{scope:"col",class:"text-center",style:{width:"30px"}},[(0,l.createElementVNode)("i",{class:"fa-regular fa-lock"})],-1))),z=r((()=>(0,l.createElementVNode)("th",null," Задача ",-1))),H={key:0,class:"table-column-date text-center"},W={key:1,class:"table-column-date text-center"},G={class:"cell-favorite"},Q={key:0,class:"fa-regular fa-star"},Y={class:"text-muted"},ee={key:0,class:"fa-regular fa-lock"},te={key:0,class:"task-completed-mark"},oe=r((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-check"},null,-1))),le=[oe],ae=["href"],se={key:1,class:"text-muted category-title"},ne=r((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-comments"},null,-1))),ce={key:0},ie={key:2,class:"ms-1"},re=["href"],de=r((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-paperclip"},null,-1))),me=[de],pe={key:3,class:"text-muted category-title"},he=r((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-tag"},null,-1))),ue={key:0,class:"table-column-date text-center"},ke={class:"text-muted category-title"},fe={key:1,class:"table-column-date text-center"},be={class:"text-muted category-title"};function ge(e,t,o,a,s,n){const c=(0,l.resolveComponent)("OrderBySelector");return(0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,null,[(0,l.createElementVNode)("div",d,[(0,l.createElementVNode)("div",m,[(0,l.createElementVNode)("h4",null," Всего задач: "+(0,l.toDisplayString)(this.tasks.length)+", отображается: "+(0,l.toDisplayString)(n.filteredTasks.length)+". ",1),(0,l.createElementVNode)("div",p,[(0,l.createElementVNode)("button",{class:"btn btn-sm btn-primary",onClick:t[0]||(t[0]=e=>s.viewOptions.showOptions=!s.viewOptions.showOptions)},[h,(0,l.createTextVNode)(" Настройки ")])])]),s.viewOptions.showOptions?((0,l.openBlock)(),(0,l.createElementBlock)("div",u,[(0,l.createElementVNode)("div",k,[f,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[1]||(t[1]=e=>s.tasksFilters.showActive=e),id:"check-show-active"},null,512),[[l.vModelCheckbox,s.tasksFilters.showActive]]),(0,l.createTextVNode)(),b,g,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[2]||(t[2]=e=>s.tasksFilters.showPrivate=e),id:"check-show-private"},null,512),[[l.vModelCheckbox,s.tasksFilters.showPrivate]]),(0,l.createTextVNode)(),v,V,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[3]||(t[3]=e=>s.tasksFilters.showCompleted=e),id:"check-show-completed"},null,512),[[l.vModelCheckbox,s.tasksFilters.showCompleted]]),(0,l.createTextVNode)(),w,N,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[4]||(t[4]=e=>s.tasksFilters.showFavoritesOnly=e),id:"check-show-favorite-only"},null,512),[[l.vModelCheckbox,s.tasksFilters.showFavoritesOnly]]),(0,l.createTextVNode)(),y,E]),(0,l.createElementVNode)("div",C,[x,(0,l.createVNode)(c,{onOrderChanged:t[5]||(t[5]=e=>this.orderByFields=e)})]),(0,l.createElementVNode)("div",O,[S,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[6]||(t[6]=e=>s.fetchOptions.autoUpdate=e),id:"check-auto-update"},null,512),[[l.vModelCheckbox,s.fetchOptions.autoUpdate]]),(0,l.createTextVNode)(),B,F,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[7]||(t[7]=e=>s.viewOptions.showCategory=e),id:"check-show-category"},null,512),[[l.vModelCheckbox,s.viewOptions.showCategory]]),(0,l.createTextVNode)(),T,D,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[8]||(t[8]=e=>s.viewOptions.showCommentsCount=e),id:"check-show-comments-count"},null,512),[[l.vModelCheckbox,s.viewOptions.showCommentsCount]]),(0,l.createTextVNode)(),_,A,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[9]||(t[9]=e=>s.viewOptions.showCreatedDate=e),id:"check-show-created-date"},null,512),[[l.vModelCheckbox,s.viewOptions.showCreatedDate]]),(0,l.createTextVNode)(),I,U,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[10]||(t[10]=e=>s.viewOptions.showCompletedDate=e),id:"check-show-completed-date"},null,512),[[l.vModelCheckbox,s.viewOptions.showCompletedDate]]),(0,l.createTextVNode)(),j,M]),(0,l.createElementVNode)("div",J,[L,((0,l.openBlock)(!0),(0,l.createElementBlock)(l.Fragment,null,(0,l.renderList)(this.categories,(e=>((0,l.openBlock)(),(0,l.createElementBlock)("span",{key:e.id,class:"category-checkbox-block"},[(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[11]||(t[11]=e=>s.categoriesVisibleIds=e),id:"category"+e.id,value:e.id},null,8,P),[[l.vModelCheckbox,s.categoriesVisibleIds]]),(0,l.createTextVNode)(),(0,l.createElementVNode)("label",{for:"category"+e.id,class:"options-checkbox-label",onClick:(0,l.withModifiers)((t=>s.categoriesVisibleIds=[e.id]),["alt","prevent"])},(0,l.toDisplayString)(e.title),9,R),q])))),128)),(0,l.createElementVNode)("button",{onClick:t[12]||(t[12]=e=>s.categoriesVisibleIds=[]),class:"btn btn-sm btn-primary me-1 mt-2"},"Убрать все"),(0,l.createElementVNode)("button",{onClick:t[13]||(t[13]=(...e)=>n.copyAllCategoryIdsToVisible&&n.copyAllCategoryIdsToVisible(...e)),class:"btn btn-sm btn-primary mt-2"},"Показать все")])])):(0,l.createCommentVNode)("",!0)]),(0,l.createElementVNode)("div",$,[(0,l.createElementVNode)("table",X,[(0,l.createElementVNode)("thead",null,[(0,l.createElementVNode)("tr",null,[Z,K,z,s.viewOptions.showCreatedDate?((0,l.openBlock)(),(0,l.createElementBlock)("th",H," Создана ")):(0,l.createCommentVNode)("",!0),s.viewOptions.showCompletedDate?((0,l.openBlock)(),(0,l.createElementBlock)("th",W," Завершена ")):(0,l.createCommentVNode)("",!0)])]),(0,l.createElementVNode)("tbody",null,[((0,l.openBlock)(!0),(0,l.createElementBlock)(l.Fragment,null,(0,l.renderList)(n.filteredTasks,(e=>((0,l.openBlock)(),(0,l.createElementBlock)("tr",{key:e.id,class:(0,l.normalizeClass)(e.is_acquainted?"":"table-success")},[(0,l.createElementVNode)("td",G,[e.is_favorite?((0,l.openBlock)(),(0,l.createElementBlock)("i",Q)):(0,l.createCommentVNode)("",!0)]),(0,l.createElementVNode)("td",Y,[e.is_private?((0,l.openBlock)(),(0,l.createElementBlock)("i",ee)):(0,l.createCommentVNode)("",!0)]),(0,l.createElementVNode)("td",null,[e.is_completed?((0,l.openBlock)(),(0,l.createElementBlock)("span",te,le)):(0,l.createCommentVNode)("",!0),(0,l.createElementVNode)("a",{href:`/journal/task/${e.id}/`,class:"task-title-link"},(0,l.toDisplayString)(e.title),9,ae),s.viewOptions.showCommentsCount?((0,l.openBlock)(),(0,l.createElementBlock)("span",se,[ne,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(e.comments_count),1),e.new_comments_count?((0,l.openBlock)(),(0,l.createElementBlock)("span",ce," · "+(0,l.toDisplayString)(e.new_comments_count),1)):(0,l.createCommentVNode)("",!0)])):(0,l.createCommentVNode)("",!0),e.attachment?((0,l.openBlock)(),(0,l.createElementBlock)("span",ie,[(0,l.createElementVNode)("a",{href:e.attachment,class:"text-muted"},me,8,re)])):(0,l.createCommentVNode)("",!0),s.viewOptions.showCategory?((0,l.openBlock)(),(0,l.createElementBlock)("span",pe,[he,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(e.category_title),1)])):(0,l.createCommentVNode)("",!0)]),s.viewOptions.showCreatedDate?((0,l.openBlock)(),(0,l.createElementBlock)("td",ue,[(0,l.createElementVNode)("span",ke,(0,l.toDisplayString)(n.formatDateTime(e.created)),1)])):(0,l.createCommentVNode)("",!0),s.viewOptions.showCompletedDate?((0,l.openBlock)(),(0,l.createElementBlock)("td",fe,[(0,l.createElementVNode)("span",be,(0,l.toDisplayString)(e.is_completed?n.formatDateTime(e.completed):""),1)])):(0,l.createCommentVNode)("",!0)],2)))),128))])])])],64)}o(7658);const ve=e=>((0,l.pushScopeId)("data-v-3a429529"),e=e(),(0,l.popScopeId)(),e),Ve=ve((()=>(0,l.createElementVNode)("h6",{class:"options-title"},"Сортировать по:",-1))),we={class:"drop-item"},Ne=["onClick"],ye=ve((()=>(0,l.createElementVNode)("h6",{class:"options-title"},"Доступные поля:",-1))),Ee={class:"drop-item"};function Ce(e,t,o,a,s,n){const c=(0,l.resolveComponent)("draggable");return(0,l.openBlock)(),(0,l.createElementBlock)("div",null,[(0,l.createElementVNode)("div",null,[Ve,(0,l.createVNode)(c,{list:s.fieldsSelected,itemKey:"id",group:"fields",class:"drop-area"},{item:(0,l.withCtx)((({element:e})=>[(0,l.createElementVNode)("div",we,[(0,l.createTextVNode)((0,l.toDisplayString)(e.name)+" ",1),(0,l.createElementVNode)("button",{class:"button-ascending",onClick:t=>e.ascending=!e.ascending},(0,l.toDisplayString)(e.ascending?"▲":"▼"),9,Ne)])])),_:1},8,["list"])]),(0,l.createElementVNode)("div",null,[ye,(0,l.createVNode)(c,{list:s.fieldsAvailable,itemKey:"id",group:"fields",class:"drop-area"},{item:(0,l.withCtx)((({element:e})=>[(0,l.createElementVNode)("div",Ee,(0,l.toDisplayString)(e.name),1)])),_:1},8,["list"])])])}var xe=o(6983),Oe=o.n(xe),Se={components:{draggable:Oe()},props:{orderBy:Array},emits:["orderChanged"],data(){return{fieldsSelected:[{name:"Новое",id:1,sortField:"is_acquainted",ascending:!0},{name:"Избранное",id:2,sortField:"is_favorite",ascending:!1},{name:"В работе",id:3,sortField:"is_completed",ascending:!0},{name:"Дата завершения",id:4,sortField:"completed",ascending:!1}],fieldsAvailable:[{name:"Дата создания",id:5,sortField:"created",ascending:!0},{name:"Личное",id:6,sortField:"is_private",ascending:!0}]}},watch:{fieldsSelected:{handler(e){localStorage.setItem("fieldsSelected",JSON.stringify(e)),this.$emit("orderChanged",this.orderByFields)},deep:!0},fieldsAvailable:{handler(e){localStorage.setItem("fieldsAvailable",JSON.stringify(e))},deep:!0}},computed:{orderByFields(){let e=[];return this.fieldsSelected.forEach((t=>{e.push(t.ascending?t.sortField:"-"+t.sortField)})),e}},mounted(){let e=JSON.parse(localStorage.getItem("fieldsSelected"));e&&(this.fieldsSelected=e);let t=JSON.parse(localStorage.getItem("fieldsAvailable"));t&&(this.fieldsAvailable=t)}},Be=o(89);const Fe=(0,Be.Z)(Se,[["render",Ce],["__scopeId","data-v-3a429529"]]);var Te=Fe,De={name:"TaskListTable",components:{OrderBySelector:Te},props:{tasks:Array,categories:Array,defaultFetchOptions:Object},emits:["fetchOptionsChanged","orderChanged"],data(){return{categoriesVisibleIds:[],orderByFields:[],tasksFilters:{showActive:!0,showCompleted:!1,showPrivate:!0,showFavoritesOnly:!1},viewOptions:{showOptions:!0,showCategory:!1,showCommentsCount:!0,showCreatedDate:!1,showCompletedDate:!1},fetchOptions:this.defaultFetchOptions}},watch:{categoriesVisibleIds:{handler(e){localStorage.setItem("categoriesVisibleIds",JSON.stringify(e))},deep:!0},orderByFields:{handler(){this.$emit("orderChanged",this.orderByFields)},deep:!0},viewOptions:{handler(e){localStorage.setItem("viewOptions",JSON.stringify(e))},deep:!0},tasksFilters:{handler(e){localStorage.setItem("tasksFilters",JSON.stringify(e))},deep:!0},fetchOptions:{handler(e){this.$emit("fetchOptionsChanged",e)},deep:!0}},computed:{filteredTasks(){let e=this.tasks;return this.tasksFilters.showCompleted||(e=e.filter((e=>!e.is_completed))),this.tasksFilters.showActive||(e=e.filter((e=>e.is_completed))),this.tasksFilters.showFavoritesOnly&&(e=e.filter((e=>e.is_favorite))),this.tasksFilters.showPrivate||(e=e.filter((e=>!e.is_private))),e=e.filter((e=>this.categoriesVisibleIds.includes(e.category))),e}},methods:{copyAllCategoryIdsToVisible(){for(let e=0;e<this.categories.length;e++)this.categoriesVisibleIds.push(this.categories[e].id)},formatDateTime(e){let t=new Date(e);return t.toLocaleDateString("ru-RU")+" "+t.toLocaleTimeString("ru-RU",{hour:"2-digit",minute:"2-digit"})}},mounted(){let e=JSON.parse(localStorage.getItem("viewOptions"));e&&(this.viewOptions=e);let t=JSON.parse(localStorage.getItem("tasksFilters"));t&&(this.tasksFilters=t);let o=localStorage.getItem("categoriesVisibleIds");null==o?this.copyAllCategoryIdsToVisible():this.categoriesVisibleIds=JSON.parse(o)}};const _e=(0,Be.Z)(De,[["render",ge],["__scopeId","data-v-3c0d9a24"]]);var Ae=_e,Ie={name:"App",components:{TaskListTable:Ae},data(){return{tasksAll:[],categoriesAll:[],orderByFields:[],fetchOptions:{autoUpdate:!0,pollDataTimeout:5e3},polling:null}},watch:{fetchOptions:{handler(e){localStorage.setItem("fetchOptions",JSON.stringify(e))},deep:!0},orderByFields:{handler(){this.fetchAllTasks()},deep:!0}},methods:{fetchAllCategories(){const e=window.location.origin+"/journal/tasks/api/v1/category_list/";return window.axios.get(e,{params:{}}).then((e=>(this.categoriesAll=e.data,e.data))).catch((function(e){throw console.log("Axios.get error:",e),e}))},fetchAllTasks(){const e=window.location.origin+"/journal/tasks/api/v1/task_list/";let t={orderByFields:this.orderByFields.toString()};return window.axios.get(e,{params:t}).then((e=>(this.tasksAll=e.data,e.data))).catch((function(e){throw console.log("Axios.get error:",e),e}))},pollData(){this.polling=setInterval((()=>{this.fetchOptions.autoUpdate&&this.fetchAllTasks()}),this.fetchOptions.pollDataTimeout)}},created(){this.fetchAllCategories(),this.fetchAllTasks(),this.pollData()},beforeUnmount(){clearInterval(this.polling)},mounted(){let e=JSON.parse(localStorage.getItem("fetchOptions"));e&&(this.fetchOptions=e)}};const Ue=(0,Be.Z)(Ie,[["render",i]]);var je=Ue;window.axios=o(7218),window.axios.defaults.headers.common["X-Requested-With"]="XMLHttpRequest";let Me=document.getElementsByName("csrfmiddlewaretoken");Me?window.axios.defaults.headers.common["X-CSRFToken"]=Me[0].value:console.error("CSRF token not found: https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax"),(0,l.createApp)(je).mount("#app")}},t={};function o(l){var a=t[l];if(void 0!==a)return a.exports;var s=t[l]={exports:{}};return e[l].call(s.exports,s,s.exports,o),s.exports}o.m=e,function(){var e=[];o.O=function(t,l,a,s){if(!l){var n=1/0;for(d=0;d<e.length;d++){l=e[d][0],a=e[d][1],s=e[d][2];for(var c=!0,i=0;i<l.length;i++)(!1&s||n>=s)&&Object.keys(o.O).every((function(e){return o.O[e](l[i])}))?l.splice(i--,1):(c=!1,s<n&&(n=s));if(c){e.splice(d--,1);var r=a();void 0!==r&&(t=r)}}return t}s=s||0;for(var d=e.length;d>0&&e[d-1][2]>s;d--)e[d]=e[d-1];e[d]=[l,a,s]}}(),function(){o.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return o.d(t,{a:t}),t}}(),function(){o.d=function(e,t){for(var l in t)o.o(t,l)&&!o.o(e,l)&&Object.defineProperty(e,l,{enumerable:!0,get:t[l]})}}(),function(){o.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){o.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){var e={143:0};o.O.j=function(t){return 0===e[t]};var t=function(t,l){var a,s,n=l[0],c=l[1],i=l[2],r=0;if(n.some((function(t){return 0!==e[t]}))){for(a in c)o.o(c,a)&&(o.m[a]=c[a]);if(i)var d=i(o)}for(t&&t(l);r<n.length;r++)s=n[r],o.o(e,s)&&e[s]&&e[s][0](),e[s]=0;return o.O(d)},l=self["webpackChunkvue_tasks_table_view"]=self["webpackChunkvue_tasks_table_view"]||[];l.forEach(t.bind(null,0)),l.push=t.bind(null,l.push.bind(l))}();var l=o.O(void 0,[998],(function(){return o(6036)}));l=o.O(l)})();
//# sourceMappingURL=app.js.map