<template>
    <main role="main">
        <div>
            <div class="d-flex justify-content-between align-items-center">
                <h1><span class="fa fa-vial"></span> {{$tc('dataExplorer.tagline', 1)}}</h1>
            </div>
            <hr>
            <div class="card-deck ">
                <b-card class="clickable m-1" role="button">
                    <div class="row">
                        <div class="col-md-4 col-sm-12 col-lg-3">
                            <span class="fa-stack fa-2x">
                                <span class="fas fa-circle text-primary fa-stack-2x"></span>
                                <span class="fas fa-table fa-stack-1x fa-inverse"></span>
                            </span>
                        </div>
                        <div class="col-md-9 mt-2" @click="navigate('data-explorer')">
                            <h5>Analisar, tratar e transformar dados</h5>
                            <small>
                                Utilize uma interface amigável e responsiva para tratar os dados. Você poderá
                                experimentar
                                como transformar os dados, obtendo um retorno imediato (usa amostra dos dados).
                            </small>
                        </div>
                    </div>
                </b-card>
                <b-card class="clickable m-1" @click="navigate('choose-task')" role="button">
                    <div class="row">
                        <div class="col-md-4 mt-2 col-sm-12 col-lg-3">
                            <span class="fa-stack fa-2x">
                                <span class="fas fa-circle text-success fa-stack-2x"></span>
                                <span class="fas fa-robot fa-stack-1x fa-inverse"></span>
                            </span>
                        </div>
                        <div class="col-md-9 mt-2">
                            <h5>Criar modelo de aprendizado de máquina</h5>
                            <small>
                                Crie modelos de aprendizado de máquina, definindo qual tarefa e algoritmos aplicar,
                                quais <em>features</em> usar e quais métricas lhe
                                darão o melhor modelo.
                            </small>
                        </div>
                    </div>
                </b-card>
                <b-card class="clickable m-1" @click="navigate('new-visualization')" role="button">
                    <div class="row">
                        <div class="col-md-4 col-sm-12 col-lg-3">
                            <span class="fa-stack fa-2x">
                                <span class="fas fa-circle text-danger fa-stack-2x"></span>
                                <span class="fas fa-chart-bar fa-stack-1x fa-inverse"></span>
                            </span>
                        </div>
                        <div class="col-md-9 mt-2">
                            <h5>Criar visualizações de dados</h5>
                            <small>
                                Monte gráficos, tabelas e outras visualizações de dados.
                                Associe-os a <em>dashboards</em> e compartilhe-os com outros usuários.
                            </small>
                        </div>
                    </div>
                </b-card>
                <!--
                <b-card class="clickable m-1">
                    <div class="row">
                        <div class="col-md-4 col-sm-12 col-lg-3">
                            <span class="fa-stack fa-2x">
                                <span class="fas fa-circle text-warning fa-stack-2x"></span>
                                <span class="fas fa-trophy fa-stack-1x fa-inverse"></span>
                            </span>
                        </div>
                        <div class="col-md-9 mt-2">
                            <h5>Aplicar ou avaliar um modelo usando um conjunto novo de dados</h5>
                            <small>
                                Utilize uma interface bla bla bla para tratar os dados. Você poderá experimentar
                                como
                                transformar bla bla
                            </small>
                        </div>
                    </div>
                </b-card>
                -->
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-md-12 custom-table">
                <b-card>
                    <h5>Ou você quer editar algo existente?</h5>

                    <form class="form-inline">

                        <label class="sr-only" for="type">{{$tc('common.type')}}</label>
                        <select class="form-control w-25 pt-0" v-model="typeFilter">
                            <option selected disabled>{{$tc('actions.choose')}}...</option>
                            <option value="DATA_EXPLORER">{{$t('dataExplorer.experiments.DATA_EXPLORER')}}</option>
                            <option value="MODEL_BUILDER">{{$t('dataExplorer.experiments.MODEL_BUILDER')}}</option>
                            <option value="VIS_BUILDER">{{$t('dataExplorer.experiments.VIS_BUILDER')}}</option>
                        </select>
                        <label class="sr-only" for="search">{{$tc('common.name')}}</label>
                        <input type="text" class="form-control m-2 w-25" :placeholder="$tc('common.name')"
                            v-model="searchFilter">
                        <button @click.prevent="search" ref="searchBtn"
                            class="btn btn-secondary btn-sm mb-2 btn-spinner">
                            <span class="fa fa-search default-icon"></span> {{$t('actions.search')}}
                            <font-awesome-icon icon="spinner" pulse class="icon" />
                        </button>
                    </form>


                    <v-server-table v-show="totalRecords > 0" :columns="columns" :options="options" ref="workflowList"
                        name="workflowListDataExplorer">
                        <template slot="id" slot-scope="props">
                            <router-link v-if="props.row.type === 'DATA_EXPLORER' "
                                :to="{name: 'data-explorer-panel', params: {id: props.row.id, platform: props.row.platform.id}}">
                                {{props.row.id}}</router-link>
                            <router-link v-if="props.row.type === 'MODEL_BUILDER' "
                                :to="{name: 'model-design', params: {id: props.row.id, platform: props.row.platform.id}}">
                                {{props.row.id}}</router-link>
                            <router-link v-if="props.row.type === 'VIS_BUILDER' "
                                :to="{name: 'visualization-design', params: {id: props.row.id, platform: props.row.platform.id}}">
                                {{props.row.id}}</router-link>
                        </template>
                        <template slot="type" slot-scope="props">
                            {{$t(`dataExplorer.experiments.${props.row.type}`)}}
                        </template>
                        <template slot="name" slot-scope="props">
                            <router-link v-if="props.row.type === 'DATA_EXPLORER' "
                                :to="{name: 'data-explorer-panel', params: {id: props.row.id, platform: props.row.platform.id}}">
                                {{props.row.name}}</router-link>
                            <router-link v-if="props.row.type === 'MODEL_BUILDER' "
                                :to="{name: 'model-design', params: {id: props.row.id, platform: props.row.platform.id}}">
                                {{props.row.name}}</router-link>
                            <router-link v-if="props.row.type === 'VIS_BUILDER' "
                                :to="{name: 'visualization-design', params: {id: props.row.id, platform: props.row.platform.id}}">
                                {{props.row.name}}</router-link>
                        </template>
                        <template slot="updated" slot-scope="props">{{props.row.updated | formatJsonDate}}</template>
                    </v-server-table>
                    <div v-show="totalRecords === 0">{{$t('common.noData')}}</div>
                </b-card>
            </div>
        </div>
    </main>
