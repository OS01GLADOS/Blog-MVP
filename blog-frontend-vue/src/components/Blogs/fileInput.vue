<script>
import HOST from "../../host";
import getCookie from "../../getCookie"

export default{
    name:'fileInput',
    props: ['s3_folder', 'api_add_link','id', 'image_number'],
    data(){
        return{
            label: 'Add Picture',
            image: null,
            type: 'file',
            filename: '',
            upload_link: '',
            disable_input: true,
            api_get_s3_url: HOST+'/api/geterate-upload-link/?filename=',
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

        

        uploadFile(){
        //3 upload imagelink to api
            function sendDataToDB(id, img_num, img_link){
            let form = new FormData()
            form.append('image_number', img_num)
            form.append('post', HOST+"/post/"+id+"/")
            form.append('image', img_link)
            const token = getCookie('VueBlog')

            const requestOptions = {
                    method: 'POST',
                    headers: {
                        'Authorization':' Bearer '+ token
                        },
                    body: form
            }
            fetch(HOST+'/api/postPics/', requestOptions)
            .then(async response =>{
                const data = await response.json()
                if (!response.ok){
                    const error = (data && data.message) || response.status
                    return Promise.reject(error)}
                })
                // .catch(error => {
                //     this.errorMessage = error
                //     console.error('There was an errror!', error)
                // })
            }
            let post_id = this.id
            let image_number = this.image_number
            //2 upload file to s3
            function uploadToS3(value, URL){
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
                                sendDataToDB(post_id, image_number, clean_url[0])
                            }
                    })
                    // .catch(error => {
                    //     this.errorMessage = error
                    //     console.error('There was an errror!', error)
                    // })
            }
            //1 get upload link
            let request_options = {
                method: "GET",
            }
            let URL = this.api_get_s3_url+this.s3_folder+"/"+this.id+"/"+this.filename
            fetch(URL, request_options)
                .then(async response =>{
                   const data = await response.json()
                    if (!response.ok){
                            const error = (data && data.message) || response.status
                            return Promise.reject(error)
                        }
                    uploadToS3(this.image, data.url)
                })
                // .catch(error => {
                //     this.errorMessage = error
                //     console.error('There was an errror!', error)
                // })
           
        }
    },
}


</script>

<template>
    <form @submit.prevent="uploadFile">
        {{req_res}}
        <div class="form-group">
            <label>  {{label}}   </label>
            <input
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