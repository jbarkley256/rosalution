<template>
  <table class="section-box-container">
    <tbody>
      <tr class="section-header">
        <td>
          <h2 class="section-name">
            {{header}}
          </h2>
        </td>
        <td class="annotations">
          <slot name="headerDatasets"></slot>
        </td>
        <button v-if="attachSection" class="attach-logo" @click="$emit('attach-image', header)" data-test="attach-logo">
          <font-awesome-icon :icon="['fa', 'paperclip']" size="xl" />
        </button>
        <label v-else class="collapsable-icon">
          <font-awesome-icon icon="chevron-down" size="lg"/>
        </label>
      </tr>
      <div class="seperator"></div>
      <slot></slot>
      <img v-if="displaySectionImage" class="annotation-image" :src="this.sectionImage"/>
    </tbody>
  </table>
</template>

<script>
import Annotations from '@/models/annotations.js';

export default {
  name: 'annotation-section',
  props: {
    header: {
      type: String,
    },
    imageId: {
      type: String,
    },
  },
  updated() {
    this.fetchImage(this.imageId);
  },
  data() {
    return {
      imageHeaders: [
        'Gene Homology/Multi-Sequence allignment',
        'Protein Expression',
        'Modelability',
        'Druggability',
      ],
      sectionImage: '',
    };
  },
  computed: {
    attachSection() {
      return this.imageHeaders.includes(this.header);
    },
    displaySectionImage() {
      return this.imageHeaders.includes(this.header);
    },
  },
  methods: {
    async fetchImage(imageId) {
      if (imageId == '') {
        return;
      }
      const image = await Annotations.getAnnotationImage(imageId);
      this.sectionImage = image;
    },
  },
};
</script>

<style scoped>
table {
  width:100%;
}

.section-box-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-10);
  margin: var(--p-10);
  gap: var(--p-10);
  border-radius: var(--content-border-radius);
  background-color: var(--rosalution-white);
}

.section-header {
  height: 2rem;
  display: flex;
}

.section-name {
  margin: var(--p-1) var(--p-1) 0 var(--p-1);
}

.annotations {
  flex-grow: 2;
  justify-content: flex-start;
}

.collapsable-icon {
  color: var(--rosalution-grey-200);
  cursor: pointer;
}

.attach-logo {
  color: var(--rosalution-purple-300);
  background: none;
  border: none;
  float: right;
  cursor: pointer;
}

.seperator {
  height: .125rem;
  background-color: var(--rosalution-grey-100);
  border: solid .0469rem var(--rosalution-grey-100);
}

.annotation-image {
  max-height: 31.25rem;
}

</style>
