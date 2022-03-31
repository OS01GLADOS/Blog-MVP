<script>
export default{
    name: 'custom-input',
    props: ['label', 'type', 'modelValue'],
            computed:{
                inputValue:{
                    get(){
                        return this.modelValue
                    },
                    set(value){
                        this.$emit('update:modelValue', value)
                    }
                }
            }
    }
</script>

<template>
    <div class="form-group">
        <label>  {{label}}   </label>
        <input class="form-control" v-if="type!='textarea'" :type="type" v-model="inputValue"/>

        <textarea class="form-control" v-if="type=='textarea'" v-model="inputValue" />
 
    </div>
</template>