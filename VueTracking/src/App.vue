<template>
  <div class="app">
    <!-- <div class="video-box">
      <video
        id="video"
        width="320"
        height="240"
        preload
        autoplay
        loop
        muted
      ></video>
      <canvas id="canvas" width="320" height="240"></canvas>
    </div>
    <canvas id="screenshotCanvas" width="320" height="240"></canvas> -->
    <!-- <form
      method="post"
      action="http://localhost:3000/register/"
      enctype="multipart/form-data"
      target="hideIframe1"
    >
      <h3>注册</h3>
      <input type="text" placeholder="账号" name="username" />
      <input type="file" name="photo" onchange="change(e)" />
      <button style="margin-top: 10px" type="submit">注册账号</button>
    </form> -->

    <div class="box">
      <form
        method="post"
        action="http://localhost:3000/register/"
        enctype="multipart/form-data"
        target="hideIframe1"
        v-if="signUp"
      >
        <h2>Sign up</h2>
        <div class="inputBox">
          <input type="text" required="required" name="username" />
          <span>UserName</span>
          <i></i>
        </div>
        <div class="fileInput">
          <label for="btn">Photo</label>
          <input
            type="file"
            name="photo"
            id="btn"
            style="display: none"
            @change="change"
          />
          <span class="filename">{{ filename }}</span>
        </div>
        <input type="submit" value="Sign up" @click="submit()" />
        <div class="face" @click="toFace">人脸登录</div>
      </form>
      <div class="video-box" v-else>
        <video
          id="video"
          width="320"
          height="240"
          preload
          autoplay
          loop
          muted
        ></video>
        <canvas id="canvas" width="320" height="240"></canvas>
      </div>
      <canvas id="screenshotCanvas" width="320" height="240"></canvas>
      <iframe id="myIframe1" name="hideIframe1" style="display: none"></iframe>
    </div>
    <div class="tip" :class="{ display: isTip }">{{ text }}</div>
  </div>
</template>

<script>
import tracking from "@/assets/tracking/build/tracking-min.js";
import "@/assets/tracking/build/data/face-min.js";
import axios from "axios";
export default {
  data() {
    return {
      video: null,
      screenshotCanvas: null,
      uploadLock: true, // 上传锁
      filename: "",
      isTip: true,
      signUp: true,
      text: "",
    };
  },
  mounted() {
    // this.init();
  },
  methods: {
    // 初始化设置
    async init() {
      this.video = document.getElementById("video");
      this.screenshotCanvas = document.getElementById("screenshotCanvas");

      let canvas = document.getElementById("canvas");
      let context = canvas.getContext("2d");

      // 固定写法
      let tracker = new window.tracking.ObjectTracker("face");
      tracker.setInitialScale(4);
      tracker.setStepSize(2);
      tracker.setEdgesDensity(0.1);
      window.tracking.track("#video", tracker, {
        camera: true,
      });

      await this.sleep(2000);

      let _this = this;
      tracker.on("track", function (event) {
        // 检测出人脸 绘画人脸位置
        context.clearRect(0, 0, canvas.width, canvas.height);
        event.data.forEach(function (rect) {
          context.strokeStyle = "#0764B7";
          context.strokeRect(rect.x, rect.y, rect.width, rect.height);

          // 上传图片
          _this.uploadLock && _this.screenshotAndUpload();
        });
      });
    },
    // 上传图片
    async screenshotAndUpload() {
      // 上锁避免重复发送请求
      this.uploadLock = false;

      // 绘制当前帧图片转换为base64格式
      let canvas = this.screenshotCanvas;
      let video = this.video;
      let ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      console.log("camvas", canvas);
      let base64Img = canvas.toDataURL("image/png");

      // 使用 base64Img 请求接口即可
      // console.log("base64Img:", base64Img);

      axios.post("/api/check", {
          data: base64Img,
        }).then((res) => {
          const { msg } = res.data;
          console.log(msg);
          if (msg[0] !== "no match") {
            this.text = `欢迎${msg[0]}回来`;
            this.isTip = false;
            setTimeout(() => {
              this.isTip = true;
            }, 2000);
            this.signUp = true;
          } else {
            this.text = "验证失败请重新尝试";
            this.isTip = false;
            setTimeout(() => {
              this.isTip = true;
            }, 2000);
            this.signUp = true;
          }
        });

      // 请求接口成功以后打开锁
      // await this.sleep(1500);
      // this.uploadLock = true;
    },
    change(e) {
      const file = e.target.files[0];
      this.filename = file.name;
      console.log(file);
    },
    submit() {
      this.text = "注册成功!";
      this.isTip = false;
      setTimeout(() => {
        this.isTip = true;
      }, 2000);
    },
    toFace() {
      this.signUp = false;
      setTimeout(() => {
        this.init();
      }, 100);
    },
    sleep(delay) {
      return new Promise((resolve) =>
        setTimeout(() => {
          resolve();
        }, delay)
      );
    },
  },
};
</script>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
<style scoped>
/* 绘图canvas 不需显示隐藏即可 */
#screenshotCanvas {
  display: none;
}

