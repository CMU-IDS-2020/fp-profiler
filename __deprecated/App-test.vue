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
      <GoDiagram :modelData="diagramData" style="border: solid 1px black; width:100%; height:400px"></GoDiagram>
      <!-- <p> Response {{ response }} </p> -->
      <div id="vis"></div>
    </div>
  </div>
</template>

<script>
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
      response: ':)?',
      diagramData: {  // passed to <diagram> as its modelData
        fullNodeInfo: [
            {"ID": 0, "name": "main", "selfTime": 0.0, "totalTime": 2.44, "parent": [], "child": [0, 1], "called": 1}, 
            {"ID": 1, "name": "fb", "selfTime": 2.29, "totalTime": 2.29, "parent": [0, 2], "child": [2], "called": 1}, 
            {"ID": 2, "name": "sum", "selfTime": 0.15, "totalTime": 0.15, "parent": [1], "child": [], "called": 1}
        ],

        fullEdgeInfo: [
            {"from": 0, "to": 1, "called": 1, "time": 2.29, "cTime": 2.29, "gcTime": 0.0}, 
            {"from": 0, "to": 2, "called": 1, "time": 0.15, "cTime": 0.15, "gcTime": 0.0}, 
            {"from": 1, "to": 1, "called": 331160280, "time": 0, "cTime": 0, "gcTime": 0}
        ],


        baseNodeArr: [
            {"key": 0, "name": "main", "time": 0.0, "isExpanded": true, "percent": 1, "hide": false, "timePct": 0.0}, 
            {"key": 1, "name": "fb", "time": 2.29, "isExpanded": true, "percent": 1, "hide": false, "timePct": 0.9385245901639344}, 
            {"key": 2, "name": "sum", "time": 0.15, "isExpanded": true, "percent": 1, "hide": false, "timePct": 0.06147540983606557}
        ],

        baseEdgeArr:[
            {"from": 0, "to": 1, "validcalled": 1, "validTime": 2.29, "validCTime": 2.29, "validGcTime": 0.0, "hide": false}, 
            {"from": 0, "to": 2, "validcalled": 1, "validTime": 0.15, "validCTime": 0.15, "validGcTime": 0.0, "hide": false}, 
            {"from": 1, "to": 1, "validcalled": 331160280, "validTime": 0, "validCTime": 0, "validGcTime": 0, "hide": false}
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
