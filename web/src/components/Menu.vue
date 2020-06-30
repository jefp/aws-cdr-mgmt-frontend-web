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

<template >
    <div v-if="user">
      <v-bottom-nav
        :active.sync="bottomNav"
        :value="true"
        fixed
        color="white"
      >
        <v-btn color="teal" flat value="recent"  v-on:click="Home">
          <span>Home</span>
          <v-icon>home</v-icon>
        </v-btn>

        <v-btn color="teal" flat value="request"  v-on:click="Request">
          <span>Request</span>
          <v-icon>add_circle_outline</v-icon>
        </v-btn>

        <v-btn color="teal" flat value="favorites"  v-on:click="Jobs">
          <span>Jobs</span>
          <v-icon>loop</v-icon>
        </v-btn>

        <v-btn color="teal" flat value="nearby"  v-on:click="profile">
          <span >Profile</span>
          <v-icon>person</v-icon>
        </v-btn>
        <v-btn color="teal" flat value="out"  v-on:click="signOut" v-if="user">
          <span >Logout</span>
          <v-icon>exit_to_app</v-icon>
        </v-btn>
      </v-bottom-nav>
    </div>
</template>



<script>
import { Auth, Hub} from 'aws-amplify';
import AmplifyStore from '../store/store';
import { components, AmplifyEventBus } from 'aws-amplify-vue';
import Amplify, * as AmplifyModules from 'aws-amplify';


export default {
  name: 'Menu',
  data () {
    return {
      bottomNav: 'recent'
    }
  },
  computed: {
    user() {
      return AmplifyStore.state.user
    }
  },
  methods: {
     signOut: function(event) {
        this.$Amplify.Auth.signOut()
            .then(() => {
              console.log('signout success')
              return AmplifyEventBus.$emit('authState', 'signedOut')
            })
            .catch(e => this.setError(e));
    },
    setError: function(e) {
      this.error = this.$Amplify.I18n.get(e.message || e);
      console.log(this.error);
    },
    Home: function() {
        this.$router.push('/')
    },
    Request: function() {
        this.$router.push('/request')
    },
    Jobs: function() {
        this.$router.push('/Jobs')
    },
    profile: function() {
        this.$router.push('/profile')
    },
  }
}
</script>


