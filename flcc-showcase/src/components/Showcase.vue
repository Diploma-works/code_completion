<template>
  <div class="showcase">
    <h1>Full Line Code Completion Showcase</h1>
    <p>
      Download the plugin for JetBrains IDEs from
      <a href="https://plugins.jetbrains.com/plugin/14823-full-line-code-completion">JetBrains Marketplace</a>.
    </p>
    <el-card class="box-card code-edit-card">
      <div class="code-edit-wrapper">
        <el-input placeholder="Filename" v-model="selected_meta.filename" class="code-filename-input"></el-input>
        <el-select v-model="selected_language" filterable @change="onLanguageChange($event)"
                   placeholder="Select language" class="code-language-select">
          <el-option
              v-for="item in language_options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
        <prism-editor class="code-editor" v-model="selected_meta.context"
                      :highlight="highlighter" line-numbers></prism-editor>
      </div>
    </el-card>
    <el-input class="api-key-input" placeholder="Input API key, please" v-model="api_key" v-if="show_key_input">
      <i
          class="el-icon-key el-input__icon"
          slot="suffix">
      </i>
    </el-input>
    <el-button :plain="true" class="complete-button" @click="complete">Complete</el-button>
    <el-table
        v-if="completions.length > 0"
        :data="completions"
        style="width: 100%">
      <el-table-column
          prop="suggestion"
          label="Suggestion">
      </el-table-column>
      <el-table-column
          prop="score"
          label="Score">
      </el-table-column>
    </el-table>
    <p class="footnote">Site was visited {{ num_visits }} times, {{ num_completions }} completion requests were made</p>
  </div>
</template>

<script>
import {highlight} from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-kotlin';
import 'prismjs/themes/prism-tomorrow.css'; // import syntax highlighting styles
import countapi from 'countapi-js';
import 'vue-prism-editor/dist/prismeditor.min.css'; // import the styles somewhere
import '../themes/prism-material-light.css'
import {PrismEditor} from 'vue-prism-editor';
import LanguageMeta from "@/domain/LanguageMeta";

const language_to_meta = ['python', 'java', 'kotlin'].reduce((map, langId) => {
  map[langId] = LanguageMeta.build(langId)
  return map
}, {})

export default {
  name: 'Showcase',
  components: {
    PrismEditor,
  },
  data: () => ({
    language_options: [{
      value: 'python',
      label: 'Python'
    }, {
      value: 'java',
      label: 'Java'
    }, {
      value: 'kotlin',
      label: 'Kotlin'
    }],
    selected_language: 'python',
    selected_meta: language_to_meta['python'],
    api_key: '',
    show_key_input: true,
    completions: [],
    error_message: '',
    num_visits: 0,
    num_completions: 0
  }),
  methods: {
    highlighter(code) {
      return highlight(code, this.selected_meta.prismLang, this.selected_meta.langId);
    },
    onLanguageChange(language) {
      this.selected_meta = language_to_meta[language]
    },
    async complete() {
      const offset = this.selected_meta.context.length
      let response = await this.selected_meta.complete(offset, this.api_key)
      switch (response.status) {
        case 403:
          this.$message({message: 'API key is incorrect', type: 'error'})
            this.show_key_input=true
          break;
        case 200:
          this.completions = (await response.json()).completions
          this.num_completions = (await countapi.update('flcc.showcase', 'completions', 1)).value
          break;
        case 204:
          this.$message({message: 'Request cancelled by server', type: 'warning'})
          break;
        default:
          this.$message({message: 'Whoops, something went wrong', type: 'error'})
      }
    },
  },
  async created() {
    this.num_visits = (await countapi.update('flcc.showcase', 'visits', 1)).value
    this.num_completions = (await countapi.get('flcc.showcase', 'completions')).value
    let uri = window.location.search.substring(1);
    let api_key_param = new URLSearchParams(uri).get("api_key");
    if (api_key_param != null) {
      this.api_key = api_key_param
      this.show_key_input = false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.showcase {
  max-width: 705px;
  margin: 0.69em auto auto;
  display: grid;
  grid-row-gap: 1.5em;
}

h1, p {
  margin: 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #ef6073;
}

.prism-editor__textarea:focus {
  outline: none;
}

.code-edit-card {
  padding-bottom: 30px;
}

.code-edit-wrapper {
  display: grid;
  grid-column-gap: 10px;
  grid-row-gap: 30px;
}

.code-filename-input {
  grid-row: 1;
  grid-column: 1;
}

.code-language-select {
  grid-row: 1;
  grid-column: 2;
}

.code-editor {
  grid-row: 2;
  grid-column-start: 1;
  grid-column-end: 3;
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 3px;
}

.complete-button {
  justify-self: center;
  width: 100%;
  box-shadow: 0 1px 5px 0 rgb(0 0 0 / 10%);
}

.api-key-input-label {
  color: #c7c7c7;
  margin-left: 1.5%;
  width: fit-content;
  font-size: 14px;
}

.footnote {
  color: #c7c7c7;
}

</style>
