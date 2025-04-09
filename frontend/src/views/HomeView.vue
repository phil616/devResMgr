<template>
    <div>
        <v-container>
            <v-row>
                <v-col cols="12" sm="6">
                    <v-card to="/domain" hover>
                        <v-card-title>域名管理</v-card-title>
                        <v-card-text>
                            管理和配置域名相关设置
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-card to="/instance" hover>
                        <v-card-title>防火墙/实例管理</v-card-title>
                        <v-card-text>
                            管理防火墙规则和实例配置
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row class="mt-4">
                <v-col cols="12">
                    <v-alert type="info" text>
                        免责声明：本系统仅供内部使用，请谨慎操作。对于任何因操作不当造成的损失，使用者需承担相应责任。
                    </v-alert>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>    
export default {
    name: 'HomeView',
    data() {
        return {
        }
    }
}
</script>

<style scoped>
.v-card {
    transition: transform 0.2s;
}
.v-card:hover {
    transform: translateY(-5px);
}
</style>
