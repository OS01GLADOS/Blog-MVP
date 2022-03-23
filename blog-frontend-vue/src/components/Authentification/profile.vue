<script>
import customInputVue from "./customInput.vue"
import getCookie from "../../getCookie"
import HOST from "../../host"
import loadingVue from "../loadingScreen/loading.vue"

export default{
    name: 'Profile',
    components: {customInputVue, loadingVue},
    async mounted(){
        await this.onMount()
    },
    data() {
        return {
            isLoading: true,
            item:{
                username: 'dump username',
                email: 'example@dump.mail',
                registration_date: 'Jan 01, 1987'
            },
            inputs:[
                {
                    label: "Username",
                    value: "",
                    type: "text"
                },
                {
                    label: "Email",
                    value: "",
                    type: "email"
                },
                {
                    label: "Password",
                    value: "",
                    type: "password"
                },
                {
                    label: "Repeat password",
                    value: "",
                    type: "password"
                },
            ],
            url:HOST+'/api/profiles',
        }
    },
    methods: {
        async onMount(){
            this.$emit("mounted");
            const token = getCookie('VueBlog')
            const requestOptions = {
                method: "GET",
                headers: {
                    'Authorization':' Bearer '+ token
                }
            }
            fetch(this.url+'?self=true', requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                this.item = data.results[0]
                this.inputs[0].value = this.item.username
                this.inputs[1].value = this.item.email
                this.isLoading = false
            })
            .catch(error => {
                this.errorMessage = error
                console.error('There was an errror!', error)
                })
        },
        async handleSubmit(){
            if (this.inputs[2].value === this.inputs[3].value){
                const token = getCookie('VueBlog')
                let form = new FormData()
                form.append('username', this.inputs[0].value)
                form.append('email', this.inputs[1].value)
                form.append('password', this.inputs[2].value)
                const requestOptions = {
                    method: "PUT",
                    headers: {
                        'Authorization':' Bearer '+ token
                        },
                    body: form
                    }
                fetch(this.url+'/'+this.item.id+'/', requestOptions)
                .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                await this.onMount()
                })
                .catch(error => {
                    this.errorMessage = error
                    console.error('There was an errror!', error)
                })

            }
            else{
                alert('passwords are not the same')
            }
        }
    }
}
</script>



<template>
    <div>
        <loadingVue v-if="isLoading"></loadingVue>
        <h1>User Profile: {{item.username}}</h1>
        <!-- some info -->
            <h4>Username: {{item.username}}</h4>
            <h4>email: {{item.email}}</h4>
            <p>registration date: {{item.registration_date}}</p>
        <div>
            <h1>Change User Info</h1>
            <form @submit.prevent="handleSubmit">
                <customInputVue
                    v-for="(input ,i) in inputs"
                    :key="i"
                    v-model="input.value"
                    :label="input.label"
                    :type="input.type"
                />
                <input class="btn btn-primary mt-2" type=submit value="Submit changes">
            </form>
        </div>
    </div>
</template>