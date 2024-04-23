<template>
  <div class="max-w-xl mx-auto mt-10 space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700">Stock Ticker:</label>
      <input type="text" v-model="ticker"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700">Start Date:</label>
      <input type="date" v-model="startDate"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700">End Date:</label>
      <input type="date" v-model="endDate"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700">Output Type:</label>
      <select v-model="outputType"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        <option value="json">JSON</option>
        <option value="csv">CSV</option>
      </select>
    </div>
    <button @click="submitRequest"
      class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
      Submit
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ticker: '',
      startDate: '',
      endDate: '',
      outputType: 'json'
    }
  },
  methods: {
    async submitRequest() {
      // try {
      //   const response = await fetch(`http://localhost:5000/historical-stock-data?symbol=${this.ticker}&start=${this.startDate}&end=${this.endDate}&datatype=${this.outputType}`, {
      //     method: 'GET',
      //     headers: {
      //       'Content-Type': 'application/json'
      //     },
      //     mode: 'cors'
      //   });
      //   const data = await response.json();
      //   console.log(data);
      //   alert('Data fetched successfully! Check console for details.');
      // } catch (error) {
      //   console.error('Error fetching data:', error);
      //   alert('Failed to fetch data');
      // }
      fetch(`http://localhost:5000/historical-stock-data?symbol=AMD&start=2000-03-17&end=2012-02-12&datatype=json`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));

    }
  }
}
</script>
