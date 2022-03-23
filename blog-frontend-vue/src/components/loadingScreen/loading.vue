<style>
#loading {
  position: absolute;
  z-index: 1000;
  background-color: white;
  height: 100vh;
  width: 100vw;
  text-align: center;
  line-height: 100vh;
}
.img {
  position: relative;
  margin: auto;
  margin-top: 20%;
}
 @keyframes spinner {
        0% {
          transform: translate3d(-50%, -50%, 0) rotate(0deg);
        }
        100% {
          transform: translate3d(-50%, -50%, 0) rotate(360deg);
        }
      }
.spin::before {
  animation: 1.5s linear infinite spinner;
  animation-play-state: inherit;
  border: solid 5px #cfd0d1;
  border-bottom-color: #1c87c9;
  border-radius: 50%;
  content: "";
  height: 40px;
  position: absolute;
  top: 10%;
  left: 10%;
  transform: translate3d(-50%, -50%, 0);
  width: 40px;
  will-change: transform;
}
</style>

<template>
  <div id="loading">
    <div class="spin"></div>
  </div>
</template>

<script>
export default {
  name: "Loading"
};
</script>