</template>
<script>
    import axios from 'axios';
    import Notifier from '../../mixins/Notifier';
    import { Event } from 'vue-tables-2';

    let tahitiUrl = process.env.VUE_APP_TAHITI_URL;
    const META_PLATFORM_SLUG = 'meta';
    export default {
        mixins: [Notifier],
        methods: {
            search(event) {
                this.$refs.workflowList.refresh()
            },
            navigate(name) {
                this.$router.push({ name })
            },
            clearFilters() {
                this.$refs.workflowList.setFilter('');
                this.$refs.workflowList.customQueries = {};
            },
        },
        data() {
            const self = this;
            return {
                totalRecords: 0,
                searchFilter: null,
                typeFilter: null,
                columns: [
                    'id',
                    'name',
                    'type',
                    'updated',
                    'version',
                ],
                options: {
                    hidePerPageSelect: true,
                    debounce: 800,
                    skin: 'table-sm table table-hover',
                    dateColumns: ['updated'],
                    headings: {
                        id: 'ID',
                        name: this.$tc('common.name'),
                        type: this.$tc('common.type'),
                        updated: this.$tc('common.updated'),
                        version: this.$tc('common.version'),
                    },
                    sortable: ['name', 'id', 'updated'],
                    //filterable: ['name', 'id'],
                    filterable: [],
                    sortIcon: {
                        base: 'fa fas',
                        is: 'fa-sort ml-10',
                        up: 'fa-sort-amount-up',
                        down: 'fa-sort-amount-down'
                    },
                    preserveState: true,
                    saveState: true,
                    filterByColumn: false,

                    requestFunction: function (data) {
                        self.$refs.searchBtn.classList.remove('btn-spinner');
                        data.sort = data.orderBy;
                        data.asc = data.ascending === 1 ? 'true' : 'false';
                        data.size = 5;
                        data.name = self.searchFilter //data.query;
                        data.platform = META_PLATFORM_SLUG;
                        if (self.typeFilter) {
                            data.types = self.typeFilter;
                        } else {
                            data.types = 'experiment';
                        }

                        data.fields = 'id,name,platform,updated,user,version,description,type';
                        data.enabled = 1;

                        let url = `${tahitiUrl}/workflows`;
                        self.$Progress.start();
                        return axios
                            .get(url, {
                                params: data
                            })
                            .then(resp => {
                                self.$Progress.finish();
                                self.totalRecords = resp.data.pagination.total;
                                return {
                                    data: resp.data.data,
                                    count: resp.data.pagination.total
                                };
                            })
                            .catch(
                                function (e) {
                                    self.$Progress.finish();
                                    self.error(e);
                                }.bind(this)
                            ).finally(() => self.$refs.searchBtn.classList.add('btn-spinner'));
                    },
                    texts: {
                        filter: this.$tc('common.filter'),
                        count: this.$t('common.pagerShowing'),
                        limit: this.$t('common.limit'),
                        noResults: this.$t('common.noData'),
                        loading: this.$t('common.loading'),
                        filterPlaceholder: this.$t('common.filterPlaceholder')
                    }
                }
            };
        },
    }
</script>
<style scoped>
    .custom-table>>>.VueTables .row:first-child {
        margin: initial !important;
        background-color: white;
        padding-top: 0;
    }
</style>