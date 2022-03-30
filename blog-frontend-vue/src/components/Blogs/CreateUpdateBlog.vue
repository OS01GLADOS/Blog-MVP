<script>
import customInputVue from "../Authentification/customInput.vue"
import getCookie from "../../getCookie"
import FileInput from "./fileInput.vue"
import loadingVue from "../loadingScreen/loading.vue"
import AudioInput from "./audioInput.vue"

export default {
    name: 'registration',
    components: { customInputVue, FileInput, loadingVue, AudioInput },
    data(){
        return{
            HOST: process.env.VUE_APP_SERVER_URL,
            isLoading: true,
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
            pics:[],
            audios:[],
            post_pics:[],
            post_audios:[],
            submit_label:'',
            url: '',
            method: '',
            update: false
        }
    },
    async mounted(){
        this.$emit("mounted");
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
            fetch(this.HOST+"/api/posts/"+ this.$route.params.id, requestOptions)
                .then(async response => {
                    const data = await response.json()
                    if (!response.ok){
                            const error = (data && data.message) || response.status
                            return Promise.reject(error)
                        }
                    this.inputs[0].value = data.title
                    this.inputs[1].value = data.content
                    this.post_pics = data.pics
                    this.post_audios = data.audios
                    this.isLoading = false
                })
                .catch(error => {
                    this.errorMessage = error
                    console.error('There was an errror!', error)
                })
        },
        async set_submit_value(){
            if (this.$route.query.new === 'True'){
                this.submit_label = "Create blog"
                this.url = this.HOST+"/api/posts/"
                this.method = "POST"
                this.isLoading = false
            }
            else{
                this.submit_label = "Update blog"
                this.url = this.HOST+"/api/posts/"+this.$route.params.id+ "/"
                this.onMount()
                this.method = "PUT"
                this.update = true

            }
        },
        addPicField(){
            this.pics.push({
                s3_folder : 'posts_pictures',
                api_add_link: this.HOST+'/api/postPics/'
            })
        },
        addAudioField(){
            this.audios.push({
                s3_folder : 'post_audio',
                api_add_link: this.HOST+'/api/postAudios/'
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
    <div>
        <loadingVue v-if="isLoading"></loadingVue>
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

            <div class="container" id="UpdateFunctions" v-if="update">
                <AudioInput  
                v-for="(audio, i) in audios" 
                :key="i"
                :s3_folder="audio.s3_folder"
                :api_add_link="audio.api_add_link"
                :id="this.$route.params.id"
                :audio_number="this.post_audios.length+i"
                />
                <p><input class="btn btn-primary mt-2" @click="addAudioField" type=button  value="Add audio"> </p>
            </div>
            
            <p><input class="btn btn-primary mt-2" type=submit  :value="submit_label"></p>
        </form>
        <details v-if="update">
            <summary>Related pics (insert image number like this: ||image number||)</summary>
            <div v-for=" pic in post_pics" :key="pic.id">
                <p>image number:{{pic.image_number}}</p>
                <img :src="pic.image" img width="500"/>
            </div>
        </details>
        <details v-if="update">
            <summary>Related audios (insert audio number like this: !!audio number!!)</summary>
            <div v-for=" audio in post_audios" :key="audio.id">
                <p>audio number: {{audio.audio_number}}</p>
                <label>{{audio.audio_name}}</label><br>
                <audio controls="controls">
                    <source :src="audio.audio" type="audio/mp3">
                </audio>
            </div>
        </details>
    </div>
</template>