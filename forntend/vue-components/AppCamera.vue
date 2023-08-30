<template>
  <div style="display: flex; flex-direction: column; flex-wrap: wrap; flex: 1; align-content: space-between; justify-content: center;">
    <slot name="btn">
      <button @click="takePicture"  class="btn btn--dark btn--large flex-center single" style="font-size: 30px; margin-left: 330px; width: 27vw;">Take Picture</button>
    </slot>
    <video ref="videoElementRef" autoplay style="height: 100%"></video>

    <canvas ref="canvasElementRef" style="display: none;"></canvas>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import AppButton from "../shared/AppButton.vue";

export default {
  components: {AppButton},
  setup(pros, { emit, expose }) {
    const videoElementRef = ref<HTMLVideoElement | null>(null);
    const canvasElementRef = ref<HTMLCanvasElement | null>(null);

    const initializeCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });

        if (videoElementRef.value) {
          videoElementRef.value.srcObject = stream;
        }
      } catch (error) {
        emit('onPermissionDenied');
        throw new Error("Error accessing camera:", error);
      }
    };

    function takePicture(): Promise<{blob: Blob, url:string}> {
      return new Promise((resolve) => {
        if (videoElementRef.value && canvasElementRef.value) {
          const video = videoElementRef.value;
          const canvas = canvasElementRef.value;
          const context = canvas.getContext("2d");

          if (context) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            context.drawImage(video, 0 ,0);

            canvas.toBlob((blob) => {
              console.log(blob)
              if (blob) {
                const url = URL.createObjectURL(blob);
                resolve({blob, url});
                emit("onPictureTaken", {blob, url});

              }

              if (!blob) {
                emit('onError');
                throw new Error("Error taking picture");
              }
            }, "image/jpeg");
          }
        }
      });
    }

    expose({
      takePicture
    });

    onMounted(() => {
      initializeCamera();
    });

    onBeforeUnmount(() => {
      if (videoElementRef.value?.srcObject) {
        const stream = videoElementRef.value.srcObject as MediaStream;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    });

    return {
      videoElementRef,
      canvasElementRef,
      takePicture
    };
  },
};

export interface EventOnPictureTaken {
  blob: Blob;
  url: string;
}

</script>

<style scoped lang="scss">
/* Add your component styles here */
</style>
