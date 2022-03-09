function request(URL, request_options){
    fetch(URL, request_options)
    .then(async response =>{
        if (response.status != 204){
            const error = ('there was an error while deleting') || response.status
            return Promise.reject(error)}
        return response
    })
    .catch(error => {
        this.errorMessage = error
        console.error('There was an errror!', error)
    })

}

export default request