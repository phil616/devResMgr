<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title>设置二级域名</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="setSLD">
          <v-row>
            <v-col cols="12" sm="8">
              <v-text-field
                v-model="sldDomain"
                label="二级域名 (例如: example.com)"
                outlined
                dense
                :rules="[v => !!v || '请输入二级域名']"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="4">
              <v-btn color="primary" @click="setSLD" :loading="loading.sld">设置</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card class="mb-4">
      <v-card-title>添加域名记录</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createDomain">
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="newDomain.prefix"
                label="前缀 (例如: www)"
                outlined
                dense
                :rules="[v => !!v || '请输入前缀']"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="newDomain.a_record"
                label="IPv4地址"
                outlined
                dense
                :rules="[
                  v => !!v || '请输入IPv4地址',
                  v => /^(\d{1,3}\.){3}\d{1,3}$/.test(v) || 'IPv4地址格式不正确'
                ]"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-btn color="success" @click="createDomain" :loading="loading.create">添加</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>
        域名记录
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="搜索"
          single-line
          hide-details
          outlined
          dense
          class="ml-2"
        ></v-text-field>
        <v-btn icon class="ml-2" @click="fetchDomains" :loading="loading.fetch">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="domains"
        :search="search"
        :loading="loading.fetch"
        class="elevation-1"
      >
        <!-- eslint-disable-next-line vue/valid-v-slot -->
        <template #item.proxied="{ item }">
          <v-chip :color="item.proxied ? 'success' : 'error'" small>
            {{ item.proxied ? '是' : '否' }}
          </v-chip>
        </template>
        <!-- eslint-disable-next-line vue/valid-v-slot -->
        <template #item.actions="{ item }">
          <v-btn icon small color="error" @click="confirmDelete(item)">
            <v-icon small>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-card class="mt-4">
      <v-card-title>操作日志</v-card-title>
      <v-card-text>
        <v-list dense>
          <v-list-item v-for="(log, index) in logs" :key="index">
            <v-list-item-content>
              <v-list-item-subtitle>
                <span class="font-weight-medium">{{ log.time }}</span> - {{ log.message }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <!-- 删除确认对话框 -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>确认删除</v-card-title>
        <v-card-text>
          您确定要删除域名 <strong>{{ selectedDomain?.name }}</strong> 吗？此操作不可撤销。
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey darken-1" text @click="deleteDialog = false">取消</v-btn>
          <v-btn color="error" text @click="deleteDomain" :loading="loading.delete">删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 提示消息 -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000">
      {{ snackbar.text }}
      <template #action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.show = false">关闭</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import http from '@/http'

export default {
  name: 'DomainView',
  data() {
    return {
      domains: [],
      search: '',
      sldDomain: '',
      newDomain: {
        prefix: '',
        a_record: ''
      },
      headers: [
        { text: 'ID', value: 'id', align: 'start' },
        { text: '域名', value: 'name' },
        { text: '类型', value: 'type' },
        { text: '内容', value: 'content' },
        { text: '代理状态', value: 'proxied' },
        { text: '操作', value: 'actions', sortable: false }
      ],
      loading: {
        fetch: false,
        create: false,
        delete: false,
        sld: false
      },
      logs: [],
      deleteDialog: false,
      selectedDomain: null,
      snackbar: {
        show: false,
        text: '',
        color: 'info'
      }
    }
  },
  created() {
    this.fetchDomains()
  },
  methods: {
    async fetchDomains() {
      this.loading.fetch = true
      try {
        const response = await http.get('/domain/domains')
        this.domains = response.data
        this.addLog('获取域名列表成功')
      } catch (error) {
        this.showMessage('获取域名列表失败: ' + (error.response?.data?.message || error.message), 'error')
        this.addLog('获取域名列表失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.loading.fetch = false
      }
    },
    
    async setSLD() {
      if (!this.sldDomain) {
        this.showMessage('请输入二级域名', 'warning')
        return
      }
      
      this.loading.sld = true
      try {
        await http.post(`/domain/setSLD?domain_name=${this.sldDomain}`)
        this.showMessage('二级域名设置成功', 'success')
        this.addLog(`设置二级域名: ${this.sldDomain}`)
        this.sldDomain = ''
      } catch (error) {
        this.showMessage('设置二级域名失败: ' + (error.response?.data?.message || error.message), 'error')
        this.addLog('设置二级域名失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.loading.sld = false
      }
    },
    
    async createDomain() {
      if (!this.newDomain.prefix || !this.newDomain.a_record) {
        this.showMessage('请填写完整信息', 'warning')
        return
      }
      
      if (!/^(\d{1,3}\.){3}\d{1,3}$/.test(this.newDomain.a_record)) {
        this.showMessage('IPv4地址格式不正确', 'warning')
        return
      }
      
      this.loading.create = true
      try {
        await http.post(`/domain/createDomainRecord?prefix=${this.newDomain.prefix}&a_record=${this.newDomain.a_record}`)
        this.showMessage('域名记录添加成功', 'success')
        this.addLog(`添加域名记录: ${this.newDomain.prefix}, IP: ${this.newDomain.a_record}`)
        this.newDomain.prefix = ''
        this.newDomain.a_record = ''
        this.fetchDomains()
      } catch (error) {
        this.showMessage('添加域名记录失败: ' + (error.response?.data?.message || error.message), 'error')
        this.addLog('添加域名记录失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.loading.create = false
      }
    },
    
    confirmDelete(domain) {
      this.selectedDomain = domain
      this.deleteDialog = true
    },
    
    async deleteDomain() {
      if (!this.selectedDomain) return
      
      this.loading.delete = true
      try {
        await http.post(`/domain/deleteDomainRecordByCfID?cf_id=${this.selectedDomain.id}`)
        this.showMessage('域名记录删除成功', 'success')
        this.addLog(`删除域名记录: ${this.selectedDomain.name}`)
        this.fetchDomains()
      } catch (error) {
        this.showMessage('删除域名记录失败: ' + (error.response?.data?.message || error.message), 'error')
        this.addLog('删除域名记录失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.loading.delete = false
        this.deleteDialog = false
        this.selectedDomain = null
      }
    },
    
    addLog(message) {
      const now = new Date()
      const time = now.toLocaleTimeString()
      this.logs.unshift({
        time,
        message
      })
      
      // 限制日志数量
      if (this.logs.length > 50) {
        this.logs.pop()
      }
    },
    
    showMessage(text, color = 'info') {
      this.snackbar.text = text
      this.snackbar.color = color
      this.snackbar.show = true
    }
  }
}
</script>

<style scoped>
.v-data-table {
  width: 100%;
}
</style>