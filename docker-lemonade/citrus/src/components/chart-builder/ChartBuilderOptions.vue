<template>
    <div class="chart-builder-options" v-if="workflow.visualization">
        <b-form class="chart-properties">
            <b-card sub-title="Opções da visualização">
                <b-form-group id="title" label="Tipo do gráfico:" label-for="title">
                    <v-select :options="chartTypes" label="label" :reduce="(opt) => opt.name"
                        v-model="workflow.visualization.forms.type.value">
                        <template #option="{ label, name}">
                            <div class="bg-chart" :class="`bg-${name}`">{{label}}</div>
                        </template>

                        <template #selected-option="{ label, name }">
                            <div>
                                <div class="bg-chart" :class="`bg-${name}`">{{label}}</div>
                            </div>
                        </template>
                    </v-select>
                </b-form-group>
            </b-card>
            <b-card sub-title="Eixo X" class="mt-1">
                <b-form-group label="Atributo:">
                    <v-select :options="attributes" label="name" :reduce="(opt) => opt.name" :multiple="true"
                        v-model="workflow.group.forms.attributes.value">
                        <template #option="{name, type}">
                            <font-awesome-icon class="mr-2" prefix="fa" :icon="getIcon({type})" />{{name}}
                        </template>

                        <template #selected-option="{name, type}">
                            <div role="button">
                                <font-awesome-icon class="mr-2" prefix="fa" :icon="getIcon({type})" />{{name}}
                            </div>
                        </template>
                    </v-select>
                </b-form-group>
            </b-card>
            <b-card sub-title="Eixo Y" class="mt-1" style="z-index:10">
                <b-form-group label="Atributo(s):">
                    <v-select :options="attributes" label="name" :reduce="reduceYAxis" :multiple="multipleY"
                        ref="vueSelect" v-model="workflow.group.forms.function.value">
                        <template #option="{name, type}">
                            <font-awesome-icon class="mr-2" prefix="fa" :icon="getIcon({type})" />{{name}}
                        </template>

                        <template #selected-option="{name, type, f}">
                            <div role="button" @click.stop="handleSelect(name)" @mousedown.stop="handleSelect(name)"
                                @mouseup.stop="handleSelect(name)">
                                <column-aggregate v-if="name" :name="name" :type="type" :f="f" @select="handleUpdateFunction" />
                            </div>
                        </template>
                    </v-select>
                </b-form-group>
            </b-card>
            <b-card sub-title="Formatação" class="mt-1" style="z-index:1">
                <b-form-group>
                    <b-form-checkbox v-model="workflow.visualization.forms.display_legend.value" switch>Exibir legenda
                    </b-form-checkbox>
                </b-form-group>

                <b-form-group>
                    <ColorPalette :field="palette" :value="workflow.visualization.forms.palette.value"
                        @update="handleUpdatePalette" />
                </b-form-group>

                <template v-if="workflow.visualization.forms.type.value=='bar'">
                    <b-form-group label="Direção:">
                        <select v-model="workflow.visualization.forms.direction.value"
                            class="form-control form-control-sm">
                            <option value="vertical">Vertical</option>
                            <option value="horizontal">Horizontal</option>
                        </select>
                    </b-form-group>

                    <b-form-group>
                        <b-form-checkbox v-model="workflow.visualization.forms.stacked.value" switch>Empilhado
                        </b-form-checkbox>
                    </b-form-group>
                </template>

                <template v-if="workflow.visualization.forms.type.value=='pie'">
                    <b-form-group label="Preenchimento (100 = pizza, < 100 donut)" label-for="pie-fill">
                        <b-form-input id="title" v-model="workflow.visualization.forms.hole.value" type="number" min="0"
                            max="100" step="1" class="w-50 form-control-sm" />
                    </b-form-group>
                </template>

                <template v-if="workflow.visualization.forms.type.value=='line'">

                    <b-form-group label="Espessura da Linha:" label-for="line-width">
                        <b-form-input v-model="workflow.visualization.forms.line_stroke.value" type="number" min="1"
                            max="10" step="1" class="form-control form-control-sm w-50" />

                    </b-form-group>

                    <b-form-group label="Tipo de Linha:" label-for="line-width">
                        <select class="form-control form-control-sm"
                            v-model="workflow.visualization.forms.line_type.value">
                            <option value="solid">Sólida</option>
                            <option value="dot">Ponto</option>
                            <option value="dashdot">Tracejada</option>
                        </select>
                    </b-form-group>

                    <b-form-group label="Modo para as séries:">
                        <select class="form-control form-control-sm" v-model="workflow.visualization.forms.mode.value">
                            <option value="lines">Somente linhas</option>
                            <option value="marks">Somente pontos</option>
                            <option value="lines+marks">Linhas e pontos</option>
                        </select>
                    </b-form-group>

                </template>

                <template v-if="workflow.visualization.forms.type.value=='bubble'">

                    <b-form-group label="Símbolo" label-for="line-width">
                        <b-form-select v-model="chartCustomOptions.bubbleChart.symbol" :options="[
                        {value: 'circle', text: 'Círculo'},
                        {value: 'square', text: 'Quadrado'},
                        {value: 'diamond', text: 'Diamante'},
                        {value: 'cross', text: 'Cruz'},
                    ]"></b-form-select>

                    </b-form-group>

                </template>
            </b-card>
        </b-form>
    </div>
