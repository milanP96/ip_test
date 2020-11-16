<template>
  <div>
    <div class="bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <h2
          class="mt-6 text-center text-3xl leading-9 font-extrabold text-gray-900"
        >
          Resolve ip adress
        </h2>
      </div>

      <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div>
            <label class="block text-sm font-medium leading-5 text-gray-700">
              Value
            </label>
            <div class="mt-1 rounded-md shadow-sm">
              <input
                v-model="value"
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 transition duration-150 ease-in-out sm:text-sm sm:leading-5"
              />
            </div>
          </div>

          <div class="mt-6">
            <label
              for="password"
              class="block text-sm font-medium leading-5 text-gray-700"
            >
              Search expression
            </label>
            <div class="mt-1 rounded-md shadow-sm">
              <input
                v-model="search_expression"
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 transition duration-150 ease-in-out sm:text-sm sm:leading-5"
              />
            </div>
          </div>

          <div class="mt-6">
            <span class="block w-full rounded-md shadow-sm">
              <button
                @click="start_job"
                class="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-500 focus:outline-none focus:border-indigo-700 focus:shadow-outline-indigo active:bg-indigo-700 transition duration-150 ease-in-out"
              >
                Start job
              </button>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div>
      <h2
        class="mt-6 text-center text-3xl leading-9 font-extrabold text-gray-900"
      >
        Last job
      </h2>
      <p class="text-center">Refresh for new job status</p>
      <div v-for="(job, i) in jobs" :key="i" class="text-center">
        <router-link class="text-center hover:text-red-500" :to="`/job/${job.id}`">
          <span class="m-4">{{ job.id }}</span>
          <span>{{ job.status }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      value: null,
      search_expression: null,
      jobs: null,
    };
  },
  methods: {
    async start_job() {
      let res = await axios.post("http://localhost:5000/job", {
        value: this.value,
        search_expression: this.search_expression,
      });
      this.jobs.push(res.data["new_job"]);
    },
    async fetch_jobs() {
      let res = await axios.get("http://localhost:5000/jobs");
      this.jobs = res.data;
    },
  },
  async mounted() {
    this.fetch_jobs();
  },
};
</script>