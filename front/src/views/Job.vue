<template>
  <div>
    <div v-if="job == 'Problem'">ERROR, Job do not exist</div>
    <div
      class="text-center mt-6 text-center text-xl leading-9 font-extrabold text-gray-900"
      v-else-if="job"
    >
      <p>
        ID: <span class="font-normal text-gray-700">{{ job.id }}</span>
      </p>
      <p>
        Status:
        <span
          :class="`font-normal text-gray-700 ${
            job.status == 'error'
              ? 'text-red-600'
              : job.status == 'process'
              ? 'text-yellow-700'
              : 'text-green-700'
          }`"
          >{{ job.status }}</span
        >
      </p>
      <p>
        Search expression:
        <span class="font-normal text-gray-700">{{
          job.search_expression
        }}</span>
      </p>
      <p>
        Value: <span class="font-normal text-gray-700"></span>{{ job.value }}
      </p>
      <div v-if="job.status != 'process'">
        <p>
          IPs resolved:
          <span class="font-normal text-gray-700">{{ job.ips_resolved }}</span>
        </p>
        <p>
          IPs matched (max 1000):
          <span class="font-normal text-gray-700">{{ job.ips_matched }}</span>
        </p>
        <p>IPs:</p>
        <div v-if="job.ips.length" class="font-normal text-gray-700">
          <p v-for="(ip, i) in job.ips" :key="i">{{ ip }}</p>
        </div>
        <div v-else class="text-red-600">No IPs for your request</div>
      </div>
      <p v-else class="text-yellow-700">
        {{ job.percentage}}%
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      job: null,
    };
  },
  async mounted() {
    try {
      let { data } = await axios.get(
        `http://localhost:5000/job/${this.$route.params.id}`
      );
      this.job = data;
    } catch (error) {
      this.job = "Problem";
    }
  },
};
</script>