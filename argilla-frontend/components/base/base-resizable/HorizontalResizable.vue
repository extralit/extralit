<template>
  <div class="resizable-h" :class="resizing ? '--h-resizing' : null">
    <div class="resizable-h__up">
      <slot name="up" />
    </div>

    <div class="resizable-h__bar" ref="resizableBar">
      <div class="resizable-h__bar__inner" />
    </div>
    <div class="resizable-h__down" v-if="!collapsable">
      <slot name="down" />
    </div>
    <BaseCollapsablePanel
      v-else
      class="resizable-h__down"
      :class="isExpanded ? '--expanded' : null"
      :is-expanded="isExpanded"
      @toggle-expand="toggleExpand"
    >
      <slot name="downHeader" slot="panelHeader" />
      <slot name="downHeaderExpanded" slot="panelHeaderExpanded" />
      <slot name="downContent" slot="panelContent" />
    </BaseCollapsablePanel>
  </div>
</template>

<script>
import { useResizable } from "./useResizable";
import BaseButton from "../base-button/BaseButton.vue";

const EVENT = {
  MOUSE_EVENT: "mousemove",
  MOUSE_UP: "mouseup",
  MOUSE_DOWN: "mousedown",
};

export default {
  components: { BaseButton },
  props: {
    id: {
      type: String,
      default: "h-rz",
    },
    collapsable: {
      type: Boolean,
      default: false,
    },
    minHeightPercent: {
      type: Number,
      default: 25,
    },
    topPercentHeight: {
      type: Number,
    },
  },
  data() {
    return {
      resizing: false,
      isExpanded: false,
      upSidePrevPosition: {
        clientY: 0,
        height: 0,
      },
      resizer: null,
      upSide: null,
      downSide: null,
      expandedPanelMinHeight: 80,
      collapsedPanelHeight: 50,
    };
  },
  computed: {
    parentHeight() {
      return this.resizer.parentNode.getBoundingClientRect().height;
    },
  },
  watch: {
    async isExpanded() {
      this.debounce.stop();
      const savedPosition = this.getPosition();
      if (this.isExpanded) {
        if (this.resizing) {
          this.upSide.style.height = savedPosition?.position;
        }
      } else {
        this.upSide.style.height = "100%";
      }

      await this.debounce.wait();
      this.$nextTick(() => {
        this.setPosition({
          isExpanded: this.isExpanded,
          position: savedPosition?.position ?? this.upSide.style.height,
        });
      });
    },
  },

  mounted() {
    this.resizer = this.$refs.resizableBar;
    this.upSide = this.resizer.previousElementSibling;
    this.downSide = this.resizer.nextElementSibling;

    this.limitElementHeight(this.upSide);
    if (!this.collapsable) {
      this.limitElementHeight(this.downSide);
    }

    this.resizer.addEventListener(EVENT.MOUSE_DOWN, this.mouseDownHandler);

    const savedPosition = this.getPosition();
    if (savedPosition) {
      if (savedPosition.isExpanded) {
        this.isExpanded = savedPosition.isExpanded;
        this.upSide.style.height = savedPosition.position;
      } else {
        this.isExpanded = false;
        this.upSide.style.height = "100%";
      }
    } else if (this.topPercentHeight) {
      this.isExpanded = false;
      this.upSide.style.height = `${this.topPercentHeight}%`;
    } else {
      this.isExpanded = false;
      this.upSide.style.height = "100%";
    }
  },
  destroyed() {
    this.resizer.removeEventListener(EVENT.MOUSE_DOWN, this.mouseDownHandler);
  },
  methods: {
    savePosition() {},
    limitElementHeight(element) {
      element.style["max-height"] = "100%";
      element.style["min-height"] = `${this.minHeightPercent}%`;
    },
    savePositionOnStartResizing(e) {
      this.upSidePrevPosition = {
        clientY: e.clientY,
        height: this.upSide.getBoundingClientRect().height,
      };
    },
    resize(e) {
      e.preventDefault();
      const dY = e.clientY - this.upSidePrevPosition.clientY;
      const proportionalHeight = (this.upSidePrevPosition.height + dY) * 100;
      const newHeight = proportionalHeight / this.parentHeight;
      const collapsedHeight =
        (this.collapsedPanelHeight * 100) / this.parentHeight;
      this.upSide.style.height = `${newHeight}%`;
      if (newHeight >= 100 - collapsedHeight) {
        this.isExpanded = false;
      } else {
        this.isExpanded = true;
      }
    },
    mouseMoveHandler(e) {
      this.resize(e);
    },
    mouseUpHandler() {
      this.$nextTick(() => {
        this.setPosition({
          isExpanded: this.isExpanded,
          position: `${this.upSide.getBoundingClientRect().height}px`,
        });
      });

      document.removeEventListener(EVENT.MOUSE_EVENT, this.mouseMoveHandler);
      document.removeEventListener(EVENT.MOUSE_UP, this.mouseUpHandler);
      this.resizing = false;
    },
    mouseDownHandler(e) {
      this.savePositionOnStartResizing(e);

      document.addEventListener(EVENT.MOUSE_EVENT, this.mouseMoveHandler);
      document.addEventListener(EVENT.MOUSE_UP, this.mouseUpHandler);
      this.resizing = true;
    },
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
      if (this.isExpanded) {
        const savedPosition = this.getPosition();
        const useSavedPosition =
          this.parentHeight - parseInt(savedPosition?.position) >
          this.expandedPanelMinHeight;
        this.upSide.style.height = useSavedPosition
          ? savedPosition?.position
          : "50%";
      }
    },
  },
  setup(props) {
    return useResizable(props);
  },
};
</script>

<style lang="scss" scoped>
$resizabla-bar-color: #6794fe;
$collapsed-panel-height: 50px;
$resizable-bar-width: $base-space;
.resizable-h {
  $this: &;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  min-height: 0;
  width: 100%;
  &.--h-resizing {
    user-select: none;
  }

  &__up {
    align-items: center;
    display: flex;
    justify-content: center;
    min-height: $collapsed-panel-height;
    transition: all 0.2s ease-in;
    margin-bottom: calc(-#{$resizable-bar-width} / 2);
    @include media("<desktop") {
      height: auto !important;
      max-height: none !important;
      min-height: auto !important;
    }
    .--h-resizing & {
      transition: none;
    }
  }

  &__down {
    flex: 1;
    align-items: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: $collapsed-panel-height;
    margin-top: calc(-#{$resizable-bar-width} / 2);
    &.panel {
      @include media(">=desktop") {
        border: none;
      }
    }
    @include media("<desktop") {
      height: auto !important;
      max-height: none !important;
      min-height: auto !important;
    }
  }

  &__bar {
    height: $resizable-bar-width;
    width: 100%;
    display: flex;
    align-items: center;
    z-index: 1;
    cursor: row-resize;
    @include media("<desktop") {
      display: none;
    }

    &__inner {
      width: 100%;
      border-bottom: 1px solid var(--bg-opacity-10);
      transition: all 0.1s ease-in;
    }

    &:hover,
    .--h-resizing & {
      #{$this}__bar__inner {
        transition: all 0.1s ease-in;
        border: 2px solid $resizabla-bar-color;
      }
    }
  }
}
</style>
