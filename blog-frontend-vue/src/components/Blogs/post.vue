<script>
export default{
    name: 'post',
    props:['title', 'body','author','publish_date', 'id'],
    computed:{
        styled_date:{
            get(){
                let date = new Date(this.publish_date);
                {
                    const options =  {month: 'long', day:'numeric', year:'numeric', hour:'numeric', minute:'numeric', seconds:'numeric'}
                    const locale = new Date().locale
                    return date.toLocaleString(locale,options)
                }
            }
        },
    }
}
</script>

<template>
    <div class="container">
                <h1><router-link :to="{name: 'showBlog', params:{ id: id} }">{{title}}</router-link></h1>
                <p class="small">{{styled_date}}  <router-link :to="{name: 'authorBlog', query:{ 'author':author}}">{{author}}</router-link></p>
            </div>
</template>