<template>
    <div class="container mx-auto p-4">
        <h2 class="text-2xl font-bold mb-4">Admin Dashboard</h2>
        <form @submit.prevent="addBus">
            <h3 class="text-lg font-semibold mb-2">Add New Bus</h3>
            <div class="flex flex-col mb-4">
                <input v-model="newBus.name" type="text" placeholder="Bus Name" class="border rounded px-2 py-1 mb-2">
                <input v-model="newBus.total_seats" type="number" placeholder="Total Seats"
                    class="border rounded px-2 py-1 mb-2">
                <input v-model="newBus.source" type="text" placeholder="Source" class="border rounded px-2 py-1 mb-2">
                <input v-model="newBus.destination" type="text" placeholder="Destination"
                    class="border rounded px-2 py-1 mb-2">
                <input v-model="newBus.available_days" type="number" placeholder="Available Days"
                        class="border rounded px-2 py-1 mb-2">
                <input v-model="newBus.departure_time" type="time" placeholder="Departure Time"
                    class="border rounded px-2 py-1 mb-2">

                <input v-model="newBus.arrival_time" type="time" placeholder="Arrival Time"
                    class="border rounded px-2 py-1 mb-2">

                <input v-model="newBus.fare" type="number" placeholder="Fare" class="border rounded px-2 py-1 mb-2">
              
                <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Add Bus</button>
            </div>
        </form>

        <hr class="my-6">
            <h3 class="text-lg font-semibold mb-2">Existing Buses</h3>
            <div v-for="bus in buses" :key="bus.id" class="border rounded px-4 py-2 mb-2">
                <p>ID: {{ bus.id }}</p>
                <p>Name: {{ bus.name }}</p>
                <p>Total Seats: {{ bus.total_seats }}</p>
                <p>Source: {{ bus.source }}</p>
                <p>Destination: {{ bus.destination }}</p>
                <p>Departure Time: {{ bus.departure_time }}</p>
                <p>Arrival Time: {{ bus.arrival_time }}</p>
                <p>Fare: {{ bus.fare }}</p>
                <div class="mt-2">
                    <button @click="updateBus(bus)" class="bg-green-500 text-white px-3 py-1 rounded mr-2">Update</button>
                    <button @click="deleteBus(bus.id)" class="bg-red-500 text-white px-3 py-1 rounded">Delete</button>
                </div>
            </div>
        </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const buses = ref([]);
const newBus = ref({ name: '', total_seats: 0,
available_days: 0,
source: '', destination: '', departure_time: ''
, 
arrival_time: '',
fare: 0
 });

const token = localStorage.getItem('token');

const fetchBuses = async () => {
    const response=await axios.get('http://localhost:8000/buses/',{
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    }
    )
    if(response.status==200){
        buses.value=response.data
    }
    else{
        console.error('Error fetching buses:', error);
    }
};

const addBus = () => {
    axios.post('http://localhost:8000/buses/', newBus.value,
    {
        headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
    }
    )
        .then(response => {
            console.log('Bus added:', response.data);
            fetchBuses(); 
            newBus.value = { name: '', totalSeats: 0,
            available_days: 0,
            source: '', destination: '', departure_time: ''
            ,
            arrival_time: '',
            fare: 0
         };
        })
        .catch(error => {
            console.error('Error adding bus:', error);
        });
};

const updateBus = (bus) => {
   router.push(`/editbus/${bus.id}`);
};

const deleteBus = (busId) => {
    axios.delete(`http://localhost:8000/buses/${busId}/`,{
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    }) 
        .then(response => {
            console.log('Bus deleted:', response.data);
            fetchBuses();
        })
        .catch(error => {
            console.error('Error deleting bus:', error);
        });
};

onMounted(fetchBuses);
</script>
