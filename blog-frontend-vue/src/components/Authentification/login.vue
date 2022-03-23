<script>
import CustomInput from "./customInput.vue"
import HOST from "../../host"

export default {
    name: "login",
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
                        type: "text"
                    },
                    {
                        label: "Password",
                        value: "",
                        type: "password"
                    },
                ],
                url:HOST+'/api/token/'
            }
            
        },
    methods:{
        handleSubmit(){
            let form = new FormData()
            form.append('username', this.inputs[0].value)
            form.append('password', this.inputs[1].value)

            const requestOptions = {
                        method: "POST",
                        body: form
                    }
            fetch(this.url, requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)
                    }
                    document.cookie="VueBlog=dumpcookie;max-age=0";
                    document.cookie="VueBlogRefresh=dumpcookie;max-age=0";  
                    document.cookie ='VueBlog='+data.access
                    document.cookie ='VueBlogRefresh='+data.refresh
                    this.$router.push({name: 'Home'})
                    })
            .catch(error => {
                this.errorMessage = error
                console.error('There was an errror!', error)
                })
            }
        }
}
</script>

<template>
    <h1>Log In</h1>
    <form @submit.prevent="handleSubmit"> 
        <CustomInput 
            v-for="(input ,i) in inputs"
            :key="i"
            v-model="input.value"
            :label="input.label"
            :type="input.type"
        />
        <input class="btn btn-primary mt-2" type=submit value="Log In">
    </form>
</template>