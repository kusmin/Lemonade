<template lang="">
    <div style="overflow-x: hidden;">
        <div>
            <div class="d-flex justify-content-between align-items-center border-bottom">
                <div class="title">
                    <h1>Construção de Modelos</h1>
                </div>
                <form class="float-right form-inline w-50 d-flex justify-content-end">
                    <label>{{$tc('common.name')}}:</label>
                    <input type="text" class="form-control form-control-sm ml-1 w-50" :placeholder="$tc('common.name')"
                        v-model="workflowObj.name" maxlength="100">
                    <button class="btn btn-sm btn-outline-success ml-1 float-right" @click.prevent="saveWorkflow"><span
                            class="fa fa-save"></span>
                        {{$t('actions.save')}}</button>

                    <button v-if="notRunning" @click.prevent="handleTraining"
                        class="btn btn-sm btn-outline-primary ml-1 float-right"><span class="fa fa-play"></span>
                        {{$t('actions.train')}}</button>

                    <button v-else @click.prevent="handleStopTrain"
                        class="btn btn-sm btn-outline-danger ml-1 float-right"><span class="fa fa-stop"></span>
                        {{$t('actions.stop')}}</button>

                    <button @click.prevent="loadJobs" class="btn btn-sm btn-outline-secondary ml-1 float-right"><span
                            class="fa fa-sync"></span>
                        Reload jobs</button>
                </form>
            </div>
            <div class="custom-card">
                <b-tabs v-if="loaded" class="p-2 custom-tab bg-white" align="center">
                    <b-tab title="Parâmetros" class="m-1 parameters">
                        <div class="row size-full">
                            <div class="col-md-3 col-lg-2 border-right">
                                <div class="explorer-nav p-1">
                                    <SideBar :selected="selected" @edit="edit" :supervisioned="supervisioned"/>
                                </div>
                            </div>
                            <div class="col-md-9 col-lg-10 pl-4 pr-4 bg-white expand">
                                <form action="" class="form p-2">
                                    <template v-if="selected === 'target'">
                                        <DesignData :attributes="attributes" :dataSourceList="dataSourceList"
                                            :supervisioned="supervisioned" :label="labelAttribute"
                                            :data-source="dataSource" :sample="workflowObj.sample"
                                            @search-data-source="loadDataSourceList"
                                            @retrieve-attributes="handleRetrieveAttributes" />
                                    </template>
                                    <template v-if="selected === 'data'">
                                        <TrainTest :split="workflowObj.split" />
                                    </template>
                                    <template v-if="selected === 'metric'">
                                        <Metric :evaluator="workflowObj.evaluator" :attributes="attributes" />
                                    </template>
                                    <template v-if="selected === 'adjusts'">
                                        <FeatureSelection :attributes="attributes" :features="workflowObj.features"
                                            :target="workflowObj.forms.$meta.value.target"
                                            @update-target="handleUpdateTarget" 
                                            :supervisioned="supervisioned"/>
                                    </template>
                                    <template v-if="selected === 'generation'">
                                        <FeatureGeneration />
                                    </template>
                                    <template v-if="selected === 'reduction'">
                                        <FeatureReduction :reduction="workflowObj.reduction" />
                                    </template>
                                    <template v-if="selected === 'algorithms'">
                                        <Algorithms :operations="algorithmOperation" :workflow="workflowObj"
                                            :operation-map="operationsMap" />
                                    </template>
                                    <template v-if="selected === 'grid'">
                                        <Grid :grid="workflowObj.grid" />
                                    </template>
                                    <template v-if="selected === 'weighting'">
                                        <Weighting />
                                    </template>
                                    <template v-if="selected === 'runtime'">
                                        <Runtime :clusters="clusters" />
                                    </template>
                                </form>
                            </div>
                        </div>
                    </b-tab>
                    <b-tab title="Resultados" class="pt-2" ref="tabResults">
                        <Result :jobs="jobs" ref="results"
                            :number-of-features="numberOfFeatures"
                            @delete-job="handleDeleteJob" />
                    </b-tab>
                </b-tabs>
            </div>
        </div>
    </div>
