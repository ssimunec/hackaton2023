<template>
 <div style="display: flex; flex: 1;">
   <AppCamera @onPictureTaken="getPicture" @onPermissionDenied="permissionDenied"/>
   <Confirmation
     v-if="recommended"
     :text="`Recommended meal item for you is: ${recommended}`"
     :yes="$lang.t('ok')"
     :stopBackdrop="true"
     @close="recommended = null"
     @confirm="recommended = null"
   ></Confirmation>
 </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import AppCamera from "./AppCamera.vue";
import {faceAnalyticsApi, getDetectorApi, recommendApi, uploadImageApi} from "./hackatonApi";
import Confirmation from "../../views/modals/Confirmation.vue";

export default defineComponent({
  components: {Confirmation, AppCamera},
  setup() {
    const recommended = ref(null);

    async function getPicture(e) {
      const imageName = `${crypto.randomUUID()}.jpeg`;
      await uploadImageApi(e.blob, imageName);
      const positions = await getDetectorApi(imageName);
      const {age, gender, sentiment} = await faceAnalyticsApi(imageName, positions);
      recommended.value = await recommendApi({age, sentiment, gender});
      console.log(recommended.value);
    }

  function permissionDenied() {
    console.log('permission denied')
  }

    return {getPicture, permissionDenied, recommended};
  },
});
</script>
