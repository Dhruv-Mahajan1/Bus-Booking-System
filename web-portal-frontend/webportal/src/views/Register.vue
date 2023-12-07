
<template>
    <div class="flex flex-col justify-center items-center w-screen h-screen bg-sky-950">

        <div class="flex flex-col justify-center items-center bg-emerald-200 rounded-xl p-4 w-3/4 md:w-1/4 lg:w-1/6  h-1/2 ">
            <h1>Sign-up</h1>
            <form @submit.prevent="submitForm" class="flex flex-col justify-center p-2 w-full h-full">
                  <label for="username">Username:</label>
                <input v-model="formData.username" type="text" id="username" required />
                <label for="email">Email:</label>
                <input v-model="formData.email" type="email" id="email" required />

                <label for="password"
                >Password:</label>
                <input v-model="formData.password" type="password" id="password" required />

                <button type="submit" class="bg-sky-950 text-white my-2">Sign Up</button>
            </form>
            <h2>
                  Already have an account?
            </h2>
            <router-link to="/login" class="bg-sky-950 text-white p-2 m-2">login</router-link>
        </div>
    </div>
</template>


<script setup>
import { ref } from 'vue';
import axios  from 'axios';
import { useRouter } from 'vue-router';
const router = useRouter();
const token = ref(null);
const formData = ref({
    username: '',
    password: '',
    email: ''
});

const submitForm = async () => {
    const response=await axios.post('http://localhost:8000/signup/', 
    {
        username: formData.value.username,
        password: formData.value.password,
        email: formData.value.email
    }
    ,
    {
        headers: {
            'Content-Type': 'application/json'
        }
    }
    )

    if(response.status==200){
        token.value=response.data.token
        localStorage.setItem('token',token.value)
        router.push('/home')
    }
    else{
        alert('Invalid Credentials')
    }
};
</script>
