<script>
import getCookie from "../../getCookie"

export default{
    name:'fileInput',
    props: ['s3_folder', 'api_add_link','id', 'audio_number'],
    data(){
        return{
            HOST: process.env.VUE_APP_SERVER_URL,
            label: 'Add Audio (mp3 file only)',
            audio: null,
            type: 'file',
            filename: '',
            upload_link: '',
            disable_input: true,
            disable_while_sended: false,
            api_get_s3_url: process.env.VUE_APP_SERVER_URL+'/api/geterate-upload-link/?filename=',
            req_res: {}
        }
    },
    methods:{

        onFilePicked (event) {
            const files = event.target.files
            const fileReader = new FileReader()
            fileReader.addEventListener('load', () => {
                this.imageUrl = fileReader.result
            })
            fileReader.readAsDataURL(files[0])
            this.audio = files[0]
            this.disable_input = false
            this.filename = files[0].name
            },
        async uploadFile(){
        //3 upload imagelink to api
            function sendDataToDB(id, audio_num, audio_link, content){
            let form = new FormData()
            form.append('audio_number', audio_num)
            form.append('audio_name', content.filename)
            form.append('post', process.env.VUE_APP_SERVER_URL+"/api/posts/"+id+"/")
            form.append('audio', audio_link)
            const token = getCookie('VueBlog')

            const requestOptions = {
                    method: 'POST',
                    headers: {
                        'Authorization':' Bearer '+ token,

                        },
                    body: form
            }
            fetch(process.env.VUE_APP_SERVER_URL+'/api/postAudios/', requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                
                })
                content.label = "Successfully uploaded!"

            }
            let post_id = this.id
            let audio_number = this.audio_number
            //2 upload file to s3
            function uploadToS3(value, URL, context){
                request_options = {
                    method: "PUT",
                    headers: {
                        'x-amz-acl': 'public-read',
                        "Content-Type": "audio/mpeg"
                    },
                    body: value
                }
                fetch(URL, request_options)
                    .then(async response =>{
                        if (response.ok){
                                let clean_url = URL.match(/(^[^?]*)/)
                                sendDataToDB(post_id, audio_number, clean_url[0], context)
                            }
                    })
            }
            //1 get upload link
            let request_options = {
                method: "GET",
            }
            let URL = this.api_get_s3_url+this.s3_folder+"/"+this.id+"/"+this.filename
            this.disable_while_sended = true
            await fetch(URL, request_options)
                .then(async response =>{
                   const data = await response.json()
                    if (!response.ok){
                            const error = (data && data.message) || response.status
                            return Promise.reject(error)
                        }
                    uploadToS3(this.audio, data.url, this)
                })           
        }
    },
}


</script>

<template>
    <form @submit.prevent="uploadFile">
        <div class="form-group">
            <label>  {{label}}   </label>
            <input
                :disabled="disable_while_sended"
                class="form-control"
                type="file"
                style="display"
                ref="fileInput"
                accept="audio/mp3"
                @change="onFilePicked"/>
        </div>
        <p>
        <input type="submit" :disabled="disable_input" value="Upload">
        </p>
    </form>
</template>