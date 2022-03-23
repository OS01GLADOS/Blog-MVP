<script>
import CustomInput from "./customInput.vue"
import HOST from "../../host"

export default {
    name: 'registration',
    components: { CustomInput },
    mounted: function() {
        this.$emit("mounted");
    },
    data(){
        return{
            inputs:[
                    {
                        label: "Username",
                        value: "",
                        type: "input"
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
                url:HOST+'/api/profiles/'
            }
        },
    methods:{
        async handleSubmit(){
                if (this.inputs[2].value === this.inputs[3].value){
                    let form = new FormData()
                    form.append('username', this.inputs[0].value)
                    form.append('email', this.inputs[1].value)
                    form.append('password', this.inputs[2].value)
                    const requestOptions = {
                        method: "POST",
                        body: form
                        }
                    fetch(this.url, requestOptions)
                    .then(async response =>{
                        const data = await response.json()
                        if (!response.ok){
                            const error = (data && data.message) || response.status
                            return Promise.reject(error)}
                            this.$router.push({name: 'login'})
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
    <h1>Registration</h1>
    <form @submit.prevent="handleSubmit">
        <CustomInput 
            v-for="(input ,i) in inputs"
            :key="i"
            v-model="input.value"
            :label="input.label"
            :type="input.type"
        />
        <input class="btn btn-primary mt-2" type=submit value="Create account">
    </form>
</template>