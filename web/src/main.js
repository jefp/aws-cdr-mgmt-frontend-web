/*
 * Copyright 2017-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with
 * the License. A copy of the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions
 * and limitations under the License.
 */

// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import router from './router';
import aws_exports from './aws-exports';
import { components } from 'aws-amplify-vue';
import Amplify from 'aws-amplify';

import VDateRange from 'vuetify-daterange-picker';
import 'vuetify-daterange-picker/dist/vuetify-daterange-picker.css';

Vue.use(VDateRange);


import Vuetify from 'vuetify'

Vue.use(Vuetify)


Vue.config.productionTip = false

Amplify.configure(aws_exports)

require('vuetify/dist/vuetify.min.css')

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  template: '<App/>',
  components: {
    App,
    ...components
  }
})
