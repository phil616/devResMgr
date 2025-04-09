<template>
  <v-container fluid>
    <v-card class="mb-4">
      <v-card-title>服务器实例选择</v-card-title>
      <v-card-text>
        <v-select
          v-model="selectedInstance"
          :items="instances"
          item-text="displayName"
          item-value="_InstanceId"
          label="选择服务器实例"
          return-object
          @change="loadFirewallRules"
        ></v-select>
      </v-card-text>
    </v-card>

    <v-card v-if="selectedInstance">
      <v-card-title class="d-flex justify-space-between">
        <span>防火墙规则管理</span>
        <v-btn color="primary" @click="openAddDialog">
          <v-icon left>mdi-plus</v-icon>添加规则
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="firewallRules"
          :loading="loading"
          class="elevation-1"
        >
          <template #[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- 添加/编辑规则对话框 -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span>{{ formTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-select
              v-model="editedItem.Protocol"
              :items="protocols"
              label="协议"
              required
            ></v-select>
            <v-text-field
              v-model="editedItem.Port"
              label="端口"
              required
              :rules="[v => !!v || '端口不能为空']"
            ></v-text-field>
            <v-text-field
              v-model="editedItem.CidrBlock"
              label="IPv4 CIDR"
              required
              :rules="[
                v => !!v || 'IPv4 CIDR不能为空',
                v => /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/.test(v) || 'IPv4 CIDR格式不正确'
              ]"
            ></v-text-field>
            <v-text-field
              v-model="editedItem.Ipv6CidrBlock"
              label="IPv6 CIDR (可选)"
            ></v-text-field>
            <v-select
              v-model="editedItem.Action"
              :items="actions"
              label="动作"
              required
            ></v-select>
            <v-text-field
              v-model="editedItem.FirewallRuleDescription"
              label="描述 (可选)"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close">取消</v-btn>
          <v-btn color="blue darken-1" text @click="save" :disabled="!valid">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 删除确认对话框 -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title>确认删除</v-card-title>
        <v-card-text>
          您确定要删除这条防火墙规则吗？此操作不可撤销。
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="deleteDialog = false">取消</v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 日志面板 -->
    <v-card class="mt-4">
      <v-card-title>操作日志</v-card-title>
      <v-card-text>
        <v-list dense>
          <v-list-item v-for="(log, index) in logs" :key="index">
            <v-list-item-content>
              <v-list-item-subtitle>
                {{ log.time }} - {{ log.message }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import http from '@/http'

export default {
  name: 'InstanceView',
  data() {
    return {
      instances: [],
      selectedInstance: null,
      firewallRules: [],
      loading: false,
      dialog: false,
      deleteDialog: false,
      valid: false,
      editedIndex: -1,
      editedItem: {
        Protocol: 'TCP',
        Port: '',
        CidrBlock: '',
        Ipv6CidrBlock: '',
        Action: 'ACCEPT',
        FirewallRuleDescription: ''
      },
      defaultItem: {
        Protocol: 'TCP',
        Port: '',
        CidrBlock: '',
        Ipv6CidrBlock: '',
        Action: 'ACCEPT',
        FirewallRuleDescription: ''
      },
      headers: [
        { text: '应用类型', value: '_AppType' },
        { text: '协议', value: '_Protocol' },
        { text: '端口', value: '_Port' },
        { text: 'IPv4 CIDR', value: '_CidrBlock' },
        { text: '动作', value: '_Action' },
        { text: '描述', value: '_FirewallRuleDescription' },
        { text: '操作', value: 'actions', sortable: false }
      ],
      protocols: ['TCP', 'UDP', 'ICMP', 'ALL', 'ICMPv6'],
      actions: ['ACCEPT', 'DROP'],
      logs: [],
      itemToDelete: null
    }
  },
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? '添加防火墙规则' : '编辑防火墙规则'
    }
  },
  created() {
    this.loadInstances()
  },
  methods: {
    // 加载所有服务器实例
    async loadInstances() {
      try {
        this.loading = true
        const response = await http.get('/instance/info/all?refresh=false')
        this.instances = response.data.map(instance => {
          // 创建显示名称
          const publicIp = instance._PublicAddresses && instance._PublicAddresses.length > 0 
            ? instance._PublicAddresses[0] 
            : '无公网IP'
          
          instance.displayName = `${instance._InstanceName} (${instance._InstanceId}) - ${publicIp} - ${instance._CPU}核${instance._Memory}GB - ${instance._OsName}`
          return instance
        })
        this.addLog('成功加载服务器实例列表')
      } catch (error) {
        this.addLog(`加载服务器实例失败: ${error.message}`, 'error')
        console.error('加载服务器实例失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 加载选中实例的防火墙规则
    async loadFirewallRules() {
      if (!this.selectedInstance) return
      
      try {
        this.loading = true
        // 处理region，去掉-1或-2后缀
        const region = this.selectedInstance._Zone.replace(/-[12]$/, '')
        
        const response = await http.get(`/instance/firewallRules?instance_id=${this.selectedInstance._InstanceId}&region=${region}`)
        this.firewallRules = response.data
        this.addLog(`成功加载实例 ${this.selectedInstance._InstanceName} 的防火墙规则`)
      } catch (error) {
        this.addLog(`加载防火墙规则失败: ${error.message}`, 'error')
        console.error('加载防火墙规则失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 打开添加对话框
    openAddDialog() {
      this.editedIndex = -1
      this.editedItem = Object.assign({}, this.defaultItem)
      this.dialog = true
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.resetValidation()
      })
    },

    // 编辑项目
    editItem(item) {
      this.editedIndex = this.firewallRules.indexOf(item)
      // 转换后端返回的数据格式到编辑格式
      this.editedItem = {
        Protocol: item._Protocol,
        Port: item._Port,
        CidrBlock: item._CidrBlock,
        Ipv6CidrBlock: '',  // 后端数据中可能没有这个字段
        Action: item._Action,
        FirewallRuleDescription: item._FirewallRuleDescription || ''
      }
      this.dialog = true
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.resetValidation()
      })
    },

    // 删除项目
    deleteItem(item) {
      // 转换后端返回的数据格式到删除格式
      this.itemToDelete = {
        Protocol: item._Protocol,
        Port: item._Port,
        CidrBlock: item._CidrBlock,
        Ipv6CidrBlock: '',  // 后端数据中可能没有这个字段
        Action: item._Action,
        FirewallRuleDescription: item._FirewallRuleDescription || ''
      }
      this.deleteDialog = true
    },

    // 确认删除
    async confirmDelete() {
      if (!this.selectedInstance || !this.itemToDelete) return
      
      try {
        this.loading = true
        // 处理region，去掉-1或-2后缀
        const region = this.selectedInstance._Zone.replace(/-[12]$/, '')
        
        await http.delete(`/instance/firewallRules?instance_id=${this.selectedInstance._InstanceId}&region=${region}`, {
          data: this.itemToDelete
        })
        
        this.addLog(`成功删除防火墙规则: ${this.itemToDelete.Protocol}:${this.itemToDelete.Port}`)
        // 重新加载规则列表
        await this.loadFirewallRules()
      } catch (error) {
        this.addLog(`删除防火墙规则失败: ${error.message}`, 'error')
        console.error('删除防火墙规则失败:', error)
      } finally {
        this.deleteDialog = false
        this.loading = false
        this.itemToDelete = null
      }
    },

    // 关闭对话框
    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    // 保存规则
    async save() {
      if (!this.$refs.form.validate()) return
      if (!this.selectedInstance) return
      
      try {
        this.loading = true
        // 处理region，去掉-1或-2后缀
        const region = this.selectedInstance._Zone.replace(/-[12]$/, '')
        
        if (this.editedIndex > -1) {
          // 先删除旧规则
          const oldItem = this.firewallRules[this.editedIndex]
          const deleteItem = {
            Protocol: oldItem._Protocol,
            Port: oldItem._Port,
            CidrBlock: oldItem._CidrBlock,
            Ipv6CidrBlock: '',
            Action: oldItem._Action,
            FirewallRuleDescription: oldItem._FirewallRuleDescription || ''
          }
          
          await http.delete(`/instance/firewallRules?instance_id=${this.selectedInstance._InstanceId}&region=${region}`, {
            data: deleteItem
          })
          
          // 再添加新规则
          await http.post(`/instance/firewallRules?instance_id=${this.selectedInstance._InstanceId}&region=${region}`, 
            this.editedItem
          )
          
          this.addLog(`成功更新防火墙规则: ${this.editedItem.Protocol}:${this.editedItem.Port}`)
        } else {
          // 添加新规则
          await http.post(`/instance/firewallRules?instance_id=${this.selectedInstance._InstanceId}&region=${region}`, 
            this.editedItem
          )
          
          this.addLog(`成功添加防火墙规则: ${this.editedItem.Protocol}:${this.editedItem.Port}`)
        }
        
        // 重新加载规则列表
        await this.loadFirewallRules()
        this.close()
      } catch (error) {
        this.addLog(`${this.editedIndex > -1 ? '更新' : '添加'}防火墙规则失败: ${error.message}`, 'error')
        console.error(`${this.editedIndex > -1 ? '更新' : '添加'}防火墙规则失败:`, error)
      } finally {
        this.loading = false
      }
    },

    // 添加日志
    addLog(message, type = 'info') {
      const now = new Date()
      const timeStr = now.toLocaleTimeString()
      this.logs.unshift({
        time: timeStr,
        message,
        type
      })
      
      // 限制日志数量
      if (this.logs.length > 50) {
        this.logs.pop()
      }
    }
  }
}
</script>

<style scoped>
.v-data-table {
  width: 100%;
}
</style>