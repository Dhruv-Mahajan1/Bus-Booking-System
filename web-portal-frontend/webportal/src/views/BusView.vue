<template>
    
    <div class="w-screen h-screen flex items-center justify-center">
        <div class="border-2 border-gray-400 p-4"

        :class="{
            'bg-red-500': availableSeats.length / totalSeats <= 0.1,
            'bg-green-500': availableSeats.length / totalSeats > 0.6,
            'bg-yellow-500': availableSeats.length / totalSeats > 0.1 && availableSeats.length / totalSeats <= 0.6,
        }"
        
        >
            <div v-if="loading">Loading...</div>
            <div v-else class="grid grid-cols-10 gap-4 w-1/2 h-1/2">
                <div v-for="seat in totalSeats" :key="seat" class="rounded-md p-4 flex items-center justify-center
                border-2 border-gray-400 p-4
                "
            
                  @click="showmodal(seat)">
                    <span :class="{
                        'bg-red-500': !availableSeats.includes(seat),
                        'bg-green-500': availableSeats.includes(seat),
                    }" class="px-2 py-1 rounded-md text-white">
                        {{ seat }}
                    </span>
                </div>
            </div>
        </div>
    </div>


    <div v-if="isModalOpen" class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center">
              <div class="bg-white rounded-lg p-8 max-w-md">
                <h3 class="text-lg font-semibold mb-4">Confirm ticket</h3>
                <p>Are you sure you want to book seat {{ seat }}</p>
                <div class="mt-4 flex justify-end">
                  <button
                    class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none"
                    @click="bookseat"
                  >
                    Yes
                  </button>
                  <button
                    class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md ml-2 hover:bg-gray-400 focus:outline-none"
                    @click="closeModal"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
</template>


<script setup>
import { ref, onMounted,computed } from 'vue';
import { defineProps } from 'vue';
import axios from 'axios';

const props = defineProps({
    id:Number
});


const seat = ref(0);

const isModalOpen = ref(false);


const showmodal = (id) => {
    if (!availableSeats.value.includes(id)) {
        alert("Seat not available");
        return;
    }
    isModalOpen.value = true;
    seat.value = id;
};

const closeModal = () => {
    seat.value = 0;
    isModalOpen.value = false;
};



const availableSeats = ref([]);
const totalSeats = ref(30);
const loading = ref(false);

const token = localStorage.getItem('token');


const fetchSeatAvailability = async () => {
    loading.value = true;
    try {
        const response = await axios.get("http://localhost:8000/buses/seat_availability/"+props.id+"/", {
             headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
        });
        const data = response.data;
        totalSeats.value = data.total_seats || 0;
        availableSeats.value = data.available_seats || [];
    } catch (error) {
        console.error('Error fetching seat availability:', error);
    } finally {
        loading.value = false;
    }
};

const bookseat = async () => {
    
    if(!availableSeats.value.includes(seat.value)){
        alert("Seat not available");
        return;
    }
    loading.value = true;

    try {
        const response = await axios.post("http://localhost:8000/buses/seat_availability/"+props.id + "/", {
            seat_number: seat.value
        }, {
             headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
        });
        const data = response.data;
        fetchSeatAvailability();
    } catch (error) {
        console.error('Error fetching seat availability:', error);
    } finally {
        loading.value = false;
        closeModal();
    }
};

onMounted(() => {
    fetchSeatAvailability();
});
</script>
