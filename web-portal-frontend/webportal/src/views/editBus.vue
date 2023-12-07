<template>
     <form @submit.prevent="updateBus" class="max-w-md mx-auto bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h3 class="text-2xl font-semibold mb-6 text-center">Edit Bus</h3>
        <div class="grid grid-cols-1 gap-4">
          <input v-model="newBus.name" type="text" placeholder="Bus Name" class="input-field">
          <input v-model="newBus.total_seats" type="number" placeholder="Total Seats" class="input-field">
          <input v-model="newBus.source" type="text" placeholder="Source" class="input-field">
          <input v-model="newBus.destination" type="text" placeholder="Destination" class="input-field">
          <input v-model="newBus.available_days" type="number" placeholder="Available Days" class="input-field">
          <input v-model="newBus.departure_time" type="time" placeholder="Departure Time" class="input-field">
          <input v-model="newBus.arrival_time" type="time" placeholder="Arrival Time" class="input-field">
          <input v-model="newBus.fare" type="number" placeholder="Fare" class="input-field">
        </div>
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-6 w-full">Save</button>
      </form>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { defineProps } from 'vue';
import axios from 'axios';
const props = defineProps({
    id:Number
});

const newBus = ref({
    name: '', total_seats: 0,
    available_days: 0,
    source: '',
    destination: '',
    departure_time: '',
    arrival_time: '',
    fare: 0
});

const token = localStorage.getItem('token');

const fetchBus = async () => {
    const response = await axios.get('http://localhost:8000/busDetail/'+props.id+"/", {
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    }
    )
    if (response.status == 200) {
        newBus.value.name = response.data.name;
        newBus.value.total_seats = response.data.total_seats;
        newBus.value.available_days = response.data.available_days;
        newBus.value.source = response.data.source;
        newBus.value.destination = response.data.destination;
        newBus.value.departure_time = response.data.departure_time;
        newBus.value.arrival_time = response.data.arrival_time;
        newBus.value.fare = response.data.fare;
    }
    else {
        console.error('Error fetching buses:', error);
    }
};
const updateBus = () => {
    axios.put(`http://localhost:8000/buses/${props.id}/`, newBus.value, {
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            console.log('Bus updated:', response.data);
            fetchBus();
        })
        .catch(error => {
            console.error('Error updating bus:', error);
        });
};

onMounted(fetchBus); 
</script>

<style>

.input-field {
    @apply border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-500;
}
</style>