<template>
  <footer class="footer">
    <div class="footer-bottom">
      <p>&copy; {{ new Date().getFullYear() }} 开发者资源管理器 | 版本 {{ version }}</p>
    </div>
  </footer>
</template>

<script>
export default {
  data(){
    return {
      version: '1.0.0' // 编译版本号
    };
  }
}
</script>

<style scoped>
.footer {
  background-color: #282c34;
  color: white;
  padding: 20px;
  text-align: center;
}

p {
  font-size: 14px;
  margin: 0;
}

@media (min-width: 768px) {
  .footer-ref {
    flex-direction: row;
    justify-content: space-around;
  }
}
</style>