.app {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  flex-direction: column;
  background: #23242a;
}

.box {
  position: relative;
  width: 380px;
  height: 420px;
  background: #1c1c1c;
  border-radius: 8px;
  overflow: hidden;
}

.box::before {
  content: "";
  z-index: 1;
  position: absolute;
  top: -50%;
  left: -50%;
  width: 380px;
  height: 420px;
  transform-origin: bottom right;
  background: linear-gradient(0deg, transparent, #45f3ff, #45f3ff);
  animation: animate 6s linear infinite;
}

.box::after {
  content: "";
  z-index: 1;
  position: absolute;
  top: -50%;
  left: -50%;
  width: 380px;
  height: 420px;
  transform-origin: bottom right;
  background: linear-gradient(0deg, transparent, #45f3ff, #45f3ff);
  animation: animate 6s linear infinite;
  animation-delay: -3s;
}

@keyframes animate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.video-box {
  position: relative;
  left: 0;
  right: 0;
  top: 80px;
  margin: auto;
  width: 320px;
  height: 240px;
}

video,
canvas {
  position: absolute;
  top: 0;
  left: 0;
  /* border: #000000 5px solid; */
}

form {
  position: absolute;
  inset: 2px;
  background: #28292d;
  padding: 50px 40px;
  border-radius: 8px;
  z-index: 2;
  display: flex;
  flex-direction: column;
}

h2 {
  color: #45f3ff;
  font-weight: 500;
  text-align: center;
  letter-spacing: 0.1em;
}

.inputBox {
  position: relative;
  width: 300px;
  margin-top: 35px;
  margin-bottom: 30px;
}

.inputBox input {
  position: relative;
  width: 100%;
  padding: 20px 10px 10px;
  background: transparent;
  outline: none;
  box-shadow: none;
  border: none;
  color: #23242a;
  font-size: 1em;
  letter-spacing: 0.05em;
  transition: 0.5s;
  z-index: 10;
}

.inputBox span {
  position: absolute;
  left: 0;
  padding: 20px 0px 10px;
  pointer-events: none;
  font-size: 1em;
  color: #8f8f8f;
  letter-spacing: 0.05em;
  transition: 0.5s;
}

.inputBox input:valid ~ span,
.inputBox input:focus ~ span {
  color: #45f3ff;
  transform: translateX(0px) translateY(-34px);
  font-size: 0.75em;
}

.inputBox i {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: #45f3ff;
  border-radius: 4px;
  overflow: hidden;
  transition: 0.5s;
  pointer-events: none;
  z-index: 9;
}

.inputBox input:valid ~ i,
.inputBox input:focus ~ i {
  height: 44px;
}

.links {
  display: flex;
  justify-content: space-between;
}

.links a {
  margin: 10px 0;
  font-size: 0.75em;
  color: #8f8f8f;
  text-decoration: beige;
}

.fileInput {
  margin-bottom: 40px;
}
.filename {
  margin-left: 30px;
  color: aliceblue;
}

label {
  display: inline-block;
  padding: 5px;
  background: #45f3ff;
  border-radius: 4px;
}
label:active {
  background: #05565c;
}

.links a:hover,
.links a:nth-child(2) {
  color: #45f3ff;
}

input[type="submit"] {
  border: none;
  outline: none;
  padding: 11px 25px;
  background: #45f3ff;
  cursor: pointer;
  border-radius: 4px;
  font-weight: 600;
  width: 100px;
  margin-top: 10px;
  margin: 0 auto;
}

input[type="submit"]:active {
  opacity: 0.8;
}

.tip {
  position: absolute;
  left: 0;
  right: 0;
  top: 20px;
  margin: auto;
  width: 200px;
  height: 30px;
  border-radius: 8px;
  background-color: rgba(41, 230, 255, 0.6);
  text-align: center;
  line-height: 30px;
}
.display {
  display: none;
}
.face {
  position: absolute;
  right: 20px;
  bottom: 20px;
  color: #45f3ff;
}
</style>