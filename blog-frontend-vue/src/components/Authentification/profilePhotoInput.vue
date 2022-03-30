<script>
import getCookie from "../../getCookie"

export default{
    name:'fileInput',
    props: ['s3_folder', 'id'],
    data(){
        return{
            HOST: process.env.VUE_APP_SERVER_URL,
            label: 'Add Picture',
            image: null,
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
            this.image = files[0]
            this.disable_input = false
            this.filename = files[0].name
            },
        async uploadFile(){
        //3 upload imagelink to api
            function sendDataToDB(img_link, content){
            let form = new FormData()
            form.append('image', img_link)
            const token = getCookie('VueBlog')

            const requestOptions = {
                    method: 'PUT',
                    headers: {
                        'Authorization':' Bearer '+ token
                        },
                    body: form
            }
            let profile_id = content.id
            fetch(process.env.VUE_APP_SERVER_URL+'/api/profiles/'+profile_id+'/', requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                
                })
                content.label = "Successfully uploaded!"
            }
            //2 upload file to s3
            function uploadToS3(value, URL, context){
                request_options = {
                    method: "PUT",
                    headers: {
                        'x-amz-acl': 'public-read'
                    },
                    body: value
                }
                fetch(URL, request_options)
                    .then(async response =>{
                        if (response.ok){
                                let clean_url = URL.match(/(^[^?]*)/)
                                sendDataToDB(clean_url[0], context)
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
                    uploadToS3(this.image, data.url, this)
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
                accept="image/*"
                @change="onFilePicked"/>
        </div>
        <p>
        <input type="submit" :disabled="disable_input" value="Upload">
        </p>
    </form>
</template>