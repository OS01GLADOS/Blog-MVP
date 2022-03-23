<script>
import HOST from "../../host"

export default{
    name: 'post',
    props:['title', 'body','author','publish_date', 'id'],
    data(){
        return{
            data_content: '',
            pics : []
        }
    },
    mounted(){
            const requestOptions = {
                method: "GET",
            }
            fetch(HOST+"/api/posts/"+ this.$route.params.id, requestOptions)
                .then(async response => {
                    const data = await response.json()
                    if (!response.ok){
                            const error = (data && data.message) || response.status
                            return Promise.reject(error)
                        }
                    this.data_content = data.content
                    this.pics = data.pics
                    return data.author_id
                })
                .catch(error => {
                    this.errorMessage = error
                    console.error('There was an errror!', error)
                })
    },
    computed:{
        styled_body:{
                get(){
                    const re = /https?:\/\/www.youtube.com\/watch\?v=(\S*)/;
                    let res = this.data_content.replace(re,'<br><iframe width="560" height="315" src="https://www.youtube.com/embed/$1"  frameborder="0" allow="accelerometer; autoplay; clipboard-write; gyroscope; picture-in-picture" allowfullscreen></iframe><br>' )
                    const re1 = /\|\|(\d)\|\|/;
                    let pics1 = this.pics
                    res = res.replace(re1, function(x){
                        return x.replace(/\d/, function(z){
                            if(pics1.length >0){
                            console.log(z)
                            let index = z
                            console.log(index)
                            return pics1[index]['image']
                        }
                        return ''
                        })
                       
                    })
                    res = res.replace(/\|\|(.*)\|\|/,'<br><img width="500" src="$1"/><br>')
                    return res
                },
                set(value){
                    this.data_content = value
                }
           }
    },
    methods:{
        getLink(id){
            if(this.pics.length >0){
                console.log(id)
                return this.pics[id]['image']
            }
            return ''
        }
    }
}
</script>
<template>
    <div class="container">
                <h1>{{title}}</h1>
                <p v-html="styled_body"></p>
                <p class="small">{{publish_date}}  <router-link :to="{name: 'authorBlog', query:{ 'author':author}}">{{author}}</router-link></p>
            </div>
</template>