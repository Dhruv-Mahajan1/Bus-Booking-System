<template>
    <div class="p-6">
        <h2 class="text-3xl font-bold mb-4">Booked Tickets</h2>
        <div v-if="bookedTickets.length === 0" class="text-gray-600 mb-4">No tickets booked yet.</div>
        <div v-else>
            <div>
                <p class="text-gray-600 mb-4">Click on a ticket to cancel it.</p>
            </div>
            <div v-for="ticket in bookedTickets" :key="ticket.id" @click="showmodal(ticket.id)"
                class="border rounded-lg p-4 mb-4 cursor-pointer hover:shadow-md transition duration-300">
                <p class="text-lg font-semibold mb-1">Bus No: {{ ticket.bus }}</p>
                <p class="text-gray-600 mb-1">Booking Date: {{ ticket.booking_date }}</p>
                <p class="text-gray-600 mb-1">Booking Time: {{ ticket.booking_time }}</p>
                <p class="text-lg font-semibold">Seat Number: {{ ticket.seat_number }}</p>
                <hr class="my-2">
            </div>
        </div>

        <div v-if="error" class="text-red-500 font-semibold">{{ error }}</div>
    </div>


     <div v-if="isModalOpen" class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center">
          <div class="bg-white rounded-lg p-8 max-w-md">
            <h3 class="text-lg font-semibold mb-4">Confirm Cancellation</h3>
            <p>Are you sure you want to cancel this ticket?</p>
            <div class="mt-4 flex justify-end">
              <button
                class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none"
                @click="cancelticket"
              >
                Yes, Cancel
              </button>
              <button
                class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md ml-2 hover:bg-gray-400 focus:outline-none"
                @click="closeModal"
              >
                No, Keep Ticket
              </button>
            </div>
          </div>
        </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const bookedTickets = ref([]);
const error = ref('');
const token = localStorage.getItem('token');

const ticket = ref({ id: 0 });

const isModalOpen = ref(false);


const showmodal = (id) => {
    isModalOpen.value = true;
    ticket.value.id = id;
};

const closeModal = () => {
    ticket.value.id = 0;
    isModalOpen.value = false;
};

const cancelticket= async () => {
    const response = await axios.delete("http://localhost:8000/buses/cancel_booking/"+ticket.value.id+"/", {
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    });
    if (response.status === 200) {
        fetchBookedTickets();
        closeModal();
       
    } else {
        error.value = 'Error cancelling ticket.';
    }
};

const fetchBookedTickets = async () => {
    const response = await axios.get("http://localhost:8000/buses/viewBookedseats/",

    {
           headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
    }
    );
    if (response.status === 200) {
        bookedTickets.value = response.data;
    } else {
        error.value = 'Error fetching booked tickets.';
    }
};

onMounted(fetchBookedTickets); // Fetch booked tickets when component is mounted
</script>

<style scoped>
/* Add custom styles as needed */
.error {
    color: red;
}
</style>
