(function(){"use strict";var e={1714:function(e,t,o){var l=o(9199);const a={class:"d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline pt-3 pb-2 mb-3 border-bottom"},s=(0,l.createElementVNode)("h1",{class:"h2"}," Задачи: табличный вид (Vue) ",-1),n={class:"btn-toolbar mb-2 mb-md-0"},c=(0,l.createElementVNode)("i",{class:"fa-solid fa-columns"},null,-1),i=(0,l.createElementVNode)("i",{class:"fa-solid fa-table"},null,-1),r=(0,l.createElementVNode)("i",{class:"fa-solid fa-gears"},null,-1),d=(0,l.createElementVNode)("a",{class:"btn btn-sm btn-success",href:"/journal/task/create/"},[(0,l.createElementVNode)("i",{class:"fa-solid fa-file-circle-plus"}),(0,l.createTextVNode)(" Добавить задачу ")],-1),m={key:0,class:"d-flex align-items-center"},p=(0,l.createElementVNode)("div",{class:"spinner-border text-primary me-3",role:"status"},[(0,l.createElementVNode)("span",{class:"visually-hidden"},"Loading...")],-1),h=(0,l.createElementVNode)("div",null," Идёт загрузка — пожалуйста, подождите! ",-1),u=[p,h];function k(e,t,o,p,h,k){const f=(0,l.resolveComponent)("TaskListTable"),v=(0,l.resolveComponent)("TaskListSidebar");return(0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,null,[(0,l.createElementVNode)("div",a,[s,(0,l.createElementVNode)("div",n,[(0,l.createElementVNode)("button",{onClick:t[0]||(t[0]=e=>h.viewOptions.isTableView=!h.viewOptions.isTableView),class:"btn btn-sm btn-warning me-1"},[h.viewOptions.isTableView?((0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,{key:0},[c,(0,l.createTextVNode)(" Колонки ")],64)):((0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,{key:1},[i,(0,l.createTextVNode)(" Таблица ")],64))]),(0,l.createElementVNode)("button",{class:"btn btn-sm btn-primary me-1",onClick:t[1]||(t[1]=e=>h.viewOptions.showOptions=!h.viewOptions.showOptions)},[r,(0,l.createTextVNode)(" Настройки ")]),d])]),h.tasksAll.length&&h.categoriesAll.length?((0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,{key:1},[h.viewOptions.isTableView?((0,l.openBlock)(),(0,l.createBlock)(f,{key:0,tasks:h.tasksAll,"filtered-tasks":k.filteredTasks,categories:h.categoriesAll},null,8,["tasks","filtered-tasks","categories"])):((0,l.openBlock)(),(0,l.createBlock)(v,{key:1,tasks:h.tasksAll,"filtered-tasks":k.filteredTasks,categories:h.categoriesAll},null,8,["tasks","filtered-tasks","categories"]))],64)):((0,l.openBlock)(),(0,l.createElementBlock)("div",m,u))],64)}const f=e=>((0,l.pushScopeId)("data-v-ff23b848"),e=e(),(0,l.popScopeId)(),e),v={class:"alert alert-secondary"},g={class:"d-flex justify-content-between flex-wrap flex-md-nowrap align-items-baseline m-0"},b={class:"table-tasks-wrapper"},V={class:"table table-hover table-tasks text-nowrap"},w=f((()=>(0,l.createElementVNode)("th",{scope:"col",class:"text-center",style:{width:"30px"}},[(0,l.createElementVNode)("i",{class:"fa-regular fa-star"})],-1))),N=f((()=>(0,l.createElementVNode)("th",{scope:"col",class:"text-center",style:{width:"30px"}},[(0,l.createElementVNode)("i",{class:"fa-regular fa-lock"})],-1))),E=f((()=>(0,l.createElementVNode)("th",null," Задача ",-1))),y={key:0,class:"table-column-date text-center"},x={key:1,class:"table-column-date text-center"},C={class:"cell-favorite"},B={key:0,class:"fa-regular fa-star"},O={class:"text-muted"},S={key:0,class:"fa-regular fa-lock"},_={key:0,class:"task-completed-mark"},T=f((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-check"},null,-1))),D=[T],I=["href"],F={key:1,class:"text-muted category-title"},A=f((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-comments"},null,-1))),U={key:0},j={key:2,class:"ms-1"},L=["href"],M=f((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-paperclip"},null,-1))),P=[M],J={key:3,class:"text-muted category-title"},R=f((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-tag"},null,-1))),Z={key:0,class:"table-column-date text-center"},$={class:"text-muted category-title"},q={key:1,class:"table-column-date text-center"},H={class:"text-muted category-title"};function X(e,t,o,a,s,n){const c=(0,l.resolveComponent)("OptionsPanel");return(0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,null,[(0,l.createElementVNode)("div",v,[(0,l.createElementVNode)("div",g,[(0,l.createElementVNode)("h4",null," Всего задач: "+(0,l.toDisplayString)(this.tasks.length)+", отображается: "+(0,l.toDisplayString)(o.filteredTasks.length)+". ",1)]),s.viewOptions.showOptions?((0,l.openBlock)(),(0,l.createBlock)(c,{key:0,categories:o.categories},null,8,["categories"])):(0,l.createCommentVNode)("",!0)]),(0,l.createElementVNode)("div",b,[(0,l.createElementVNode)("table",V,[(0,l.createElementVNode)("thead",null,[(0,l.createElementVNode)("tr",null,[w,N,E,s.viewOptions.showCreatedDate?((0,l.openBlock)(),(0,l.createElementBlock)("th",y," Создана ")):(0,l.createCommentVNode)("",!0),s.viewOptions.showCompletedDate?((0,l.openBlock)(),(0,l.createElementBlock)("th",x," Завершена ")):(0,l.createCommentVNode)("",!0)])]),(0,l.createElementVNode)("tbody",null,[((0,l.openBlock)(!0),(0,l.createElementBlock)(l.Fragment,null,(0,l.renderList)(o.filteredTasks,(e=>((0,l.openBlock)(),(0,l.createElementBlock)("tr",{key:e.id,class:(0,l.normalizeClass)(e.is_acquainted?"":"table-success")},[(0,l.createElementVNode)("td",C,[e.is_favorite?((0,l.openBlock)(),(0,l.createElementBlock)("i",B)):(0,l.createCommentVNode)("",!0)]),(0,l.createElementVNode)("td",O,[e.is_private?((0,l.openBlock)(),(0,l.createElementBlock)("i",S)):(0,l.createCommentVNode)("",!0)]),(0,l.createElementVNode)("td",null,[e.is_completed?((0,l.openBlock)(),(0,l.createElementBlock)("span",_,D)):(0,l.createCommentVNode)("",!0),(0,l.createElementVNode)("a",{href:`/journal/task/${e.id}/`,class:"task-title-link"},(0,l.toDisplayString)(e.title),9,I),s.viewOptions.showCommentsCount?((0,l.openBlock)(),(0,l.createElementBlock)("span",F,[A,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(e.comments_count),1),e.new_comments_count?((0,l.openBlock)(),(0,l.createElementBlock)("span",U," · "+(0,l.toDisplayString)(e.new_comments_count),1)):(0,l.createCommentVNode)("",!0)])):(0,l.createCommentVNode)("",!0),e.attachment?((0,l.openBlock)(),(0,l.createElementBlock)("span",j,[(0,l.createElementVNode)("a",{href:e.attachment,class:"text-muted"},P,8,L)])):(0,l.createCommentVNode)("",!0),s.viewOptions.showCategory?((0,l.openBlock)(),(0,l.createElementBlock)("span",J,[R,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(e.category_title),1)])):(0,l.createCommentVNode)("",!0)]),s.viewOptions.showCreatedDate?((0,l.openBlock)(),(0,l.createElementBlock)("td",Z,[(0,l.createElementVNode)("span",$,(0,l.toDisplayString)(n.useFormatDateTime(e.created)),1)])):(0,l.createCommentVNode)("",!0),s.viewOptions.showCompletedDate?((0,l.openBlock)(),(0,l.createElementBlock)("td",q,[(0,l.createElementVNode)("span",H,(0,l.toDisplayString)(e.is_completed?n.useFormatDateTime(e.completed):""),1)])):(0,l.createCommentVNode)("",!0)],2)))),128))])])])],64)}const z=e=>((0,l.pushScopeId)("data-v-47fa4222"),e=e(),(0,l.popScopeId)(),e),K={class:"row mb-3 border-top pt-3 mt-3"},W={class:"col-6 col-lg-2"},G=z((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Фильтры",-1))),Q=z((()=>(0,l.createElementVNode)("label",{for:"check-show-active",class:"options-checkbox-label"},"В работе",-1))),Y=z((()=>(0,l.createElementVNode)("br",null,null,-1))),ee=z((()=>(0,l.createElementVNode)("label",{for:"check-show-private",class:"options-checkbox-label"},"Личные",-1))),te=z((()=>(0,l.createElementVNode)("br",null,null,-1))),oe=z((()=>(0,l.createElementVNode)("label",{for:"check-show-completed",class:"options-checkbox-label"},"Завершенные",-1))),le=z((()=>(0,l.createElementVNode)("br",null,null,-1))),ae=z((()=>(0,l.createElementVNode)("label",{for:"check-show-favorite-only",class:"options-checkbox-label"},"Только избранные",-1))),se=z((()=>(0,l.createElementVNode)("br",null,null,-1))),ne={class:"col-6 col-lg-2"},ce=z((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Упорядочить",-1))),ie={class:"col-6 col-lg-2"},re=z((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Отображение",-1))),de=z((()=>(0,l.createElementVNode)("label",{for:"check-auto-update",class:"options-checkbox-label"},"Автообновление",-1))),me=z((()=>(0,l.createElementVNode)("br",null,null,-1))),pe=z((()=>(0,l.createElementVNode)("label",{for:"check-show-category",class:"options-checkbox-label"},"Категории",-1))),he=z((()=>(0,l.createElementVNode)("br",null,null,-1))),ue=z((()=>(0,l.createElementVNode)("label",{for:"check-show-comments-count",class:"options-checkbox-label"},"Комментарии",-1))),ke=z((()=>(0,l.createElementVNode)("br",null,null,-1))),fe=z((()=>(0,l.createElementVNode)("label",{for:"check-show-created-date",class:"options-checkbox-label"},"Дата создания",-1))),ve=z((()=>(0,l.createElementVNode)("br",null,null,-1))),ge=z((()=>(0,l.createElementVNode)("label",{for:"check-show-completed-date",class:"options-checkbox-label"},"Дата завершения",-1))),be=z((()=>(0,l.createElementVNode)("br",null,null,-1))),Ve={class:"col-6 col-lg-6"},we=z((()=>(0,l.createElementVNode)("h5",{class:"options-title mb-1 pb-1 border-bottom"},"Категории",-1))),Ne=["id","value"],Ee=["for","onClick"],ye=z((()=>(0,l.createElementVNode)("br",null,null,-1))),xe=z((()=>(0,l.createElementVNode)("br",null,null,-1)));function Ce(e,t,o,a,s,n){const c=(0,l.resolveComponent)("OrderBySelector");return(0,l.openBlock)(),(0,l.createElementBlock)("div",K,[(0,l.createElementVNode)("div",W,[G,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[0]||(t[0]=e=>s.taskFilters.showActive=e),id:"check-show-active"},null,512),[[l.vModelCheckbox,s.taskFilters.showActive]]),(0,l.createTextVNode)(),Q,Y,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[1]||(t[1]=e=>s.taskFilters.showPrivate=e),id:"check-show-private"},null,512),[[l.vModelCheckbox,s.taskFilters.showPrivate]]),(0,l.createTextVNode)(),ee,te,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[2]||(t[2]=e=>s.taskFilters.showCompleted=e),id:"check-show-completed"},null,512),[[l.vModelCheckbox,s.taskFilters.showCompleted]]),(0,l.createTextVNode)(),oe,le,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[3]||(t[3]=e=>s.taskFilters.showFavoritesOnly=e),id:"check-show-favorite-only"},null,512),[[l.vModelCheckbox,s.taskFilters.showFavoritesOnly]]),(0,l.createTextVNode)(),ae,se]),(0,l.createElementVNode)("div",ne,[ce,(0,l.createVNode)(c)]),(0,l.createElementVNode)("div",ie,[re,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[4]||(t[4]=e=>s.fetchOptions.autoUpdate=e),id:"check-auto-update"},null,512),[[l.vModelCheckbox,s.fetchOptions.autoUpdate]]),(0,l.createTextVNode)(),de,me,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[5]||(t[5]=e=>s.viewOptions.showCategory=e),id:"check-show-category"},null,512),[[l.vModelCheckbox,s.viewOptions.showCategory]]),(0,l.createTextVNode)(),pe,he,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[6]||(t[6]=e=>s.viewOptions.showCommentsCount=e),id:"check-show-comments-count"},null,512),[[l.vModelCheckbox,s.viewOptions.showCommentsCount]]),(0,l.createTextVNode)(),ue,ke,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[7]||(t[7]=e=>s.viewOptions.showCreatedDate=e),id:"check-show-created-date"},null,512),[[l.vModelCheckbox,s.viewOptions.showCreatedDate]]),(0,l.createTextVNode)(),fe,ve,(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[8]||(t[8]=e=>s.viewOptions.showCompletedDate=e),id:"check-show-completed-date"},null,512),[[l.vModelCheckbox,s.viewOptions.showCompletedDate]]),(0,l.createTextVNode)(),ge,be]),(0,l.createElementVNode)("div",Ve,[we,((0,l.openBlock)(!0),(0,l.createElementBlock)(l.Fragment,null,(0,l.renderList)(this.categories,(e=>((0,l.openBlock)(),(0,l.createElementBlock)("span",{key:e.id,class:"category-checkbox-block"},[(0,l.withDirectives)((0,l.createElementVNode)("input",{type:"checkbox","onUpdate:modelValue":t[9]||(t[9]=e=>s.viewOptions.categoriesVisibleIds=e),id:"category"+e.id,value:e.id},null,8,Ne),[[l.vModelCheckbox,s.viewOptions.categoriesVisibleIds]]),(0,l.createTextVNode)(),(0,l.createElementVNode)("label",{for:"category"+e.id,class:"options-checkbox-label",onClick:(0,l.withModifiers)((t=>s.viewOptions.categoriesVisibleIds=[e.id]),["alt","prevent"])},(0,l.toDisplayString)(e.title),9,Ee),ye])))),128)),(0,l.createElementVNode)("button",{onClick:t[10]||(t[10]=e=>s.viewOptions.categoriesVisibleIds=[]),class:"btn btn-sm btn-primary me-1 mt-2"},"Убрать все"),(0,l.createElementVNode)("button",{onClick:t[11]||(t[11]=e=>s.viewOptions.copyAllCategoryIdsToVisible(o.categories)),class:"btn btn-sm btn-primary mt-2"},"Показать все"),xe])])}const Be=e=>((0,l.pushScopeId)("data-v-7144e0fa"),e=e(),(0,l.popScopeId)(),e),Oe=Be((()=>(0,l.createElementVNode)("h6",{class:"options-title"},"Сортировать по:",-1))),Se={class:"drop-item"},_e=["onClick"],Te=Be((()=>(0,l.createElementVNode)("h6",{class:"options-title"},"Доступные поля:",-1))),De={class:"drop-item"};function Ie(e,t,o,a,s,n){const c=(0,l.resolveComponent)("draggable");return(0,l.openBlock)(),(0,l.createElementBlock)("div",null,[(0,l.createElementVNode)("div",null,[Oe,(0,l.createVNode)(c,{list:s.fieldsSelected,itemKey:"id",group:"fields",class:"drop-area"},{item:(0,l.withCtx)((({element:e})=>[(0,l.createElementVNode)("div",Se,[(0,l.createTextVNode)((0,l.toDisplayString)(e.name)+" ",1),(0,l.createElementVNode)("button",{class:"button-ascending",onClick:t=>e.ascending=!e.ascending},(0,l.toDisplayString)(e.ascending?"▲":"▼"),9,_e)])])),_:1},8,["list"])]),(0,l.createElementVNode)("div",null,[Te,(0,l.createVNode)(c,{list:s.fieldsAvailable,itemKey:"id",group:"fields",class:"drop-area"},{item:(0,l.withCtx)((({element:e})=>[(0,l.createElementVNode)("div",De,(0,l.toDisplayString)(e.name),1)])),_:1},8,["list"])])])}o(7658);var Fe=o(6983),Ae=o.n(Fe);const Ue=(0,l.reactive)({autoUpdate:!0,pollDataTimeout:5e3,orderByFields:[],set(e){this.autoUpdate=e.autoUpdate,this.pollDataTimeout=e.pollDataTimeout,this.orderByFields=e.orderByFields}});var je={components:{draggable:Ae()},props:{},data(){return{fetchOptions:Ue,fieldsSelected:[{name:"Новое",id:1,sortField:"is_acquainted",ascending:!0},{name:"Избранное",id:2,sortField:"is_favorite",ascending:!1},{name:"В работе",id:3,sortField:"is_completed",ascending:!0},{name:"Дата завершения",id:4,sortField:"completed",ascending:!1}],fieldsAvailable:[{name:"Дата создания",id:5,sortField:"created",ascending:!0},{name:"Личное",id:6,sortField:"is_private",ascending:!0}]}},watch:{fieldsSelected:{handler(e){localStorage.setItem("fieldsSelected",JSON.stringify(e)),Ue.orderByFields=this.orderByFields},deep:!0},fieldsAvailable:{handler(e){localStorage.setItem("fieldsAvailable",JSON.stringify(e))},deep:!0}},computed:{orderByFields(){let e=[];return this.fieldsSelected.forEach((t=>{e.push(t.ascending?t.sortField:"-"+t.sortField)})),e}},mounted(){let e=JSON.parse(localStorage.getItem("fieldsSelected"));e&&(this.fieldsSelected=e);let t=JSON.parse(localStorage.getItem("fieldsAvailable"));t&&(this.fieldsAvailable=t)}},Le=o(89);const Me=(0,Le.Z)(je,[["render",Ie],["__scopeId","data-v-7144e0fa"]]);var Pe=Me;const Je=(0,l.reactive)({showActive:!0,showCompleted:!1,showPrivate:!0,showFavoritesOnly:!1,set(e){this.showActive=e.showActive,this.showCompleted=e.showCompleted,this.showPrivate=e.showPrivate,this.showFavoritesOnly=e.showFavoritesOnly}}),Re=(0,l.reactive)({isTableView:!0,showOptions:!0,showCategory:!1,showCommentsCount:!0,showCreatedDate:!1,showCompletedDate:!1,categoriesVisibleIds:[],set(e){this.isTableView=e.isTableView,this.showOptions=e.showOptions,this.showCategory=e.showCategory,this.showCommentsCount=e.showCommentsCount,this.showCreatedDate=e.showCreatedDate,this.showCompletedDate=e.showCompletedDate,this.categoriesVisibleIds=e.categoriesVisibleIds},copyAllCategoryIdsToVisible(e){this.categoriesVisibleIds=[];for(let t=0;t<e.length;t++)this.categoriesVisibleIds.push(e[t].id)}});var Ze={name:"OptionsPanel",components:{OrderBySelector:Pe},props:{categories:Array},data(){return{fetchOptions:Ue,taskFilters:Je,viewOptions:Re}}};const $e=(0,Le.Z)(Ze,[["render",Ce],["__scopeId","data-v-47fa4222"]]);var qe=$e;function He(e){let t=new Date(e);return t.toLocaleDateString("ru-RU")+" "+t.toLocaleTimeString("ru-RU",{hour:"2-digit",minute:"2-digit"})}function Xe(e){return e.author_avatar_url?"/media/"+e.author_avatar_url:"/static/images/default_profile_pic.png"}function ze(e){return`${e.author_last_name} ${e.author_first_name.slice(0,1)}.${e.author_second_name.slice(0,1)}.`}var Ke={name:"TaskListTable",components:{OptionsPanel:qe},props:{tasks:Array,filteredTasks:Array,categories:Array},data(){return{viewOptions:Re}},methods:{useFormatDateTime:He}};const We=(0,Le.Z)(Ke,[["render",X],["__scopeId","data-v-ff23b848"]]);var Ge=We;const Qe=e=>((0,l.pushScopeId)("data-v-79bee03e"),e=e(),(0,l.popScopeId)(),e),Ye={class:"component"},et={class:"tasks"},tt={class:"d-flex align-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom"},ot={class:"",style:{"flex-grow":"1"}},lt={class:"task-list list-group list-group-flush"},at=["onClick"],st={class:"d-flex w-100 align-items-center justify-content-between"},nt={class:"mb-1"},ct={key:0,class:"fa-regular fa-star"},it={key:1,class:"fa-regular fa-lock"},rt={class:"col-10 mb-1 small"},dt={key:0,class:"alert alert-secondary flex-grow-1 m-1"},mt={key:1,class:"task-detail"},pt={key:0},ht={class:"card mb-2"},ut={class:"card-header text-muted"},kt={class:"d-flex flex-wrap flex-md-nowrap align-items-center"},ft={class:"flex-grow-1"},vt={key:0,class:"fa-solid fa-lock me-1"},gt=Qe((()=>(0,l.createElementVNode)("i",{class:"fa-regular fa-calendar"},null,-1))),bt=Qe((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-user"},null,-1))),Vt=Qe((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-calendar-check"},null,-1))),wt={class:"card-body task-card-body"},Nt=["innerHTML"],Et={key:0,class:"mt-3"},yt=Qe((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-paperclip"},null,-1))),xt=["href"],Ct=Qe((()=>(0,l.createElementVNode)("h4",null," Комментарии ",-1))),Bt={class:"timeline"},Ot=Qe((()=>(0,l.createElementVNode)("div",{class:"timeline__line"},null,-1))),St={class:"timeline__items"},_t={class:"timeline__top mb-2"},Tt=Qe((()=>(0,l.createElementVNode)("div",{class:"timeline__circle text-center"},[(0,l.createElementVNode)("i",{class:"fa-solid fa-comment"})],-1))),Dt=["id"],It={class:"timeline__desc_avatar"},Ft={class:"d-flex"},At={class:"timeline__desc_avatar__avatar mt-3 me-2"},Ut=["src"],jt={class:"card flex-grow-1"},Lt={class:"card-header d-flex text-muted"},Mt={class:"flex-grow-1"},Pt=Qe((()=>(0,l.createElementVNode)("i",{class:"fa-solid fa-user"},null,-1))),Jt=["id"];function Rt(e,t,o,a,s,n){const c=(0,l.resolveComponent)("OptionsPanel");return(0,l.openBlock)(),(0,l.createElementBlock)("div",Ye,[(0,l.createElementVNode)("div",et,[(0,l.createElementVNode)("div",tt,[(0,l.createElementVNode)("div",ot," Задач: "+(0,l.toDisplayString)(o.filteredTasks.length)+" / "+(0,l.toDisplayString)(o.tasks.length),1)]),(0,l.createElementVNode)("div",lt,[((0,l.openBlock)(!0),(0,l.createElementBlock)(l.Fragment,null,(0,l.renderList)(this.filteredTasks,(e=>((0,l.openBlock)(),(0,l.createElementBlock)("a",{key:e.id,href:"#",onClick:t=>this.selectedItem=e,class:(0,l.normalizeClass)(["task-list-item list-group-item list-group-item-action py-3 lh-sm",{active:s.selectedItem&&s.selectedItem.id===e.id}])},[(0,l.createElementVNode)("div",st,[(0,l.createElementVNode)("strong",nt,(0,l.toDisplayString)(e.title),1),e.is_favorite?((0,l.openBlock)(),(0,l.createElementBlock)("i",ct)):(0,l.createCommentVNode)("",!0),e.is_private?((0,l.openBlock)(),(0,l.createElementBlock)("i",it)):(0,l.createCommentVNode)("",!0)]),(0,l.createElementVNode)("div",rt,(0,l.toDisplayString)(e.category_title),1)],10,at)))),128))])]),s.viewOptions.showOptions?((0,l.openBlock)(),(0,l.createElementBlock)("div",dt,[(0,l.createVNode)(c,{categories:o.categories},null,8,["categories"])])):((0,l.openBlock)(),(0,l.createElementBlock)("div",mt,[s.selectedItem?((0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,{key:1},[s.detailItem?((0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,{key:0},[(0,l.createElementVNode)("h3",null,(0,l.toDisplayString)(s.detailItem.title),1),(0,l.createElementVNode)("div",ht,[(0,l.createElementVNode)("div",ut,[(0,l.createElementVNode)("div",kt,[(0,l.createElementVNode)("div",ft,[s.detailItem.is_private?((0,l.openBlock)(),(0,l.createElementBlock)("i",vt)):(0,l.createCommentVNode)("",!0),gt,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(n.useFormatDateTime(s.detailItem.created))+" · ",1),bt,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(n.useAuthorShortName(s.detailItem))+" ",1),s.detailItem.is_completed?((0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,{key:1},[(0,l.createTextVNode)(" · "),Vt,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(n.useFormatDateTime(s.detailItem.completed)),1)],64)):(0,l.createCommentVNode)("",!0)])])]),(0,l.createElementVNode)("div",wt,[(0,l.createElementVNode)("span",{innerHTML:s.detailItem.body},null,8,Nt),s.detailItem.attachment?((0,l.openBlock)(),(0,l.createElementBlock)("p",Et,[yt,(0,l.createTextVNode)(" Файл: "),(0,l.createElementVNode)("a",{href:s.detailItem.attachment},(0,l.toDisplayString)(s.detailItem.attachment),9,xt)])):(0,l.createCommentVNode)("",!0)])]),s.comments?((0,l.openBlock)(),(0,l.createElementBlock)(l.Fragment,{key:0},[Ct,(0,l.createElementVNode)("div",Bt,[Ot,(0,l.createElementVNode)("div",St,[((0,l.openBlock)(!0),(0,l.createElementBlock)(l.Fragment,null,(0,l.renderList)(s.comments,(e=>((0,l.openBlock)(),(0,l.createElementBlock)("div",{key:e.id,class:"timeline__item mb-3"},[(0,l.createElementVNode)("div",_t,[Tt,(0,l.createElementVNode)("div",{class:"timeline__title",id:"comment-"+e.id}," Добавлен комментарий: ",8,Dt)]),(0,l.createElementVNode)("div",It,[(0,l.createElementVNode)("div",Ft,[(0,l.createElementVNode)("div",At,[(0,l.createElementVNode)("img",{src:n.useAuthorAvatarURL(e),width:"48",height:"48",class:"rounded-circle",alt:"User picture"},null,8,Ut)]),(0,l.createElementVNode)("div",jt,[(0,l.createElementVNode)("div",Lt,[(0,l.createElementVNode)("div",Mt,[Pt,(0,l.createTextVNode)(" "+(0,l.toDisplayString)(n.useAuthorShortName(e))+", "+(0,l.toDisplayString)(n.useFormatDateTime(e.created)),1)])]),(0,l.createElementVNode)("div",{class:"card-body",id:"comment-body-"+e.id},(0,l.toDisplayString)(e.body)+" ",9,Jt)])])])])))),128))])])],64)):(0,l.createCommentVNode)("",!0)],64)):(0,l.createCommentVNode)("",!0)],64)):((0,l.openBlock)(),(0,l.createElementBlock)("span",pt," Выберите задачу слева "))]))])}var Zt={name:"TaskListSidebar",components:{OptionsPanel:qe},props:{tasks:Array,filteredTasks:Array,categories:Array},data(){return{viewOptions:Re,selectedItem:null,detailItem:null,comments:null}},methods:{useFormatDateTime:He,useAuthorAvatarURL:Xe,useAuthorShortName:ze,fetchSelectedTask(){const e=`/journal/tasks/api/v1/task/${this.selectedItem.id}/`;return window.axios.get(e,{}).then((e=>(this.detailItem=e.data,e.data))).catch((function(e){throw console.log("Axios.get error:",e),e}))},fetchSelectedTaskComments(){const e="/journal/tasks/api/v1/comment_list/";return window.axios.get(e,{params:{taskId:this.selectedItem.id}}).then((e=>(this.comments=e.data,e.data))).catch((function(e){throw console.log("Axios.get error:",e),e}))}},watch:{selectedItem:{handler(){this.fetchSelectedTask(),this.fetchSelectedTaskComments()}}},mounted(){this.selectedItem||this.tasks.length&&(this.selectedItem=this.tasks[0])}};const $t=(0,Le.Z)(Zt,[["render",Rt],["__scopeId","data-v-79bee03e"]]);var qt=$t,Ht={name:"App",components:{TaskListTable:Ge,TaskListSidebar:qt},data(){return{fetchOptions:Ue,taskFilters:Je,viewOptions:Re,tasksAll:[],categoriesAll:[],polling:null}},computed:{filteredTasks(){let e=this.tasksAll;return Je.showCompleted||(e=e.filter((e=>!e.is_completed))),Je.showActive||(e=e.filter((e=>e.is_completed))),Je.showFavoritesOnly&&(e=e.filter((e=>e.is_favorite))),Je.showPrivate||(e=e.filter((e=>!e.is_private))),e=e.filter((e=>Re.categoriesVisibleIds.includes(e.category))),e}},watch:{fetchOptions:{handler(e){localStorage.setItem("fetchOptions",JSON.stringify(e)),this.fetchAllTasks()},deep:!0},viewOptions:{handler(e){localStorage.setItem("viewOptions",JSON.stringify(e))},deep:!0},taskFilters:{handler(e){localStorage.setItem("taskFilters",JSON.stringify(e))},deep:!0}},methods:{fetchAllCategories(){const e=window.location.origin+"/journal/tasks/api/v1/category_list/";return window.axios.get(e,{params:{}}).then((e=>{this.categoriesAll=e.data;let t=JSON.parse(localStorage.getItem("viewOptions"));return t&&Re.set(t),null==Re.categoriesVisibleIds&&Re.copyAllCategoryIdsToVisible(this.categoriesAll),e.data})).catch((function(e){throw console.log("Axios.get error:",e),e}))},fetchAllTasks(){const e=window.location.origin+"/journal/tasks/api/v1/task_list/";let t={orderByFields:Ue.orderByFields.toString()};return window.axios.get(e,{params:t}).then((e=>(this.tasksAll=e.data,e.data))).catch((function(e){throw console.log("Axios.get error:",e),e}))},pollData(){this.polling=setInterval((()=>{Ue.autoUpdate&&this.fetchAllTasks()}),Ue.pollDataTimeout)}},created(){this.fetchAllCategories(),this.fetchAllTasks(),this.pollData()},beforeUnmount(){clearInterval(this.polling)},mounted(){let e=JSON.parse(localStorage.getItem("fetchOptions"));e&&Ue.set(e);let t=JSON.parse(localStorage.getItem("taskFilters"));t&&Je.set(t)}};const Xt=(0,Le.Z)(Ht,[["render",k]]);var zt=Xt;window.axios=o(7218),window.axios.defaults.headers.common["X-Requested-With"]="XMLHttpRequest";let Kt=document.getElementsByName("csrfmiddlewaretoken");Kt?window.axios.defaults.headers.common["X-CSRFToken"]=Kt[0].value:console.error("CSRF token not found: https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax"),(0,l.createApp)(zt).mount("#dashboard-page-content")}},t={};function o(l){var a=t[l];if(void 0!==a)return a.exports;var s=t[l]={exports:{}};return e[l].call(s.exports,s,s.exports,o),s.exports}o.m=e,function(){var e=[];o.O=function(t,l,a,s){if(!l){var n=1/0;for(d=0;d<e.length;d++){l=e[d][0],a=e[d][1],s=e[d][2];for(var c=!0,i=0;i<l.length;i++)(!1&s||n>=s)&&Object.keys(o.O).every((function(e){return o.O[e](l[i])}))?l.splice(i--,1):(c=!1,s<n&&(n=s));if(c){e.splice(d--,1);var r=a();void 0!==r&&(t=r)}}return t}s=s||0;for(var d=e.length;d>0&&e[d-1][2]>s;d--)e[d]=e[d-1];e[d]=[l,a,s]}}(),function(){o.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return o.d(t,{a:t}),t}}(),function(){o.d=function(e,t){for(var l in t)o.o(t,l)&&!o.o(e,l)&&Object.defineProperty(e,l,{enumerable:!0,get:t[l]})}}(),function(){o.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){o.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){var e={143:0};o.O.j=function(t){return 0===e[t]};var t=function(t,l){var a,s,n=l[0],c=l[1],i=l[2],r=0;if(n.some((function(t){return 0!==e[t]}))){for(a in c)o.o(c,a)&&(o.m[a]=c[a]);if(i)var d=i(o)}for(t&&t(l);r<n.length;r++)s=n[r],o.o(e,s)&&e[s]&&e[s][0](),e[s]=0;return o.O(d)},l=self["webpackChunkvue_tasks_table_view"]=self["webpackChunkvue_tasks_table_view"]||[];l.forEach(t.bind(null,0)),l.push=t.bind(null,l.push.bind(l))}();var l=o.O(void 0,[998],(function(){return o(1714)}));l=o.O(l)})();
//# sourceMappingURL=app.js.map