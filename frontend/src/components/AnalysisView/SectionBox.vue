<template>
  <table class="section-box-container">
    <tbody>
      <input v-if="!this.edit" type="checkbox" v-bind:id="section_toggle"/>
      <tr class="section-header">
        <td class="section-header-content">
          <h2 class="section-name">
            {{header}}
          </h2>
          <button v-if="isSectionImage" class="attach-logo" @click="$emit(this.sectionImageOperation, header)">
            <font-awesome-icon :icon="['fa', 'paperclip']" size="xl" />
          </button>
          <label v-if="this.edit" class="edit-logo" id="edit-logo">
            <font-awesome-icon icon="pencil" size="lg"/>
          </label>
          <label v-else class="collapsable-logo" v-bind:for="section_toggle">
            <font-awesome-icon icon="chevron-down" size="lg"/>
          </label>
        </td>
      </tr>
      <div class="separator"></div>
        <tr class="field-value-row" v-for="content in contentList" :key="content">
          <td v-if="!this.sectionImageExist">
            <label class="field"
            v-bind:style="[content.value.length === 0 && !this.edit ? 'color: var(--rosalution-grey-300);'
            : 'color: var(--rosalution-black);']">
              {{content.field}}
            </label>
          </td>
          <td class="values" v-if="!this.sectionImageExist">
            <span v-if="this.edit" role="textbox" class="editable-values" contenteditable
            data-test="editable-value" @input="onContentChanged(header, content.field, $event)">
              {{content.value.join('\r\n')}}
            </span>
            <tr v-else v-for="value in content.value" :key="value" class="value-row" data-test="value-row">
              {{value}}
            </tr>
          </td>
        </tr>
        <img class="section-image" :src="this.sectionImage"/>
    </tbody>
  </table>
</template>

<script>
import Analyses from '../../models/analyses';

export default {
  name: 'section-box',
  emits: ['update:contentRow', 'attach-image', 'update-image'],
  props: {
    analysis_name: {
      type: String,
    },
    header: {
      type: String,
    },
    content: {
      type: Array,
    },
    edit: {
      type: Boolean,
    },
  },
  data() {
    return {
      contentList: this.content,
      section_toggle: this.header.toLowerCase() + '_collapse',
      sectionImage: '',
    };
  },
  created() {
    this.pedigreeImage();
  },
  computed: {
    isSectionImage() {
      return this.header == 'Pedigree';
    },
    sectionImageExist() {
      return (this.isSectionImage && this.contentList.length > 0);
    },
    sectionImageOperation() {
      if (this.sectionImageExist) {
        return 'update-image';
      }
      return 'attach-image';
    },
  },
  methods: {
    onContentChanged(header, contentField, event) {
      const contentRow = {
        header: header,
        field: contentField,
        value: event.target.innerText.split('\n'),
      };
      this.$emit('update:contentRow', contentRow);
    },
    async pedigreeImage() {
      if (this.header == 'Pedigree' && this.contentList.length > 0) {
        const fileId = this.contentList[0].value[0];
        const image = await Analyses.getSectionImage(fileId);
        this.sectionImage = image;
      }
    },
  },
};
</script>

<style scoped>
div {
  font-family: "Proxima Nova", sans-serif;
  padding: var(--p-0);
}

.section-box-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-10);
  margin: var(--p-10);
  width: 100%;
  gap: var(--p-10);
  border-radius: 1.25rem;
  background-color: var(--rosalution-white);
}

.section-header {
  height: 1.75rem;
  display: flex;
}

.section-header-content {
  display: flex;
  align-items: center;
  flex: 1 0 auto;
}

.section-name {
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
  flex: 1 0 auto;
}

.section-image {
  max-height: 31.25rem;
}

.attach-logo {
  color: var(--rosalution-purple-300);
  background: none;
  border: none;
  cursor: pointer;
}

.collapsable-logo {
  color: var(--rosalution-grey-200);
  cursor: pointer;
}

.logo-attach-edit {
  color: var(--rosalution-purple-300);
  background: none;
  border: none;
  cursor: pointer;
}

.separator {
  height: .125rem;
  background-color: var(--rosalution-grey-100);
  border: solid .0469rem var(--rosalution-grey-100);
}

.field-value-row {
  display: flex;
  flex-direction: row;
  gap: .625rem;
  margin: 0.625rem 0.250rem 0.625rem 0.250rem;
}

.field {
  display: inline-block;
  width: 11.25rem;
  height: 1.375rem;
  margin: 0 1.1875rem .0063rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  text-align: left;
}

.values {
  font-size: 1.125rem;
  text-align: left;
  color: var(--rosalution-black);
  width: 100%;
  display: block;
}

.value-row {
  font-size: 1.125rem;
  color: var(--rosalution-black);
  display: block;
  width: 100%;
}

.edit-logo {
  color: var(--rosalution-purple-100);
}

.editable-values {
  display: block;
  width: 100%;
  overflow: hidden;
  resize: both;
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: 2px solid var(--rosalution-purple-200);
  font-family: inherit;
  font-size: inherit;
}


span:focus {
  color: var(--rosalution-purple-300);
  outline: none;
  box-shadow: 0px 5px 5px var(--rosalution-grey-200);
}

input[type="checkbox"] {
  display: none;
}

.section-box-container input[type="checkbox"]:checked ~ .field-value-row {
  display: none;
}

.section-box-container input[type="checkbox"]:checked ~ img {
  display: none;
}

input[type="checkbox"]:checked ~ tr > td > .collapsable-logo {
  transform: scaleY(-1);
}
</style>