</template>
<script>

    import vSelect from 'vue-select';
    import palettes from '../widgets/util/palettes';
    import ColorPalette from '../widgets/ColorPalette.vue';
    import ChartBuilderColumnAggregate from './ChartBuilderColumnAggregate.vue';

    export default {
        components: { vSelect, ColorPalette, 'column-aggregate': ChartBuilderColumnAggregate },
        props: {
            attributes: { type: Array, required: true },
            workflow: { type: Object, required: true }
        },
        data() {
            return {
                y_attributes: [],
                form: {
                    title: {
                        text: ""
                    },
                    showlegend: false,
                    pallete: 0
                },
                chartType: "bar",

                chartCustomOptions: {
                    barOptions: {
                        stacked: false,
                        horizontal: false
                    },
                    pieOptions: {
                        hole: 1
                    },
                    lineOptions: {
                        line: {
                            dash: 'solid',
                            width: 1,
                            shape: 'linear'
                        }
                    },
                    bubbleChart: {
                        symbol: 'circle'
                    }
                },
                chartTypes: [
                    {
                        name: "bar",
                        label: "Gráfico de Barras",
                    },
                    {
                        name: "pie",
                        label: "Gráfico de Pizza",
                    },
                    {
                        name: "line",
                        label: "Gráfico de Linhas",
                    },
                    /*
                    {
                        name: "bubble",
                        label: "Gráfico de Bolhas",
                    },
                    */
                    {
                        name: "scatter",
                        label: "Gráfico de Dispersão",
                    },
                    /*{
                        name: "dots",
                        label: "Gráfico de Pontos",
                        image: "https://images.plot.ly/plotly-documentation/thumbnail/dot-plot.jpg"
                    },*/
                    {
                        name: "filled-area",
                        label: "Gráfico de Área",
                    },
                ],
                palette: { label: 'Paleta de cores' }
            }
        },
        watch: {
            workflow() {
                if (this.workflow.visualization.forms.hole.value === null) {
                    this.$nextTick(() => this.workflow.visualization.forms.hole.value = 100);
                }
            }
        },
        computed: {
            palettes: () => palettes.map(v => v[0]).reduce((prev, cur, i) => [...prev, { value: i, text: cur }], []),
            multipleY() {
                return this.chartType !== 'pie';
            }
        },
        mounted() {
            this.$root.$on('chartBuilderUpdateChart', this.updateChart)
                        
        },
        methods: {
            getIcon(attr) {
                switch (attr.type) {
                    case 'DECIMAL':
                    case 'INTEGER':
                        return 'hashtag';
                    case 'CHARACTER':
                        return 'font';
                    case 'DATE':
                        return 'calendar';
                    default:
                        return 'question-circle'
                }
            },
            changeOptions() {

                let options = { ...this.form };

                options.colorway = palettes[this.form.pallete][1];

                switch (this.chartType) {
                    case "bar":
                        if (this.chartCustomOptions.barOptions.stacked) options.barmode = 'stack';
                        if (this.chartCustomOptions.barOptions.horizontal) options.orientation = 'h';
                        break;
                    case "pie":
                        options.hole = 1 - this.chartCustomOptions.pieOptions.hole;
                        break;
                    case "line":
                        options.line = this.chartCustomOptions.lineOptions.line;
                        break;
                    case "bubble":
                        options.symbol = this.chartCustomOptions.bubbleChart.symbol;
                        break;
                }

                this.$root.$emit('chartBuilderUpdateChart', {
                    type: "layout",
                    value: options
                });
            },
            updateChart(data) {
                if (data.type == "type") {
                    this.chartType = data.value;
                }
            },
            handleUpdatePalette(field, value) {
                this.workflow.visualization.forms.palette.value = value;
            },
            handleSelect(name) {
                /*const item = this.yAxis.find((v) => v.attribute === name);
                console.debug(item)*/

            },
            handleUpdateFunction(name, f, type) {
                const item = this.workflow.group.forms.function.value.find((v) => v.attribute === name);
                if (item) {
                    item.f = f;
                    item.name = name;
                    item.alias = `${f.toLowerCase()}_${name}`;
                    item.type = type;
                }
            },
            reduceYAxis(opt) {
                return { attribute: opt.name, f: 'count', alias: `count_${opt.name}` };
            }
        }
    }
</script>
<style scoped lang="scss">
    .bg-filled-area {
        width: 52px;
        height: 52px;
        background: url('chart-types.png') -8px -10px;
    }

    .bg-bar {
        width: 52px;
        height: 52px;
        background: url('chart-types.png') -79px -9px;
    }

    .bg-bubble {
        width: 52px;
        height: 52px;
        background: url('chart-types.png') -10px -78px;
    }

    .bg-line {
        width: 52px;
        height: 52px;
        background: url('chart-types.png') -78px -78px;
    }

    .bg-pie {
        width: 52px;
        height: 52px;
        background: url('chart-types.png') -146px -10px;
    }

    .bg-scatter {
        width: 52px;
        height: 52px;
        background: url('chart-types.png') -146px -78px;
    }

    .bg-chart {
        padding-left: 60px;
        padding-top: 15px;
        white-space: nowrap;
    }

    .chart-properties {
        font-size: .8em
    }
</style>