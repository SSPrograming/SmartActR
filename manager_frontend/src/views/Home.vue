<template>
  <div class="home">
    <div class="container">
      <p>今天是 <span>{{ year }}</span> 年 <span>{{ month }}</span> 月 <span>{{ date }}</span> 日星期
        <span>{{ day }}</span></p>
      <p class="time"><span>{{ hours }}</span>:<span>{{ minutes }}</span>:<span>{{ seconds }}</span></p>
      <p>共 <span>{{ reserveNum }}</span> 个预约记录，其中 <span>{{ failNum }}</span> 个已违约</p>
      <p>小程序访问量为 <span>{{ visitNum }}</span> 人</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      year: 0,
      month: 0,
      date: 0,
      day: '',
      hours: '',
      minutes: '',
      seconds: '',
      reserveNum: 0,
      visitNum: 0,
      failNum: 0
    }
  },
  mounted() {
    const date = new Date()
    this.year = date.getFullYear()
    this.month = date.getMonth() + 1
    this.date = date.getDate()
    this.day = this.$utils.time.day2str(date.getDay())
    this.hours = this.$utils.time.fix(date.getHours(), 2)
    this.minutes = this.$utils.time.fix(date.getMinutes(), 2)
    this.seconds = this.$utils.time.fix(date.getSeconds(), 2)
    this.reserveNum = 32
    this.visitNum = 100
    this.failNum = 5
    setInterval(() => {
      const date = new Date()
      this.hours = this.$utils.time.fix(date.getHours(), 2)
      this.minutes = this.$utils.time.fix(date.getMinutes(), 2)
      this.seconds = this.$utils.time.fix(date.getSeconds(), 2)
    }, 1000)
  }
}
</script>

<style scoped>
.container {
  padding-top: 5vh;
  padding-left: 5%;
}

p {
  font-size: 24px;
  padding-bottom: 16px;
}

span {
  font-size: 28px;
  color: deeppink;
}

.time span {
  font-size: 32px;
}
</style>