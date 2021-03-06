<template>

    <div class="options-container">
        <div class="options-visualization">
            <div class="title border-bottom">
                <h5>Construção de Visualização</h5>
            </div>
            <br />
            <div>
                <form class="clearfix visualization-form">
                    <b-card sub-title="Dados básicos">
                        <label>{{$tc('common.title')}}:</label>
                        <input type="text" class="form-control form-control-sm" :placeholder="$tc('common.name')"
                            v-model="workflowObj.name" maxlength="100">

                        <label for="">Fonte de dados:</label> &nbsp;
                        <vue-select v-if="workflowObj && workflowObj.readData" @search="loadDataSourceList"
                            :filterable="false" :options="dataSourceList" :reduce="(opt) => opt.id" label="name"
                            v-model="workflowObj.readData.forms.data_source.value" @input="retrieveAttributes">

                            <template v-slot:no-options="{ search, searching }">
                                <small>Digite parte do nome pesquisar ...</small>
                            </template>
                            <template slot="option" slot-scope="option">
                                <div class="d-center">
                                    <span class="span-id">{{ pad(option.id, 4, '&nbsp;') }}</span> - {{
                                    option.name }}
                                </div>
                            </template>
                            <template slot="selected-option" slot-scope="option">
                                <div class="selected d-center">
                                    {{ pad(option.id, 4, '&nbsp;') }} - {{ option.name }}
                                </div>
                            </template>
                        </vue-select>

                        <label>{{$tc('titles.cluster')}}: </label>
                        <v-select :options="clusters" v-model="workflowObj.preferred_cluster_id" label="name"
                            :reduce="(opt) => opt.id" :taggable="false" :close-on-select="true" :filterable="false">
                            <template #option="{ description, id, name, type }">
                                {{ name }}<br />
                                <small><em>{{ description }}</em></small>
                            </template>
                        </v-select>
                    </b-card>
                    <b-card class="mt-1" sub-title="Consulta (opcional)" v-if="loaded">
                        <label>Limitar quantidade de registros:</label>
                        <input type="number" class="form-control form-control-sm w-50" maxlength="10"
                            v-model.numeric="workflowObj.sample.forms.value.value" step="100" />

                        <ExpressionEditor :field="filterField" :value="workflowObj.filter.forms.formula.value"
                            :suggestionEvent="() => attributes.map(a=>a.name)" @update="handleUpdateFilter" />

                        <!--
                        <template>
                            <label class="mt-2">Agrupar por:</label>
                            <v-select :options="attributes" label="name" :reduce="(opt) => opt.name" :multiple="true"
                                v-model="workflowObj.group.forms.attributes.value">
                                <template #option="{name, type}">
                                    <font-awesome-icon class="mr-2" prefix="fa" :icon="getIcon({type})" />{{name}}
                                </template>

                                <template #selected-option="{name, type}">
                                    <div role="button">
                                        <font-awesome-icon class="mr-2" prefix="fa" :icon="getIcon({type})" />{{name}}
                                    </div>
                                </template>
                            </v-select>
                        </template>
                        -->

                    </b-card>

                </form>
            </div>
            <div class="mt-2 ">
                <button class="btn btn-sm btn-primary ml-1 mr-5" @click.prevent="loadData">
                    <span class="fa fa-search"></span>
                    {{$t('actions.search')}}</button>

                <button class="btn btn-sm btn-outline-success ml-1 float-right" @click.prevent="saveWorkflow"><span
                        class="fa fa-save"></span>
                    {{$t('actions.save')}}</button>

                <router-link class="btn btn-sm btn-outline-secondary ml-1 float-right" :to="{name: 'index-explorer'}"
                    :title="$t('actions.back')">{{$t('actions.back')}}</router-link>

            </div>
        </div>
        <div class="options-main">
            <div class="chart">
                <chart-builder-visualization />
            </div>
        </div>
        <div class="options-visualization">
            <div>
                <chart-builder-options :attributes="attributes" :workflow="workflowObj" />
            </div>
        </div>
    </div>


    </div>

