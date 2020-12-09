<template>
  <div>
    <div class="row mb-3">
      <form class="col-6" id="upload-file" method="post" enctype="multipart/form-data">
        <div class="custom-file">
          <input @change="selectFile" type="file" name="file" class="custom-file-input" id="customFile">
          <label class="custom-file-label" for="customFile"> {{ file ? file.name : "Select file..." }} </label>
        </div>
      </form>
    <button type="button" class="btn btn-primary" @click="uploadFile">Upload</button>
    </div>
    <div class="card border border-dark mb-3" style="height: 610px; width: 810px;">
      <div ref="editor" style="height: 600px; width: 800px;"></div>
    </div>
    <div v-if="error" class="alert alert-dismissible alert-warning">
      <button type="button" class="close" data-dismiss="alert" @click="clearError">&times;</button>
      <h4 class="alert-heading">Error!</h4>
      <p class="mb-0"> {{ errorMessage }} </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import * as monaco from 'monaco-editor';

export default {
  name: 'CodeInput',
  data() {
    return {
      code: '',
      file: null,
      error: false,
      errorMessage: '',
    }
  },
  methods: {
    clearError() {
      this.error = false;
      this.errorMessage = '';
    },
    selectFile() {
      this.file = $('#upload-file')[0][0].files[0];
      var request = new XMLHttpRequest();
      var fr = new FileReader(); 
      fr.onload = () => { 
        this.editor.setValue(fr.result); 
      }
      fr.readAsText(this.file); 
    },
    uploadFile() {
      axios.post('/upload-file', {
        code: this.editor.getValue(),
      }).then(response => {
        console.log(response);
        if (response.data.error) {
          console.log(response.data);
          this.error = true;
          this.errorMessage = response.data.error_message;
          this.editor.setValue(response.data.source)
        } else {
          this.error = false;
          this.errorMessage = '';
          this.$emit('response', response.data);
        }
      }).catch(function (error) {
        console.log(error);
      });
    },
  },
  async mounted() {
    const el = this.$refs.editor;
    this.editor = monaco.editor.create(el, {
      value: "",
      language: 'cpp',
    });
  },
}
</script>

