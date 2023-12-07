<template>
    <div class="w-full flex justify-between md:justify-around bg-sky-950 text-sky-950">
         

          <div class="w-2/6 flex-col md:flex-row  flex justify-around items-center">

    
          <button @click="logout" class="p-2 rounded-lg bg-emerald-200">
                        logout
            </button>
          </div>

          <input type="text" class="w-2/6 rounded-lg p-2" placeholder="source"  
          v-model="source"  
          />
          <input type="text" class="w-2/6 rounded-lg p-2" placeholder="destination" 
          v-model="destination"/>
          <button class="w-2/6 rounded-lg p-2 bg-emerald-200" @click="search">search</button>

          <button class="w-2/6 rounded-lg p-2 bg-emerald-200" @click="checkbookedseats()">booked </button>

        
    </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      <div
        v-for="bus in result"
        :key="bus.id"
        @click="routetothisbus(bus.id)"
        class="rounded-lg text-white shadow-md p-6 cursor-pointer transition duration-300 transform hover:scale-105"
        :class="{
          'bg-red-500': bus.available_seats / bus.total_seats <= 0.1,
          'bg-green-500': bus.available_seats / bus.total_seats > 0.6,
          'bg-yellow-500': bus.available_seats / bus.total_seats > 0.1 && bus.available_seats / bus.total_seats <= 0.6,
        }"
       
      >
        <h3 class="text-xl font-semibold mb-2">{{ bus.name }}</h3>
        <p>Total Seats: {{ bus.total_seats }}</p>
        <p>Departure Time: {{ bus.departure_time }}</p>
        <p>Arrival Time: {{ bus.arrival_time }}</p>
        <p>Source: {{ bus.source }}</p>
        <p>Destination: {{ bus.destination }}</p>
        <p>Fare: {{ bus.fare }}</p>
        <p>Available Days: {{ bus.available_days }}</p>
        <p>Available Seats: {{ bus.available_seats }}</p>

        <hr class="my-4 border-gray-300">
      </div>
    </div>
</template>
<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';

import { useRouter } from 'vue-router';

const router = useRouter();
const source = ref('');
const destination = ref('');
const result = ref([]);


const token = localStorage.getItem('token');

const routetothisbus = (id) => {
  router.push(`/bus/${id}`);
}; 

const checkbookedseats = () => {
  router.push(`/bookedseats`);
};

const search=async ()=>{
   console.log(source.value)
    console.log(destination.value)
    const response=await axios.get('http://localhost:8000/buses/available/'+source.value+'/'+destination.value+'/',{
        headers:{
            'Authorization':`Token ${token}`,
            'Content-Type':'application/json'
        }
    })
    if(response.status==200){

        result.value=response.data
    }
    else{
        alert("search unsuccessful")
    }
}
const logout = async () => {
  const headers = {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json',
  };
  try {
    await axios.delete('http://localhost:8000/logout/',
      { headers });
    localStorage.removeItem('token');
    alert('Logged out successfully.');
    router.push('/login');
  } catch (error) {
    alert('Error logging out.');
  }
};


</script>