</template>

<script>
    import ChartBuilderVisualization from '../../../components/chart-builder/ChartBuilderVisualization.vue';
    import ChartBuilderOptions from '../../../components/chart-builder/ChartBuilderOptions.vue';

    import Vue from 'vue';
    import io from 'socket.io-client';

    import InputHeader from '../../../components/InputHeader.vue';
    import ExpressionEditor from '../../../components/widgets/ExpressionEditor.vue';
    import DataSourceMixin from '../DataSourceMixin.js';
    import { debounce } from "../../../util.js";
    import Notifier from '../../../mixins/Notifier.js';

    import { Workflow, Operation, VisualizationBuilderWorkflow } from '../entities.js';
    import axios from 'axios';
    import vSelect from 'vue-select';
    const limoneroUrl = process.env.VUE_APP_LIMONERO_URL;
    const tahitiUrl = process.env.VUE_APP_TAHITI_URL;
    const standUrl = process.env.VUE_APP_STAND_URL;
    const standNamespace = process.env.VUE_APP_STAND_NAMESPACE;
    const META_PLATFORM_ID = 1000;

    export default {
        mixins: [DataSourceMixin, Notifier],
        components: {
            'vue-select': vSelect,
            ChartBuilderVisualization,
            ChartBuilderOptions,
            ExpressionEditor
        },
        computed: {
            dataSourceId: {
                get() { return this.workflowObj.readData.forms.data_source.value; },
                set(newValue) { this.workflowObj.readData.forms.data_source.value = newValue }
            },
        },
        data() {
            return {
                attributes: [],
                clusters: [],
                clusterId: null,
                dataSource: null,
                dataSourceOptions: [],
                filterField: { label: 'Filtrar', values: '{"alias": false}' },
                group: false,
                internalWorkflowId: null,
                isDirty: false,
                job: null,
                jobs: [],
                groupedJobs: null,
                loaded: false,
                loadingData: false,
                notRunning: true,
                operationsMap: new Map(),
                socket: null, // used by socketio (web sockets)
                targetPlatform: 1,
                workflowObj: { forms: { $meta: { value: { target: '', taskType: '' } } } },
            }
        },
        async created() {
            this.internalWorkflowId = (this.$route) ? this.$route.params.id : 0;
            await this.load();
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

                }
            },
            async load() {
                this.loadingData = true;
                this.$Progress.start()
                try {
                    await this.loadOperations();
                    let resp = await axios.get(`${tahitiUrl}/workflows/${this.internalWorkflowId}`);
                    this.workflowObj = new VisualizationBuilderWorkflow(resp.data, this.operationsMap);
                    if (this.workflowObj.type !== 'VIS_BUILDER') {
                        this.error(null, this.$tc('modelBuilder.invalidType'));
                        this.$router.push({ name: 'index-explorer' })
                        return;
                    }
                    await this.loadDataSource(this.dataSourceId);

                    const self = this;
                    const attributes = this.dataSource.attributes;
                    self.workflowObj.group.forms.function.value.forEach(attr => {
                        attr['name'] = attr.attribute;
                        const v = attributes.find(a => a.name === attr.name);
                        attr['type'] = v ? v.type : '';
                    });
                    this.loadClusters();
                    this.loaded = true;
                } catch (e) {
                    this.error(e);
                    this.$router.push({ name: 'index-explorer' })
                } finally {
                    Vue.nextTick(() => {
                        this.$Progress.finish();
                        this.loadingData = false;
                        this.isDirty = false;
                    });
                }
            },
            async loadOperations() {
                const params = {
                    category: 'visualization-builder', platform: META_PLATFORM_ID,
                    fields: 'id,forms,categories,name,slug'
                };

                const resp = await axios.get(`${tahitiUrl}/operations`, { params });
                resp.data.data.forEach(op => this.operationsMap.set(op.slug, new Operation(op)));
            },
            async loadDataSource(id) {
                const resp = await axios.get(`${limoneroUrl}/datasources/${id}`);
                this.dataSource = resp.data;
                this.attributes = this.dataSource.attributes.sort((a, b) => a.name.localeCompare(b.name));
                this.attributes.forEach(a => a.attribute = a.name);
                this.dataSourceList = [this.dataSource];
            },
            async loadClusters() {
                try {
                    const resp = await axios.get(`${standUrl}/clusters?enabled=true&platform=${this.targetPlatform}`)
                    this.clusters = resp.data.data;
                } catch (ex) {
                    this.error(ex);
                }
            },
            async saveWorkflow() {
                let cloned = JSON.parse(JSON.stringify(this.workflowObj));
                let url = `${tahitiUrl}/workflows/${cloned.id}`;

                cloned.platform_id = META_PLATFORM_ID;

                cloned.tasks.forEach((task) => {
                    task.operation = { id: task.operation.id };
                    delete task.version;
                    delete task.step;
                    delete task.status;
                });

                try {
                    const resp = await axios.patch(url, cloned, { headers: { 'Content-Type': 'application/json' } });
                    this.isDirty = false;
                    this.success(this.$t('messages.savedWithSuccess', { what: this.$tc('titles.workflow') }));
                } catch (e) {
                    this.error(e);
                }
            },
            handleUpdateFilter(field, value) {
                this.workflowObj.filter.forms.formula.value = value;
            },
            async loadData() {
                const self = this;
                self.loadingData = true;
                const cloned = JSON.parse(JSON.stringify(this.workflowObj));
                cloned.platform_id = cloned.platform.id; //FIXME: review

                cloned.tasks.forEach((task) => {
                    // Remove unnecessary attributes from operation
                    task.operation = { id: task.operation.id };
                    delete task.version;
                });

                const body = {
                    workflow: cloned,
                    cluster: { id: cloned.preferred_cluster_id },
                    name: `## vis explorer ${self.workflowObj.id} ##`,
                    user: this.$store.getters.user, //: { id: user.id, login: user.login, name: user.name },
                    persist: false, // do not save the job in db.
                    app_configs: { verbosity: 0, target_platform: 'scikit-learn' },
                }

                try {
                    const response = await axios.post(`${standUrl}/jobs`, body,
                        { headers: { 'Locale': self.$root.$i18n.locale, } })
                    self.job = response.data.data;
                    //self.connectWebSocket();
                } catch (ex) {
                    if (ex.data) {
                        self.error(ex.data.message);
                    } else if (ex.status === 0) {
                        self.$root.$refs.toastr.e(`Error connecting to the backend (connection refused).`);
                    } else {
                        self.error(`Unhandled error: ${JSON.stringify(ex)}`);
                    }
                } finally {
                    self.$Progress.finish();
                }
            },
        }
    }

</script>

<style scoped lang="scss">
    #chart-builder {
        width: 100%;
        height: calc(100vh - 110px);
        display: flex;

        .visualization-builder {
            width: 550px;
        }

        /*
        .datasource {
            overflow: auto;
            width: 250px;
            padding-right: 1rem;
            border-right: 1px solid rgba(black, .08);
        }

        .options {
            width: 300px;
            padding: 0 2rem;

            .type-selector {
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid rgba(black, .08);
            }
        }*/

        .visualization {
            width: 100%;
            display: flex;
            flex-direction: column;

            div {
                width: 100%;
            }

            .chart {
                height: 100%;
            }
        }
    }

    .options-visualization {
        flex: 0 0 350px;
        background-color: #fff;
        padding: 5px;
    }

    .options-container {
        display: flex;
        flex-wrap: wrap;
        margin: 0 auto;
        gap: 10px;
    }

    .options-main {
        flex: 3;
    }

    .visualization-form {
        font-size: .8em;
    }
</style>