</template>
<script>
    import Vue from 'vue';
    import io from 'socket.io-client';
    import SideBar from './SideBar';
    import DesignData from './DesignData';
    import TrainTest from './TrainTest';
    import Metric from './Metric';
    import FeatureSelection from './FeatureSelection';
    import FeatureGeneration from './FeatureGeneration';
    import FeatureReduction from './FeatureReduction';
    import Algorithms from './Algorithms';
    import Grid from './Grid';
    import Runtime from './Runtime';
    import Result from './result/Result';
    import Weighting from './Weighting';

    import InputHeader from '../../../components/InputHeader.vue';
    import DataSourceMixin from '../DataSourceMixin.js';
    import VuePerfectScrollbar from 'vue-perfect-scrollbar'
    import { debounce } from "../../../util.js";
    import Notifier from '../../../mixins/Notifier.js';

    import { ModelBuilderWorkflow, Operation } from '../entities.js';

    import axios from 'axios';
    import vSelect from 'vue-select';
    const limoneroUrl = process.env.VUE_APP_LIMONERO_URL;
    const tahitiUrl = process.env.VUE_APP_TAHITI_URL;
    const standUrl = process.env.VUE_APP_STAND_URL;
    const standNamespace = process.env.VUE_APP_STAND_NAMESPACE;
    const META_PLATFORM_ID = 1000;

    export default {
        components: {
            InputHeader, 'vue-select': vSelect,
            SideBar, DesignData, TrainTest, Metric, FeatureSelection, FeatureGeneration,
            FeatureReduction, Algorithms, Grid, Runtime, Weighting, Result
        },
        mixins: [DataSourceMixin, Notifier],
        computed: {
            algorithmOperation() {
                const taskType = this.workflowObj.forms.$meta.value.taskType || 'classification';
                return Array.from(this.operationsMap.values()).filter((op) => op.categories.find(cat => cat.subtype === taskType));
            },
            dataSourceId: {
                get() { return this.workflowObj.tasks[0].forms.data_source.value; },
                set(newValue) { this.workflowObj.tasks[0].forms.data_source.value = newValue }
            },
            supervisioned() {
                return this.taskType === 'regression' || this.taskType === 'classification';
            },
            taskType: {
                get() { return this.workflowObj.forms.$meta.value.taskType; },
                set(newValue) {
                    return this.$store.dispatch('dataExplorer/setTaskName', newValue)
                }
            },
            numberOfFeatures(){
                return this.workflowObj?.features?.forms?.features?.value?.length || 0;
            }
        },
        data() {
            return {
                attributes: [],
                clusters: [],
                dataSource: null,
                dataSourceOptions: [],
                internalWorkflowId: null,
                isDirty: false,
                job: null,
                jobs: [],
                groupedJobs: null,
                labelAttribute: '',
                loaded: false,
                loadingData: false,
                notRunning: true,
                operationsMap: new Map(),
                selectedAlgorithm: { forms: [] },
                selected: 'target',
                socket: null, // used by socketio (web sockets)
                targetPlatform: 1,
                workflowObj: { forms: { $meta: { value: { target: '', taskType: '' } } } },

                //FIXME: hard-coded. It'd be best defined in Tahiti
                unsupportedParameters: new Set(['perform_cross_validation', 'cross_validation', 'one_vs_rest'])
            }
        },
        async created() {
            this.internalWorkflowId = (this.$route) ? this.$route.params.id : 0;
            await this.load();
        },
        beforeDestroy() {
            this.disconnectWebSocket();
        },
        methods: {
            /* WebSocket Handling */
            disconnectWebSocket() {
                if (this.socket) {
                    this.socket.emit('leave', { room: this.job.id });
                    this.socket.close();
                }
            },
            changeRoom(room) {
                this.socket.emit('join', { cached: false, room });
            },
            connectWebSocket() {
                const self = this;
                if (self.socket === null) {
                    const socket = io(standNamespace, { upgrade: true, });
                    self.socket = socket;

                    socket.on('connect', () => { socket.emit('join', { cached: false, room: self.job.id }); });

                    socket.on('task result', (msg, callback) => {
                        //const task = self.workflowObj.getTaskById(msg.id);
                        this.jobs[0].results.push({
                            task_id: msg.id,
                            operation_id: msg.operation_id,
                            title: msg.title,
                            type: msg.type,
                            content: msg.message
                        })
                        this.jobs[0].groupedResults = this.jobs[0].results.reduce((rv, x) => {
                            const key = `${x.task_id}:${x.title}`;
                            (rv[key] = rv[key] || []).push(x);
                            return rv;
                        }, {});
                        this.$refs.results.selectFirst();
                    });
                    socket.on('update job', msg => {
                        if (msg.status === 'ERROR') {
                            self.error(msg);
                            self.notRunning = true;
                        }
                        if (msg.status === 'COMPLETED') {
                            self.jobStatus = msg.message;
                            self.notRunning = true;
                        }
                        //self.job && (self.job.status = msg.status);
                        this.loadJobs();
                    });
                } else if (self.job) {
                    self.changeRoom(self.job.id);
                }
            },
            async handleTraining() {
                this.$refs.tabResults.activate();
                const self = this;
                const cloned = JSON.parse(JSON.stringify(this.workflowObj));
                cloned.platform_id = cloned.platform.id; //FIXME: review
                cloned.preferred_cluster_id = self.workflowObj.preferred_cluster_id;

                cloned.tasks = cloned.tasks.filter((task) => task.enabled);
                cloned.tasks.forEach((task) => {
                    if (task.enabled && task.previewable) {
                        // Remove unnecessary attributes from operation
                        task.operation = { id: task.operation.id };
                        delete task.version;
                    }
                });
                const body = {
                    workflow: cloned,
                    cluster: { id: self.workflowObj.preferred_cluster_id }, //FIXME: How to determine the cluster?
                    name: `## model builder ${self.workflowObj.id} ##`,
                    user: this.$store.getters.user,
                    persist: true,
                    type: 'MODEL_BUILDER',
                    app_configs: { verbosity: 0 },
                }
                try {
                    const response = await axios.post(`${standUrl}/jobs`, body,
                        { headers: { 'Locale': self.$root.$i18n.locale, } })
                    self.jobs.splice(0, 0, response.data.data);
                    self.job = response.data.data;
                    self.success('Construção dos modelos foi iniciada.');
                    this.notRunning = false;
                    this.$refs.results.selectFirst();
                    self.connectWebSocket();
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
            async load() {
                this.loadingData = true;
                this.$Progress.start()
                try {
                    await this.loadOperations();
                    let resp = await axios.get(`${tahitiUrl}/workflows/${this.internalWorkflowId}`)
                    this.workflowObj = new ModelBuilderWorkflow(resp.data, this.operationsMap);
                    if (this.workflowObj.type !== 'MODEL_BUILDER') {
                        this.error(null, this.$tc('modelBuilder.invalidType'));
                        this.$router.push({ name: 'index-explorer' })
                        return;
                    }
                    await this.loadDataSource(this.dataSourceId);
                    this.labelAttribute = this.workflowObj.forms.$meta.value.label;
                    const evaluator = this.workflowObj.tasks.find(t => t.operation.slug === 'evaluator');
                    if (evaluator && ! evaluator?.forms?.task_type?.value){
                        evaluator.forms.task_type.value = this.workflowObj.forms.$meta.value.taskType;
                    }

                    await this.loadJobs();

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
            async loadJobs() {
                const params = {
                    workflow_id: this.internalWorkflowId, sort: 'updated',
                    asc: false, size: 10
                };
                const resp = await axios.get(`${standUrl}/jobs`, { params });


                const runningStatuses = ['RUNNING', 'PENDING', 'WAITING'];
                resp.data.data.forEach(job => {
                    if (this.job === null && runningStatuses.indexOf(job.status) > -1) {
                        this.job = job;
                    }
                    job.results.forEach(result => {
                        if (result?.content) {
                            result.content = JSON.parse(result.content);
                        }
                    });
                    job.results.sort((a, b) => a.t - b.t);
                    job.groupedResults = job.results.reduce((rv, x) => {
                        const key = `${x.task_id}:${x.title}`;
                        (rv[key] = rv[key] || []).push(x);
                        return rv;
                    }, {});
                    Object.entries(job.groupedResults).forEach(([id, results]) => {
                        let result0 = results[0];
                        const isLargerBetter = Boolean(result0.content.metric && result0.content.metric.isLargerBetter);
                        let best = result0.content.metric ? result0.content.metric.value : 0;
                        results.forEach(r => {
                            if (r.content.metric && 
                                    (isLargerBetter && r.content.metric.value > best 
                                        || !isLargerBetter && r.content.metric.value < best)) {
                                best = r.content.metric.value;
                            }
                        });
                        Vue.set(result0, 'best', best);

                    });
                });
                this.jobs = resp.data.data;
                if (this.$refs.results) {
                    this.$refs.results.selectFirst();
                }

                this.notRunning = this.jobs.length === 0 || this.jobs.every(job => runningStatuses.indexOf(job.status) === -1);
                if (this.job) {
                    this.connectWebSocket();
                }
            },
            async loadOperations() {
                const params = {
                    category: 'model-builder', platform: META_PLATFORM_ID,
                    fields: 'id,forms,categories,name,slug'
                };

                const resp = await axios.get(`${tahitiUrl}/operations`, { params });
                resp.data.data.forEach(op => this.operationsMap.set(op.slug, new Operation(op)));
            },
            async loadDataSource(id) {
                const resp = await axios.get(`${limoneroUrl}/datasources/${id}`);
                this.dataSource = resp.data;
                this.attributes = this.dataSource.attributes; //.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
            },
            async loadClusters() {
                try {
                    const resp = await axios.get(`${standUrl}/clusters?enabled=true&platform=${this.targetPlatform}`)
                    this.clusters = resp.data.data;
                } catch (ex) {
                    this.error(ex);
                }
            },
            edit(option) {
                this.selected = option;
            },
            getWidget(field) {
                if (field.suggested_widget.endsWith(':read-only')) {
                    const s = field.suggested_widget;
                    return s.substring(0, s.length - 10) + '-component';
                } else {
                    return field.suggested_widget + '-component';
                }
            },
            async saveWorkflow() {
                let cloned = JSON.parse(JSON.stringify(this.workflowObj));
                let url = `${tahitiUrl}/workflows/${cloned.id}`;

                cloned.preferred_cluster_id = 1; //FIXME! 
                cloned.platform_id = META_PLATFORM_ID;

                cloned.tasks.forEach((task) => {
                    task.operation = { id: task.operation.id };
                    delete task.version;
                    delete task.step;
                    delete task.status;
                });
                // Required in order to be able to generate hyperparams
                cloned.forms.$grid = {
                    value: {
                        strategy: this.workflowObj.grid.forms.strategy?.value,
                        max_iterations: this.workflowObj.grid.forms.max_iterations?.value,
                    }
                }

                try {
                    const resp = await axios.patch(url, cloned, { headers: { 'Content-Type': 'application/json' } });
                    this.isDirty = false;
                    this.success(this.$t('messages.savedWithSuccess', { what: this.$tc('titles.workflow') }));
                } catch (e) {
                    this.error(e);
                }
            },
            getFieldValue(field) {
                //FIXME
                return null;
            },
            selectAlgorithm(algo) {
                this.selectedAlgorithm = algo;
            },
            handleRetrieveAttributes(ds) {
                this.dataSourceId = ds.id;
                this.loadDataSource(ds.id);
            },
            handleUpdateTarget(target) {
                this.workflowObj.forms.$meta.value.target = target;
            },
            async handleDeleteJob(job_id, selected) {
                this.confirm(
                    this.$t('actions.delete'),
                    this.$tc('titles.job') + "?",
                    async () => {
                        let resp = await axios.delete(`${standUrl}/jobs/${job_id}`);
                        this.loadJobs();
                        this.$refs.results.selectFirst();
                    },
                );
            },
            handleStopTrain() {
                const confirm = () => {
                    this.jobs.forEach(async job => {
                        if (job.status === 'RUNNING' || job.status === 'PENDING' || job.status === 'WAITING') {
                            await axios.post(`${standUrl}/jobs/${job.id}/stop`);
                            job.status = 'CANCELED';
                        }
                    });
                    this.notRunning = true;
                };
                this.confirm(
                    this.$t('actions.stop'),
                    this.$t('messages.doYouWantToStop'),
                    confirm,
                );
            },
        },
        watch: {
            async selected() {
                if (this.selected === 'algorithms') {
                    const params = {
                        enabled: 'true',
                        platform: 1, //FIXME
                        category: this.taskType,
                        lang: this.$locale,
                    }
                    const resp = await axios.get(
                        `${tahitiUrl}/operations`, { params });
                    //this.algorithms = resp.data;
                    //this.selectedAlgorithm = this.algorithms[0];
                }
            }
        }
    }
</script>

<style scoped>
    .custom-card {
        padding: 0 5px;
    }

    h5 {
        font-size: 14pt;
    }

    h5,
    h6 {
        color: #888;
    }

    form {
        font-size: 11pt;
    }

    .editor {
        border-bottom: 1px dashed;
        border-color: #888;
    }

    .parameters label {
        margin-top: 10px;
    }

    .scroll-area {
        xborder: 1px solid #ccc;
        max-height: calc(100vh - 320px);
        padding: 10px 15px 10px 10px;
    }

    .active-item {
        background-color: #e7f3ff
    }

    .size-full>div {
        height: calc(100vh - 220px);
    }

    .expand {
        display: table;
    }
</style>