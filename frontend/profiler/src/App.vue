<template>
  <div id="app">
    <div class="container">
      <!-- upload a file -->
      <div class="row">
        <form class="col-6" id="upload-file" method="post" enctype="multipart/form-data">
          <div class="custom-file">
            <input @change="selectFile" type="file" name="file" class="custom-file-input" id="customFile">
            <label class="custom-file-label" for="customFile"> {{ file ? file.name : "Select file..." }} </label>
          </div>
        </form>
        <button type="button" class="btn btn-primary" @click="uploadFile">Upload</button>
      </div>
<<<<<<< HEAD
    <GoDiagram v-bind:modelData="diagramData"
               style="border: solid 1px black; width:100%; height:400px"></GoDiagram>
=======
      <GoDiagram :modelData="diagramData" style="border: solid 1px black; width:100%; height:400px"></GoDiagram>
      <!-- <p> Response {{ response }} </p> -->
>>>>>>> bd4c2e9792a3b3c4bcda9b5daa8c4db0067745e4
      <div id="vis"></div>
    </div>
  </div>
</template>

<script>
<<<<<<< HEAD
import GoDiagram from './components/GoDiagram.vue'
=======
>>>>>>> bd4c2e9792a3b3c4bcda9b5daa8c4db0067745e4
import axios from 'axios'
import $ from 'jquery'
import vegaEmbed from 'vega-embed'
import GoDiagram from './components/GoDiagram.vue'

function obtainHighlightItems(view_) {
  return view_.scenegraph().root.items[0].items[1].items[0].items[1].items[0].items[1].items;
}

export default {
  name: 'App',
  components: {
    GoDiagram
  },
  data() {
    return {
      file: null,
<<<<<<< HEAD
      response: '',
=======
      response: ':)?',
>>>>>>> bd4c2e9792a3b3c4bcda9b5daa8c4db0067745e4
      diagramData: {  // passed to <diagram> as its modelData
        nodeDataArray: [
          { key: 1, text: "Alpha", color: "lightblue" },
          { key: 2, text: "Beta", color: "orange" },
          { key: 3, text: "Gamma", color: "lightgreen" },
          { key: 4, text: "Delta", color: "pink" }
        ],
        linkDataArray: [
          { from: 1, to: 2 },
          { from: 1, to: 3 },
          { from: 3, to: 4 }
        ]
      },
    }
  },
  methods: {
    selectFile() {
      this.file = $('#upload-file')[0][0].files[0];
    },
    uploadFile() {
      var form_data = new FormData($('#upload-file')[0]);
      $.ajax({
        type: 'POST',
        url: '/upload-file',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: response => {
          this.response = response;
          vegaEmbed('#vis', response).then(({spec, view}) => {
          this.vega_view = view;
          // console.log(view.scenegraph().root.items[0].items[1].items[0].items[1].items[0].items[1].items.length);
          // this.highlightLinesByFunc('access_by_col');
          // this.highlightLinesByFunc('access_by_row');
          // this.highlightLinesByLnum([15, 16, 17]);

    // view.addEventListener('click', function (event, item) {
    //     console.log(item.mark);
    //       })
        });
        },
      });
    },
    highlightLines(items) {
      // let items = obtainHighlightItems(this.vega_view);
      for (let item of items) {
        item.opacity = 0.5;
        this.vega_view.dirty(item);
      }
    },
    clearHighlightLines(items) {
      for (let item of items) {
        if (item.opacity > 0.0) {
          item.opacity = 0.0;
          this.vega_view.dirty(item);
        }
      }
    },
    highlightLinesByFunc(func_name) {
      let items = obtainHighlightItems(this.vega_view);
      this.clearHighlightLines(items);
      this.highlightLines(items.filter(item=>(item.datum.Func === func_name)));
    },
    highlightLinesByLnum(line_nums) {
      let items = obtainHighlightItems(this.vega_view);
      this.clearHighlightLines(items);
      this.highlightLines(items.filter(item=>(line_nums.includes(item.datum['Line Number']))));
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
