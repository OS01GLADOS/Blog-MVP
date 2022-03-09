<script>
import customInputVue from "../Authentification/customInput.vue"
import getCookie from "../../getCookie"
import HOST from "../../host"
import FileInput from "./fileInput.vue"

export default {
    name: 'registration',
    components: { customInputVue, FileInput },
    data(){
        return{
            inputs:[
                {
                    label: "Title",
                    value: "",
                    type: "text"
                },
                {
                    label: "Content",
                    value: "",
                    type: "textarea"
                },
            ],
            pics:[

            ],
            post_pics:[],
            submit_label:'',
            url: '',
            method: '',
            update: false
        }
    },
    async mounted(){
        await this.set_submit_value()
    },
    methods:{



        async onMount(){
            const token = getCookie('VueBlog')
            const requestOptions = {
                method: "GET",
                headers: {
                        'Authorization':' Bearer '+ token
                        },
            }
            fetch(HOST+"/api/posts/"+ this.$route.params.id, requestOptions)
                .then(async response => {
                    const data = await response.json()
                    if (!response.ok){
                            const error = (data && data.message) || response.status
                            return Promise.reject(error)
                        }
                    this.inputs[0].value = data.title
                    this.inputs[1].value = data.content
                    this.post_pics = data.pics
                })
                .catch(error => {
                    this.errorMessage = error
                    console.error('There was an errror!', error)
                })
        },
        async set_submit_value(){
            if (this.$route.query.new === 'True'){
                this.submit_label = "Create blog"
                this.url = HOST+"/api/posts/"
                this.method = "POST"
            }
            else{
                this.submit_label = "Update blog"
                this.url = HOST+"/api/posts/"+this.$route.params.id+ "/"
                this.onMount()
                this.method = "PUT"
                this.update = true
            }
        },
        addPicField(){
            this.pics.push({
                s3_folder : 'posts_pictures',
                api_add_link: HOST+'/api/postPics/'
            })
        },
        handleInput(i){
            if(i>1){
                this.inputs[i].filename = this.inputs[i].value.match(/([^\\]*)$/)[0]
            }
        },
        async handleSubmit(){
            let form = new FormData()

            form.append('pics', this.pics)
            form.append('title', this.inputs[0].value)
            form.append('content', this.inputs[1].value)
            const token = getCookie('VueBlog')
            const requestOptions = {
                    method: this.method,
                    headers: {
                        'Authorization':' Bearer '+ token
                        },
                    body: form
            }
            fetch(this.url, requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
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
    <form @submit.prevent="handleSubmit">
        <customInputVue
            
            v-for="(input ,i) in inputs"
            :key="i"
            @input="handleInput(i)"
            v-model="input.value"
            :label="input.label"
            :type="input.type"
        />
        

        <!-- for update only -->
        <div class="container" id="UpdateFunctions" v-if="update">
            <FileInput  
            v-for="(pic, i) in pics" 
            :key="i"
            :s3_folder="pic.s3_folder"
            :api_add_link="pic.api_add_link"
            :id="this.$route.params.id"
            :image_number="this.post_pics.length+i"
            />
            <p><input class="btn btn-primary mt-2" @click="addPicField" type=button  value="Add picture"> </p>
        </div>
        
        <p><input class="btn btn-primary mt-2" type=submit  :value="submit_label"></p>
    </form>

                    <div>
                    <p>Related pics</p>
                    <div v-for=" pic in post_pics" :key="pic.id">
                        <p>{{pic.image_number}}</p>
                        <img :src="pic.image"/>
                        </div>
                </div>
</template>