<template>
    <div v-if="readOnly">
        {{value === null ? field.default: value}}
    </div>
    <div v-else>
        <LabelComponent :field="field" :value="value" :show-help="showHelp"></LabelComponent>
        <input type="text" maxlength="100" class="form-control input-sm" :value="value === null ? field.default: value"
            @input="updated" :required="field.required" :class="{'form-control-sm': small}"/>
    </div>
</template>
<script>
    import LabelComponent from './Label.vue'
    import Widget from '../../mixins/Widget.js';
    export default {
        mixins: [Widget],
        components: { LabelComponent },
        methods: {
            updated: _.debounce(function (e) { 
                this.triggerUpdateEvent(this.message, this.field, e.target.value); 
            }, 500)
        },
        computed: {
            normalizedValue: () => {
                return this.field.value || this.field.default;
            }
        },
        mounted() {
            const value = (this.field['default'] ? this.field['default']: null)
            this.$root.$emit(this.message,
                 this.field, this.value || value);
        },
    }
</script>
