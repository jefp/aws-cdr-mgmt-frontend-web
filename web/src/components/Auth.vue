<template>
  <v-container grid-list-md>
    <v-layout row wrap align-center justify-center fill-height>
      <div>
        <v-flex xs10 offset-xs1>
          <v-card-text class="justify-center">
            <amplify-authenticator />
          </v-card-text>
        </v-flex>
      </div>
    </v-layout>
  </v-container>
</template>

<script>
import Vue from 'vue'


export default {
  name: 'Auth',
  data () {
    return {}
  }
}
</script>
